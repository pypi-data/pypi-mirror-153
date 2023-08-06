import os
import urllib


def convert_to_boolean(string):
    """
    Shipyard can't support passing Booleans to code, so we have to convert
    string values to their boolean values.
    """
    if string in ['True', 'true', 'TRUE']:
        value = True
    else:
        value = False
    return value


def set_environment_variables(environment_variables_to_set):
    """
    Set any args.value to an environment variable.
    This will override system defaults.
    Must be formatted as:
    {'ENVIRONMENT_VARIABLE_NAME': args.value}
    """
    for environment_variable_name, arg_name in environment_variables_to_set.items():
        os.environ[environment_variable_name] = arg_name
    return


def create_shipyard_link():
    """
    Create a link back to the Shipyard log page for the currently running voyage.
    """
    org_name = os.environ.get('SHIPYARD_ORG_NAME')
    project_id = os.environ.get('SHIPYARD_PROJECT_ID')
    fleet_id = os.environ.get('SHIPYARD_FLEET_ID')
    vessel_id = os.environ.get('SHIPYARD_VESSEL_ID')
    fleet_log_id = os.environ.get('SHIPYARD_FLEET_LOG_ID')
    vessel_log_id = os.environ.get('SHIPYARD_LOG_ID')

    if project_id and fleet_id and fleet_log_id:
        dynamic_link_section = urllib.parse.quote(
            f'{org_name}/projects/{project_id}/fleets/{fleet_id}/logs/{fleet_log_id}/{vessel_log_id}')
        shipyard_link = f'https://app.shipyardapp.com/{dynamic_link_section}'
    elif project_id and vessel_id and log_id:
        dynamic_link_section = urllib.parse.quote(
            f'{org_name}/projects/{project_id}/vessels/{vessel_id}/logs/{vessel_log_id}')
        shipyard_link = f'https://app.shipyardapp.com/{dynamic_link_section}'
    else:
        shipyard_link = 'https://www.shipyardapp.com'
    return shipyard_link
