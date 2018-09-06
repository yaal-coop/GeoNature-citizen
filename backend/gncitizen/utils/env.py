import os
import sys
from pathlib import Path

from flask_sqlalchemy import SQLAlchemy

from gncitizen.utils.utilstoml import load_toml

ROOT_DIR = Path(__file__).absolute().parent.parent.parent.parent
BACKEND_DIR = ROOT_DIR / 'backend'
DEFAULT_VIRTUALENV_DIR = BACKEND_DIR / "venv"
with open(str((ROOT_DIR / 'VERSION'))) as v:
    GEONATURE_VERSION = v.read()
DEFAULT_CONFIG_FILE = ROOT_DIR / 'config/default_config.toml'
GNC_EXTERNAL_MODULE = ROOT_DIR / 'external_modules'


def get_config_file_path(config_file=None):
    """ Return the config file path by checking several sources

        1 - Parameter passed
        2 - GEONATURE_CONFIG_FILE env var
        3 - Default config file value
    """
    config_file = config_file or os.environ.get('GEONATCITIZEN_CONFIG_FILE')
    return Path(config_file or DEFAULT_CONFIG_FILE)


def load_config(config_file=None):
    """ Load the geonature-citizen configuration from a given file """
    config_gnc = load_toml(get_config_file_path())

    return config_gnc


SQLALCHEMY_DATABASE_URI = load_config()['SQLALCHEMY_DATABASE_URI']
db = SQLAlchemy()


def list_and_import_gn_modules(app, mod_path=GNC_EXTERNAL_MODULE):
    """
        Get all the module enabled from gn_commons.t_modules
    """
    # with app.app_context():
    #     data = db.session.query(TModules).filter(
    #         TModules.active_backend == True
    #     )
    #     enabled_modules = [d.as_dict()['module_name'] for d in data]

    # iter over external_modules dir
    #   and import only modules which are enabled
    for f in mod_path.iterdir():
        if f.is_dir():
            conf_manifest = load_toml(str(f / 'manifest.toml'))
            module_name = conf_manifest['module_name']
            module_path = Path(GNC_EXTERNAL_MODULE / module_name)
            module_parent_dir = str(module_path.parent)
            module_name = "{}.config.conf_schema_toml".format(module_path.name)
            sys.path.insert(0, module_parent_dir)
            module = __import__(module_name, globals=globals())
            module_name = "{}.backend.blueprint".format(module_path.name)
            module_blueprint = __import__(module_name, globals=globals())
            sys.path.pop(0)

            conf_module = load_toml(str(f / 'config/conf_gn_module.toml'))
            print(conf_module, conf_manifest, module_blueprint)

            yield conf_module, conf_manifest, module_blueprint
