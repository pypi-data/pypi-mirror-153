from pyawr_utils import common_utils, awrde_utils
import numpy as np
import warnings
import itertools

_Elements = common_utils._Elements
_Equations = common_utils._Equations
#
#*****************************************************************************************************
#

# class _Options():

class _Schematics():
    '''Class that contains class constructors and methods at the Circuit Schematics level in the AWR project tree'''

    def __init__(self, project):
        self._schematics = project.Schematics
        self._build_circuit_schematics_dict()

    def _build_circuit_schematics_dict(self):
        self._circuit_schematics_dict = {}
        #
        #
        #schematic = self._schematics('LPF')
        #self._circuit_schematics_dict[schematic.Name] = _Schematic(self._schematics(schematic.Name))
        #
        #
        for schematic in self._schematics:
            try:
                self._circuit_schematics_dict[schematic.Name] = _Schematic(self._schematics(schematic.Name))
            except:
                raise RuntimeError('Failed to create circuit schematics dictionary')

    @property
    def circuit_schematics_dict(self) -> dict:
        return self._circuit_schematics_dict

    def add_circuit_schematic(self, circuit_schematic_name: str) -> bool:
        if not isinstance(circuit_schematic_name, str):
            raise TypeError('Schematic diagram name must be a string type')

        elif isinstance(circuit_schematic_name, str):
            if circuit_schematic_name == self._schematics.GetUniqueName(circuit_schematic_name):
                new_circuit_schematic = self._schematics.Add(circuit_schematic_name)
                self._circuit_schematics_dict[new_circuit_schematic.Name] = _Schematic(
                                                                            self._schematics(circuit_schematic_name))

            elif circuit_schematic_name != self._schematics.GetUniqueName(circuit_schematic_name):
                warnings.warn('Circuit schematic name ' + circuit_schematic_name \
                               + ' is already in use')

            else:
                warnings.warn('Circuit schematic failed to be added')

        return self._circuit_schematics_dict

    def remove_circuit_schematic(self, circuit_schematic_name: str) -> dict:
        if not isinstance(circuit_schematic_name, str):
            raise TypeError('Schematic diagram name must be a string type')

        elif isinstance(circuit_schematic_name, str):
            try:
                for circuit_schematic_index in range(1, self._schematics.Count + 1):
                    if circuit_schematic_name == self._schematics(circuit_schematic_index).Name:
                        circuit_schematic_removed = self._schematics.Remove(circuit_schematic_index)

                        if circuit_schematic_removed == True:
                            self._circuit_schematics_dict.pop(circuit_schematic_name)
                        else:
                            warnings.warn('Circuit schematic ' + new_circuit_schematic_name \
                                          + 'was not deleted')

                        break

            except:
                warnings.warn('remove_circuit_schematic: Circuit Schematic ' + circuit_schematic_name  \
                              + ' did not get removed')

        return self._circuit_schematics_dict

    def copy_circuit_schematic(self, existing_circuit_schematic_name: str, new_circuit_schematic_name: str) -> dict:
        if not isinstance(existing_circuit_schematic_name, str) and not isinstance(new_circuit_schematic_name, str):
            raise TypeError('Schematic diagram names must be a string type')

        elif new_circuit_schematic_name != self._schematics.GetUniqueName(new_circuit_schematic_name):
            warnings.warn('New circuit schematic name ' + new_circuit_schematic_name \
                                + 'is already in use')

        elif self._circuit_schematics_dict.get(existing_circuit_schematic_name) is None:
            warnings.warn('Circuit schematic name ' + existing_circuit_schematic_name \
                          + 'cannot be copied because it does not exist')

        elif existing_circuit_schematic_name in self._circuit_schematics_dict.keys():
            schematic_count = 0
            for schematic in self._schematics:
                if existing_circuit_schematic_name == schematic.Name:
                    new_circuit_schematic = self._schematics.Copy(schematic_count, new_circuit_schematic_name)
                    self._circuit_schematics_dict[new_circuit_schematic.Name] = _Schematic(
                                                                        self._schematics(new_circuit_schematic_name))
                    break

                schematic_count += 1

        return self._circuit_schematics_dict

    def rename_circuit_schematic(self, existing_circuit_schematic_name: str, new_circuit_schematic_name: str) -> dict:
        if not isinstance(existing_circuit_schematic_name, str) and not isinstance(new_circuit_schematic_name, str):
            raise TypeError('Schematic diagram names must be a string type')

        elif new_circuit_schematic_name != self._schematics.GetUniqueName(new_circuit_schematic_name):
            warnings.warn('New circuit schematic name ' + new_circuit_schematic_name \
                                + 'is already in use')

        elif existing_circuit_schematic_name in self._circuit_schematics_dict.keys():
            schematic_count = 0
            for schematic in self._schematics:
                if existing_circuit_schematic_name == schematic.Name:
                    self._schematics(existing_circuit_schematic_name).Name = new_circuit_schematic_name
                    self._circuit_schematics_dict[new_circuit_schematic_name] = self._circuit_schematics_dict[
                                                                                    existing_circuit_schematic_name]
                    self._circuit_schematics_dict.pop(existing_circuit_schematic_name)
                    break

                schematic_count += 1

        return self._circuit_schematics_dict
#
#*****************************************************************************************************
#
class _Schematic(_Elements, _Equations): 

    def __init__(self, circuit_schematic):
        self._circuit_schematic = circuit_schematic
        _Elements.__init__(self, self._circuit_schematic, 'Schematic')
        _Equations.__init__(self, self._circuit_schematic)
        

    @property
    def circuit_schematic_name(self) -> str:
        '''Returns name of circuit schematics'''
        return self._circuit_schematic.Name

    @property
    def frequency_range(self) -> np.ndarray:
        '''Returns circuit schematic frequency range'''
        self.frequency_array = np.array([round(frequency.Value) for frequency in self._circuit_schematic.Frequencies])
        return self.frequency_array

    def set_frequency_range(self, frequency_array: np.ndarray, units_str: str = 'GHz'):
        '''Sets circuit cchematic frequency range'''
        units_dict = {'Hz':1, 'kHz':1e3, 'MHz':1e6, 'GHz':1e9}
        try:
            frequency_multiplier = units_dict[units_str]

        except:
            raise RuntimeError('Incorrect units: ' + units_str)

        frequency_array = np.multiply(frequency_array, frequency_multiplier)
        try:
            self._circuit_schematic.UseProjectFrequencies = False
            self._circuit_schematic.Frequencies.Clear()
            self._circuit_schematic.Frequencies.AddMultiple(frequency_array)

        except:
            raise RuntimeError('Error in setting circuit schematic frequencies')

    @property
    def use_project_frequencies(self) -> bool:
        return self._circuit_schematic.UseProjectFrequencies

    @use_project_frequencies.setter
    def use_project_frequencies(self, set_state: bool) -> bool:
        if not isinstance(set_state, bool):
            raise TypeError('set_state must be a boolean')

        self._circuit_schematic.UseProjectFrequencies = set_state
        return self._circuit_schematic.UseProjectFrequencies

    @property
    def options(self)->dict:
        '''Gets Circuit Schematic settings with a dictionary of option values'''
        pass


    @options.setter
    def options(self, circuit_schematic_option_set_dict: dict):
        '''Sets Circuit Schematic settings with a dictionary of option values'''
        for option_set_dict_key, option_set_dict_value in circuit_schematic_option_set_dict.items():
            pass


































