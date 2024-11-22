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
    PATH = "/tmp/test_{}".format(time.time())

    def test_create_dir(self):
        path = tools.create_dir(self.PATH, may_excist=False)
        assert os.path.isdir(self.PATH)
    
    def test_create_may_excist(self):
        assert tools.create_dir(self.PATH, may_excist=True)

    def test_create_may_not_excist(self):
        try:
            tools.create_dir(self.PATH, may_excist=False)
        except FileExistsError:
            return
        assert False


if __name__ == '__main__':
    unittest.main()