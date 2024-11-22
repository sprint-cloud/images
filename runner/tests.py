import yaml
import time
import os
import unittest
import hub.tools as tools
from hub.deployment import HubApp, HubChart

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
        chart = HubChart(name='test', 
                 version='0.1')

        self.app = HubApp(name='TestApp', 
                    owner='admin', 
                    chart=chart)
        
    # Todo improve this test
    def test_generate_app(self):
        assert self.app.app_manifest()

    # Todo improve this test
    def test_generate_ns(self):
        assert self.app.namespace_manifest()

if __name__ == '__main__':
    unittest.main()