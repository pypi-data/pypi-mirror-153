import os
from os.path import join
from pathlib import Path

# export SFY_SERVER="https://sf-server.tfy-ctl-euwe1-devtest.devtest.truefoundry.tech"
# export SFY_TENANT_ID="895253af-ec9d-4be6-83d1-6f248e644e79"
# export AUTH_UI="https://app.devtest.truefoundry.tech"
# export AUTH_SERVER="https://auth-server.tfy-ctl-euwe1-devtest.devtest.truefoundry.tech"

SERVICE_FOUNDRY_SERVER = (
    os.getenv("SFY_SERVER")
    or "https://sf-server.tfy-ctl-euwe1-production.production.truefoundry.com"
)

# Auth related config
# TODO: Call service foundry to get this.
DEFAULT_TENANT_ID = os.getenv("SFY_TENANT_ID") or "f80b91e0-2ac8-4b03-8e0b-e88e7844fd11"
AUTH_UI = os.getenv("SFY_AUTH_UI") or "https://app.truefoundry.com"
AUTH_SERVER = (
    os.getenv("SFY_AUTH_SERVER")
    or "https://auth-server.tfy-ctl-euwe1-production.production.truefoundry.com"
)
SESSION_FILE = str(Path.home() / ".truefoundry")

# Build related Config
SERVICE_DEF_FILE_NAME = "servicefoundry.yaml"
TEMPLATE_DEF_FILE_NAME = "template.yaml"
SFY_DIR = ".servicefoundry"
BUILD_DIR = join(SFY_DIR, "build")

COMPONENT = "Component"
BUILD_PACK = "BuildPack"
KIND = "kind"

# Polling during login redirect
MAX_POLLING_RETRY = 100
POLLING_SLEEP_TIME_IN_SEC = 4

# Refresh access token cutoff
REFRESH_ACCESS_TOKEN_IN_SEC = 10 * 60

ENTITY_JSON_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
