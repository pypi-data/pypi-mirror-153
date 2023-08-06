import os

try:
    import files
except BaseException:
    from . import files


def determine_base_artifact_folder(vendor):
    """
    Creates the base folder structure for storing artifacts.
    Uses USER to support local runs.
    """
    artifact_folder_default = f'{os.environ.get("USER")}-artifacts'
    base_artifact_folder = files.clean_folder_name(
        f'{os.environ.get("SHIPYARD_ARTIFACTS_DIRECTORY",artifact_folder_default)}/{vendor}-blueprints/')
    return base_artifact_folder


def create_artifacts_folders(vendor):
    """
    Creates all artifact subfolders so that generated logging files can be inserted in immediately.
    """
    base_artifact_folder = determine_base_artifact_folder(vendor)
    subfolders = ['artifacts', 'response', 'logs', 'variables']
    for subfolder in subfolders:
        files.create_folder_if_dne(files.clean_folder_name(f'{base_artifact_folder}/{subfolder}')
