import os
import uuid

if "CSM_SIMULATION_ID" not in os.environ:
    os.environ["CSM_SIMULATION_ID"] = str(uuid.uuid1())

SECONDS_IN_MINUTE = 60


def get_alternative_environ_var(first_key: str, second_key: str, default_value: str):
    if first_key in os.environ:
        return os.environ[first_key]
    return os.environ.get(second_key, default_value)


class EnvironmentVariables:
    from_adt_folder = get_alternative_environ_var('SUPPLY_DRIVER_FROM_ADT_FOLDER',
                                                  'CSM_DATASET_ABSOLUTE_PATH',
                                                  '/mnt/scenariorun-data/')
    parameters_folder = get_alternative_environ_var('SUPPLY_DRIVER_PARAMETER_FOLDER',
                                                    'CSM_PARAMETERS_ABSOLUTE_PATH',
                                                    '/mnt/scenariorun-parameters/')
    temp_folder = os.environ.get('SUPPLY_DRIVER_TEMP_FOLDER',
                                 '/tmp/supply_tmp/')
    simulation_import_folder = os.environ.get('SUPPLY_DRIVER_SIMU_IMPORT_FOLDER',
                                              '/pkg/share/Simulation/Resource/Import')
    simulation_id = os.environ.get('CSM_SIMULATION_ID', str(uuid.uuid1()))
    simulation_name = os.environ.get('CSM_SIMULATION_VAR', "Simulation")
    amqp_consumer = os.environ.get('CSM_PROBES_MEASURES_TOPIC', None)
    adx_parameters = {
        "uri": os.environ.get('AZURE_DATA_EXPLORER_RESOURCE_URI', None),
        "ingest-uri": os.environ.get('AZURE_DATA_EXPLORER_RESOURCE_INGEST_URI', None),
        "database": os.environ.get('AZURE_DATA_EXPLORER_DATABASE_NAME', None)
    }
