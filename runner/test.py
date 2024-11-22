import os
from hub.tools import create_dir
from hub.deployment import HubChart, HubApp

chart = HubChart(name='test', 
                 version='0.1')

app = HubApp(name='TestApp', 
             owner='admin', 
             chart=chart)

outdir = create_dir(path='out')

out = os.path.join(outdir, 'app.yaml')
with open(out, "w") as f:
    f.write(app.app_manifest())

out = os.path.join(outdir, 'namespace.yaml')
with open(out, "w") as f:
    f.write(app.namespace_manifest())
