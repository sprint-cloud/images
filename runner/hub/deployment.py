import yaml, os
from typing import Optional
from pydantic import BaseModel, Field, computed_field
from jinja2 import Environment, FileSystemLoader

TEMPLATEDIR = os.getenv('HUBTEMPLATEDIR')
if TEMPLATEDIR is None:
    TEMPLATEDIR = './templates'

env = Environment(loader = FileSystemLoader(TEMPLATEDIR),   trim_blocks=True, lstrip_blocks=True)

'''
 apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: {{ name }}
  namespace: argocd
  labels:
     hub/owner: {{ owner }}
spec:
  project: apps
  source:
    chart: "{{ chart.name }}"
    repoURL: "{{ chart.repo }}"
    targetRevision: "{{ chart.version }}"
    helm:
      valuesObject:
        {{ chart.values | indent(8) }}
  destination:
    server: https://kubernetes.default.svc
    namespace: {{ appns }}
  syncPolicy:
    automated:
      prune: true
      selfHeal: true 
'''
class Metadata(BaseModel):
    name: str
    namespace: str
    labels: dict = None
    annotations: dict = {}

class Manifest(BaseModel):
    metadata: Metadata

class AppUser(BaseModel):
    email: str
    name: str

class IngressTls(BaseModel):
    hosts: list[str]

class IngressPath(BaseModel):
    path: str = "/"
    pathType: str = "ImplementationSpecific"

class IngressHost(BaseModel):
    host: str
    paths: list[IngressPath] = [IngressPath()]

class AppIngress(BaseModel):
    className: str = "apps"
    hosts: list[IngressHost] = []
    tls: Optional[IngressTls]
        
def ingress_factory(val):
    tls = IngressTls(hosts=[val['domain']])
    host = IngressHost(host=val['domain'])
    return AppIngress(hosts=[host], tls=tls)

class Resources(BaseModel):
    cpu: str = '250m'
    mem: str = '128Mi'

class ResourceValues(BaseModel):
    requests: Resources = Resources()
    limits: Resources = Resources()

class HelmValues(BaseModel):
    domain: str
    user: AppUser
    ingress: AppIngress = Field(default_factory=ingress_factory)
    resources: ResourceValues = ResourceValues()

class Helm(BaseModel):
    valuesObject: HelmValues

class AppSource(BaseModel):
    chart: str
    TargetRevision: str
    repoUrl: str = 'ghcr.io/sprint-cloud'
    Helm: Helm

class AppDestination(BaseModel):
    server: str = 'https://kubernetes.default.svc'
    namespace: str

class AppSync(BaseModel):
    prune: bool = True
    selfHeal: bool = True

class AppSyncPolicy(BaseModel):
    automated: AppSync = AppSync()
    syncOptions: list = ['CreateNamespace=true']

class AppSpec(BaseModel):
    project: str = "apps"
    source: AppSource
    destination: AppDestination
    syncPolicy: AppSyncPolicy = AppSyncPolicy()

class ArgoApp(Manifest):
    apiVersion: str = 'argoproj.io/v1alpha1'
    spec: AppSpec

def generate_app_source(chart: str, version: str, values: HelmValues):
    return AppSource(
            chart=chart, 
            TargetRevision=version, 
            Helm=Helm(valuesObject=values))

def generate_app(appname:str, source:AppSource, user:AppUser):
    meta = Metadata(name = appname, 
                    namespace = "argocd",
                    labels = {
                        'user': user.name,
                        'email': user.email
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



