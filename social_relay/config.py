# No need to change this normally, override in locals if needed
import logging
from logging import handlers
import os

# Set this to a real domain in local config
SERVER_HOST = "http://127.0.0.1:5000"

RELAY_USERNAME = "relay"


# Just something hcard needs, override in locals if you want to customize
# This might appear visible on some pod who fetches the relay hcard...
RELAY_NAME = "Social-Relay"

# Set this to something else if you have any issues from default value
USER_AGENT = "Social-Relay 1.0 https://github.com/jaywink/social-relay"

# Relays only need a public key because Diaspora pods want to read one. So this doesn't need changing normally,
# override in locals if needed
RELAY_PUBLIC_KEY = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC9eofav26VCq3C6g9sIPjiEYzhuiFGGAMx4NAY2bP9NFxXtuERYsqtS+" \
                   "bie101/rjcDEbK5IcZY+jvCGh0P8oI/nj5kSREWxNv3OwRlCbyCtN2XR/eWEs/SfNvZysGtQunLGaUwtcyD+PUXeDuj0PH" \
                   "FuVUEudJ5DiJzu2fcUMGhLv9Xr+C2HU0tcNUjtZmYySsiVXVVrKMzj/Bgefkq7ECy3gchSgYpa2Mc5vOEBG1OxAyQvYDlE" \
                   "IohseDPo5YC9FBjp9gy7caJtvSmM5YQnDP7fjp/ghDSFtVqRWpfJbM2g9R+rAhD6w1JgvBYoOHF0ittOrbPv8WvzhaHivX" \
                   "ZADp relay@localhost"

POD_LIST_JSON = "https://the-federation.info/pods.json"

RQ_DASHBOARD = False  # Enable in local config

BOWER_COMPONENTS_ROOT = "../bower_components"

LOG_PATH = "var/social-relay.log"
LOG_TO_CONSOLE = False

# Database
DATABASE_NAME = 'var/social-relay.db'

# Redis
REDIS_DB = 0
REDIS_PORT = 6379
REDIS_HOST = 'localhost'

# Override in local config with hosts to always forward to
ALWAYS_FORWARD_TO_HOSTS = []

try:
    from social_relay.local_config import *
except ImportError:
    pass

# Set up database URI
DATABASE = 'sqlite:///{name}'.format(name=DATABASE_NAME)

RELAY_ACCOUNT = "%s@%s" % (
    RELAY_USERNAME,
    SERVER_HOST.split("//")[1]
)

# If running tests load some overrides here
if "TEST" in os.environ:
    from social_relay.tests.config import *

# Logging init
file_handler = handlers.RotatingFileHandler(
    filename=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", LOG_PATH),
    maxBytes=10000000,
    backupCount=10
)
logging_handlers = [file_handler]
if LOG_TO_CONSOLE:
    logging_handlers.append(logging.StreamHandler())

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s:%(levelname)s:%(module)s: %(message)s',
    handlers=logging_handlers
)

# Make sure we have a GUID
try:
    assert len(RELAY_GUID) == 32
except Exception:
    print("****\nYOU MUST define 'RELAY_GUID' configuration as 32 chars that will be unique *across* the "
          "whole network.\n****")
    raise

# Make sure if RQ_DASHBOARD is enabled, we have user/pass
if RQ_DASHBOARD:
    try:
        assert RQ_DASHBOARD_USERNAME
        assert RQ_DASHBOARD_PASSWORD
    except Exception:
        print("****\nYOU MUST define RQ_DASHBOARD_USERNAME and RQ_DASHBOARD_PASSWORD if RQ_DASHBOARD is enabled.\n"
              "****")
        raise
