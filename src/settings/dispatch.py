import sys

from src.settings.dev import DevAppSettings
from src.settings.prod import ProdAppSettings

def create_settings():
    if 'prod' in sys.argv:
        return ProdAppSettings()
    else:
        return DevAppSettings()
