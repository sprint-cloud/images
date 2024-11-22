import os
from hub import deployment, create_dir

chart = deployment.HubChart(name='test', 
                 version='0.1')

app = deployment.HubApp(name='TestApp', 
             owner='admin', 
             chart=chart)

outdir = create_dir('out')

out = os.path.join(outdir, 'app.yaml')
with open(out, "w") as f:
    f.write(app.app_manifest())

out = os.path.join(outdir, 'namespace.yaml')
with open(out, "w") as f:
    f.write(app.namespace_manifest())
