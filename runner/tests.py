import yaml
import time
import os
import unittest
import hub.tools as tools
from hub.deployment import Helm, HelmValues, AppUser, generate_app_source, generate_app, read_apps, generate_manifest


class TestCreateDir(unittest.TestCase):

    def setUp(self):
        self.path = tools.create_temp_dir()
    
    def test_create_may_excist(self):
        assert tools.create_dir(self.path, may_excist=True)

    def test_create_may_not_excist(self):
        try:
            tools.create_dir(self.path, may_excist=False)
        except FileExistsError:
            return
        assert False



class TestDeployment(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tools.create_dir('/tmp/testout')
   
    # Todo: update to mock
    def test_generate_apps(self):
        for appname in ['my-blog', 'myapi', 'anotherapp']:
            out = tools.create_dir(f"{self.tmpdir}/{appname}")
            user = AppUser(email='user@example.com', name='username')
            values = HelmValues(user=user, domain="app.example.com")
            source = generate_app_source('wordpress', version='0.0.*', values=values)
            app  = generate_app(appname=appname, source=source, user=user, workflowName='test-workflow')
            ns = app.generate_namespace()
            ns.to_yaml(f"{out}/namespace.yaml")
            app.to_yaml(f"{out}/app.yaml")

    def test_read_apps(self):
        apps = read_apps(self.tmpdir)

   

if __name__ == '__main__':
    unittest.main()