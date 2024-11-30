import os
import json, yaml
from datetime import datetime
from typing import Optional, Annotated
from pydantic import BaseModel, Field, computed_field
from jinja2 import Environment, FileSystemLoader

TEMPLATEDIR = os.getenv('HUBTEMPLATEDIR')
if TEMPLATEDIR is None:
    TEMPLATEDIR = './templates'

env = Environment(loader = FileSystemLoader(TEMPLATEDIR),   trim_blocks=True, lstrip_blocks=True)

class HubModel(BaseModel):
    @classmethod
    def from_json(cls, data:str):
        return cls(**json.loads(data))
    
    def to_json(self, out:str):
        with open(out, "w") as f:
            data = self.model_dump_json()
            f.write(data)
        return out
    
    def from_yaml(self, path:str):
        with open(path, "w") as f:
            return self(**yaml.safe_load(f.read()))

    def to_yaml(self, out: str):
        with open(out, "w") as f:
            f.write(yaml.dump(self.model_dump()))
        return out

class Metadata(HubModel):
    name: str
    namespace: Optional[str] = None
    labels: dict = {}
    annotations: dict = {}

class Manifest(HubModel):
    metadata: Metadata

class AppUser(HubModel):
    email: str
    name: str

class IngressTls(HubModel):
    hosts: list[str]

class IngressPath(HubModel):
    path: str = "/"
    pathType: str = "ImplementationSpecific"

class IngressHost(HubModel):
    host: str
    paths: list[IngressPath] = [IngressPath()]

class AppIngress(HubModel):
    enabled: bool = True
    className: str = "apps"
    hosts: list[IngressHost] = []
    tls: Optional[IngressTls]
        
def ingress_factory(val):
    tls = IngressTls(hosts=[val['domain']])
    host = IngressHost(host=val['domain'])
    return AppIngress(hosts=[host], tls=tls)

class Resources(HubModel):
    cpu: str = '250m'
    mem: str = '128Mi'

class ResourceValues(HubModel):
    requests: Resources = Resources()
    limits: Resources = Resources()

class HelmValues(HubModel):
    domain: str
    user: AppUser
    ingress: AppIngress = Field(default_factory=ingress_factory)
    resources: ResourceValues = ResourceValues()


class Helm(HubModel):
    valuesObject: HelmValues

class AppSource(HubModel):
    chart: str
    targetRevision: str
    repoURL: str = 'ghcr.io/sprint-cloud'
    Helm: Helm

class AppDestination(HubModel):
    server: str = 'https://kubernetes.default.svc'
    namespace: str

class AppSync(HubModel):
    prune: bool = True
    selfHeal: bool = True

class AppSyncPolicy(HubModel):
    automated: AppSync = AppSync()
    syncOptions: list = []

class AppSpec(HubModel):
    project: str = "apps"
    source: AppSource
    destination: AppDestination
    syncPolicy: AppSyncPolicy = AppSyncPolicy()

class Namespace(Manifest):
    apiVersion: str = 'v1'
    kind: str = 'Namespace'

class ArgoApp(Manifest):
    apiVersion: str = 'argoproj.io/v1alpha1'
    kind: str = 'Application'
    spec: AppSpec

    def generate_namespace(self):
        meta = Metadata(
            name = f"app-{self.metadata.name}"
        )
        return Namespace(metadata=meta)

def generate_app_source(chart: str, version: str, values: HelmValues):
    return AppSource(
            chart=chart, 
            targetRevision=version, 
            Helm=Helm(valuesObject=values))

def generate_app(appname:str, source:AppSource, user:AppUser):
    meta = Metadata(name = appname, 
                    namespace = "argocd",
                    labels = {
                        'pipeline': 'true'
                    }
                    )
    namespace = f"app-{appname}"
    spec = AppSpec(source=source, 
                   destination=AppDestination(namespace=namespace))
    return ArgoApp(
            metadata =  meta,
            spec = spec
        )

def generate_manifest(app:ArgoApp, outdir: str):
    out = f"{outdir}/app.yaml"
    with open(out, "w") as f:
        f.write(yaml.dump(app.model_dump()))
    return out


def read_apps(appdir: str) -> list[ArgoApp]:
    apps: list[ArgoApp] = []
    app_paths = [f.path for f in os.scandir(appdir) if f.is_dir()]
    for path in app_paths:
        manifest = f"{path}/app.yaml"
        if not os.path.exists(manifest):
            print(f"{manifest} does not exist...")
            continue
        with open(f"{path}/app.yaml", "r") as f:
            print(f"Reading: { manifest }...")
            data = yaml.safe_load(f.read())
            apps.append(ArgoApp(**data))
    return apps