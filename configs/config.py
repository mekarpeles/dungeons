import io
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('configs/network.cfg')
PORT = int(config.get("telnet", "port"))
HOST = config.get("telnet", "host")
DEBUG_MODE = bool(config.get("server", "debug"))

SCOPES = {"room": lambda controller, protocol: controller.character.position == protocol.character.position,
          "world": lambda controller, protocol: True}
