import ipynbname
import pkg_resources
import os

from ml_sdk.ml.model.notebook import WatchmenNotebook


def get_notebook(storage_type:str,storage_location:str = None):
    note_name = ipynbname.name()
    path = ipynbname.path()
    if storage_location is not None:
        notebook = WatchmenNotebook(name=note_name, storageLocation=storage_location, storageType=storage_type)
    else:
        notebook = WatchmenNotebook(name=note_name, storageLocation=str(path), storageType=storage_type)

    return get_dependencies(notebook)


def get_dependencies(notebook: WatchmenNotebook):
    for m in pkg_resources.working_set:
        notebook.dependencies[m.project_name] = m.version
    return notebook


def get_environment():
    environments = {}
    # environments = os.environ.values()
    for item, value in os.environ.items():
        environments[item] = value

    return environments


