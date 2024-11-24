import yaml, os
from pydantic import BaseModel, Field, computed_field
from jinja2 import Environment, FileSystemLoader

TEMPLATEDIR = os.getenv('HUBTEMPLATEDIR')
if TEMPLATEDIR is None:
    TEMPLATEDIR = './templates'

env = Environment(loader = FileSystemLoader(TEMPLATEDIR),   trim_blocks=True, lstrip_blocks=True)


class HubChart(BaseModel):
    name: str
    version: str
    repo: str = Field(default='ghcr.io/sprint-cloud')
    values: dict = Field(default_factory=dict)

class HubApp(BaseModel):
    name: str
    owner: str
    chart: HubChart
    namespace: str = Field(default='argocd')
    image: str = Field(default=None) 

    @computed_field
    @property
    def appnamespace(self) -> str:
        return "{}-{}".format('app', self.name.lower())
    
    @computed_field
    @property
    def domainhost(self) -> str:
        return self.name.lower()
    
    def app_manifest(self) -> str:
        return env.get_template('app_tmpl.j2').render(self, 
                                                      appns=self.appnamespace,
                                                      host=self.domainhost)
    def namespace_manifest(self) -> str:
        return env.get_template('namespace_tmpl.j2').render(self, 
                                                      appns=self.appnamespace)
    
