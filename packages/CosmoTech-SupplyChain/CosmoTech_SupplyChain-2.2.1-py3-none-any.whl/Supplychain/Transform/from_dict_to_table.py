from typing import Union

from CosmoTech_Acceleration_Library.Accelerators.adx_wrapper import ADXQueriesWrapper
from Supplychain.Generic.adx_wrapper import ADXWrapper
from Supplychain.Schema.adt_column_description import ADTColumnDescription
from Supplychain.Generic.timer import Timer
from Supplychain.Generic.folder_io import FolderReader, FolderWriter

from Supplychain.Generic.adx_and_file_writer import ADXAndFileWriter

dataset_description = ADTColumnDescription.format


class FromDictToTableConverter(Timer, ADXAndFileWriter):

    def max_time_step(self,
                      file_name: str) -> int:
        file_to_convert = self.reader.files.get(file_name, [])
        file_description = dataset_description[file_name]

        time_elements = list(file_description['change'])

        max_time_step = 0

        for events in file_description['event'].values():
            time_elements.extend(events)

        for element in file_to_convert:
            _local_max = 0
            for time_element in time_elements:
                time_dict = element.get(time_element, {})
                if time_dict:
                    _end_time_step = max(map(int, time_dict.keys()))
                    _local_max = max(_local_max, _end_time_step)
            max_time_step = max(max_time_step, _local_max)
        return max_time_step

    def convert_file(self,
                     file_name: str,
                     base_row_keys: tuple):
        """
        Will open a given CSV file and convert it to a better ADX format
        The file will be separated into 2 files :
        - a "fixed" file containing non changing data
        - a "temporal" file containing all the temporal data associated to every time step by extending the data
        :param file_name: the file to convert
        :param base_row_keys: a list of rows from the fixed data that should be used as index for the temporal
        :return: None
        """

        file_to_convert = self.reader.files.get(file_name, [])

        fixed_data_filename = file_name
        temporal_data_filename = file_name + "Schedules"

        file_description = dataset_description[file_name]

        fixed_data = list()
        temporal_data = list()

        events_filenames = list(file_description['event'].keys())
        event_data = dict()
        for _name in events_filenames:
            event_data[_name] = list()

        for element in file_to_convert:
            # Each element will be converted separatly
            current_fixed_data = dict()
            if self.simulation_id is not None:
                current_fixed_data['SimulationRun'] = self.simulation_id
            current_events = dict()

            # First fixed data are read
            for _key in file_description['fixed']:
                if _key in element:
                    current_fixed_data[_key] = element[_key]
                else:
                    current_fixed_data[_key] = None

            def read_data(column_list: list) -> dict:
                schedule = dict()
                for change in column_list:
                    value = element.get(change, None)
                    if value:
                        _timesteps = sorted(value.keys(), key=int)
                        # We create our list of time steps
                        for _timestep in _timesteps:
                            if _timestep not in schedule:
                                schedule[_timestep] = dict()
                            if _timestep not in value:
                                continue
                            measure = value[_timestep]
                            # This time we have a single key so we directly add it's value
                            schedule[_timestep][change] = measure
                return schedule

            # We read the temporal data for "changes" and "events"
            current_changes = read_data(file_description['change'])
            for event_name, event_columns in file_description['event'].items():
                current_events[event_name] = read_data(event_columns)

            fixed_data.append(current_fixed_data)

            # We prepare a data structure to keep the latest change value for our data
            current_change_value = dict()
            for k in file_description['change']:
                # Needs a default value depending on the key
                current_change_value[k] = 0

            # We create a base row which will be duplicated and filed for each timestep
            present_base = [_k for _k in base_row_keys if _k in current_fixed_data]
            base_row = {_k: current_fixed_data[_k] for _k in present_base}
            previous_row = None
            for timestep in range(self.total_time_step):
                if file_description['change']:
                    current_row = base_row.copy()
                    current_row['Timestep'] = timestep

                    def change_from_key(local_key):
                        # In case of a change if the value exists in the data at a given time step
                        # we update our current value then set it in the row
                        if timestep in current_changes and local_key in current_changes[timestep]:
                            current_change_value[local_key] = current_changes[timestep][local_key]
                        current_row[local_key] = current_change_value[local_key]

                    # We loop over all our keys in "changes" and in "events"
                    for change_key in file_description['change']:
                        change_from_key(change_key)

                    # If we have any data in "changes" or "events" we keep the created row
                    to_be_kept = True
                    if previous_row is not None and not self.keep_duplicate:
                        to_be_kept = False
                        for k in previous_row.keys():
                            if k != "Timestep":
                                if current_row[k] != previous_row[k]:
                                    to_be_kept = True
                                    break
                    if to_be_kept:
                        previous_row = current_row
                        temporal_data.append(current_row)

                for event_name, event_columns in file_description['event'].items():
                    event_row = base_row.copy()
                    event_row['Timestep'] = timestep
                    event_exists = False
                    current_event = current_events[event_name]
                    for event_key in event_columns:
                        if timestep in current_event and event_key in current_event[timestep]:
                            event_row[event_key] = current_event[timestep][event_key]
                            event_exists = True
                        else:
                            # Needs a default value depending on the key
                            event_row[event_key] = 0.0
                    if event_exists or self.keep_duplicate:
                        event_data[event_name].append(event_row)

        if fixed_data:
            self.write_target_file(fixed_data, fixed_data_filename, self.simulation_id)
        else:
            fake_fixed_element = dict()
            for key in file_description['fixed']:
                fake_fixed_element[key] = None
            if self.simulation_id:
                fake_fixed_element['SimulationRun'] = self.simulation_id
            self.write_target_file([fake_fixed_element, ], fixed_data_filename, self.simulation_id)

        fake_row_keys = base_row_keys
        if self.simulation_id is None and 'SimulationRun' in base_row_keys:
            fake_row_keys = [k for k in base_row_keys if k != 'SimulationRun']

        if temporal_data:
            self.write_target_file(temporal_data, temporal_data_filename, self.simulation_id)
        elif file_description['change']:
            fake_temporal_element = dict()
            for column_list in fake_row_keys, ['Timestep', ], file_description['change']:
                for key in column_list:
                    fake_temporal_element[key] = None
            if self.simulation_id:
                fake_temporal_element['SimulationRun'] = self.simulation_id
            self.write_target_file([fake_temporal_element, ], temporal_data_filename, self.simulation_id)
        for event_name, event_file_content in event_data.items():
            if event_file_content:
                self.write_target_file(event_file_content, event_name, self.simulation_id)
            elif file_description['event'][event_name]:
                fake_event_element = dict()
                for column_list in fake_row_keys, ['Timestep', ], file_description['event'][event_name]:
                    for key in column_list:
                        fake_event_element[key] = None
                if self.simulation_id:
                    fake_event_element['SimulationRun'] = self.simulation_id
                self.write_target_file([fake_event_element, ], event_name, self.simulation_id)
        self.split("{time_since_last_split:6.4f}({time_since_start:6.4f}) - " + file_name)

    def __init__(self,
                 simulation_id: Union[str, None],
                 reader: FolderReader,
                 writer: Union[FolderWriter, None] = None,
                 adx_connector: Union[ADXQueriesWrapper, ADXWrapper, None] = None,
                 keep_duplicate: bool = True):
        """
        Init and execute transformation of the data
        :param reader: Folder reader serving files
        :param writer: Potential folder writer
        :param simulation_id: ID of the simulation to be added to every row
        :param adx_connector: Potential connecto to ADX
        :param keep_duplicate: should duplicate rows be kept ?
        """

        # Initialize the ADX wrapping
        Timer.__init__(self, '[Save to ADX]')
        ADXAndFileWriter.__init__(self,
                                  writer=writer,
                                  adx_connector=adx_connector)

        self.simulation_id = simulation_id

        self.keep_duplicate = keep_duplicate

        self.reader = reader

        # Get the total of time_steps from the configuration file
        self.total_time_step = 0

    def convert(self):
        # lookup for max time step
        if 'Configuration' in self.reader.files and len(self.reader.files['Configuration']) > 0:
            self.total_time_step = (self.reader.files['Configuration'][0]['SimulatedCycles']
                                    * self.reader.files['Configuration'][0]['StepsPerCycle'])
            self.convert_file("Configuration", ())
        else:
            self.total_time_step = max(map(self.max_time_step, ["ProductionResource",
                                                                "ProductionOperation",
                                                                "Stock",
                                                                "Transport", ])) + 1

        self.convert_file("ProductionResource", ("SimulationRun", "id",))
        self.convert_file("ProductionOperation", ("SimulationRun", "id",))
        self.convert_file("Stock", ("SimulationRun", "id",))

        self.convert_file("contains", ())
        self.convert_file("input", ())
        self.convert_file("output", ())
        self.convert_file("Transport", ("SimulationRun",
                                        "Label",))  # TODO to be replaced by RelationshipId when available from azure-digital-twins-simulator-connector
