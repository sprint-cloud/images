import yaml
import time
import os
import unittest
import hub.tools as tools
from hub.deployment import HubApp, HubChart

chart = HubChart(name='test', 
                 version='0.1')

app = HubApp(name='TestApp', 
             owner='admin', 
             chart=chart)

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


if __name__ == '__main__':
    unittest.main()