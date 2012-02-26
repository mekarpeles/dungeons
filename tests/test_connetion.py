import unittest
import telnetlib
from dungeons.configs.config import PORT
from dungeons.configs.config import HOST

class TestConnection(unittest.TestCase):

    def test_connect(self):
        try:
            print PORT
            print HOST
            conn = telnetlib.Telnet(HOST, PORT)
        except:
            raise

    
    
