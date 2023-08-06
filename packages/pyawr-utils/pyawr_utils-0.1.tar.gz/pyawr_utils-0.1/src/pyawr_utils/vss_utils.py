from pyawr_utils import common_utils
import warnings
from tkinter import messagebox
import numpy as np


_Elements = common_utils._Elements
_Equations = common_utils._Equations
#
#**********************************************************************************************
#
class _SystemDiagrams():
    def __init__(self, awrde):#----------------------------------------------------
        self.awrde = awrde
        self._build_sys_diags_dict()
        #
    def _build_sys_diags_dict(self):
        '''Create list of all  system diagrams names in project '''
        self._sys_diags_dict = {}
        for sys_diag in self.awrde.Project.SystemDiagrams:
            self._sys_diags_dict[sys_diag.Name] = _SystemDiagram(self.awrde, sys_diag.Name)
        #end for
        #
    @property
    def system_diagrams_dict(self) -> dict:#------------------------------------------
        '''returns dictionary of system diagrams'''
        self._build_sys_diags_dict()
        return self._sys_diags_dict
        #  
    @property
    def system_diagram_name_list(self) -> list[str]:#-------------------------------------
        '''
        Create list of all system diagram names in project
        
        Parameters
        ----------
        None
        
        Returns
        -------
        system_diagram_name_list: list[string]
                         Each element in the list is a system digram name
        '''        
        _system_diagram_name_list = list()
        for system_diagram in self.awrde.Project.SystemDiagrams:
            _system_diagram_name_list.append(system_diagram.Name)
        #end for
        return _system_diagram_name_list
        #
    def remove_system_diagram(self, system_diagram_name: str) -> bool:
        '''
        Delete a system diagram from the AWRDE project
        
        Parameters
        ----------
        system_diagram_name: string,
                 name of the System Diagram to be deleted
        
        Returns
        -------
        system_diagram_removed: bool
                    True if system diagram successfully deleted
                    False if system diagram could not be deleted
                    
        '''  
        if not isinstance(system_diagram_name, str):
            raise RuntimeError('system_diagram_name must be a string type')
        #end if
        system_diagram_removed = False
        try:
            for sys_idx in range(self.awrde.Project.SystemDiagrams.Count):
                if self.awrde.Project.SystemDiagrams[sys_idx].Name == system_diagram_name:
                    self.awrde.Project.SystemDiagrams.Remove(sys_idx+1)
                    system_diagram_removed = True
                    break
                #end if
            #end for
        except:
            warnings.warn('remove_system_diagram: System Diagram ' + system_diagram_name + ' did not get removed')
        #end for
        return system_diagram_removed
        #
    def rename_system_diagram(self, system_diagram_name: str, new_system_diagram_name: str) -> bool:
        '''
        rename a system diagram
        
        Parameters
        ----------
        system_diagram_name: string
        new_system_diagram_name: string
        
        '''
        if not isinstance(system_diagram_name, str):
            raise RuntimeError('system_diagram_name must be a string type')
        #end if
        if not isinstance(new_system_diagram_name, str):
            raise RuntimeError('new_system_diagram_name must be a string type')
        #end if
        sys_diagram_name_list = self.system_diagram_name_list
        found_it = False
        for sys_diag_name_from_list in sys_diagram_name_list:
            if sys_diag_name_from_list == system_diagram_name:
                found_it = True
                if new_system_diagram_name in sys_diagram_name_list:
                    YesNo = messagebox.askyesno('Rename System Diagram','System Diagram '\
                        + new_system_diagram_name + ' exists. Remove existing System Diagram ?')
                    if YesNo:
                        self.remove_system_diagram(new_system_diagram_name)
                    else:
                        new_system_diagram_name += ' 1'
                    #end if
                #end if
                try:
                    sys = self.awrde.Project.SystemDiagrams(system_diagram_name)
                    sys.Name = new_system_diagram_name
                except:
                    raise RuntimeError('problem with renaming system diagram')
                #end try
                break
        #end for 
        if not found_it:
            warnings.warn('rename system diagram failed: ' + system_diagram_name)
        #end if
        #
    def copy_system_diagram(self, system_diagram_name: str, new_system_diagram_name: str) -> bool:    
        '''
        copy a system diagram
        
        Parameters
        ----------
        system_diagram_name: string
                            existing system diagram name
        new_system_diagram_name: string
                            name of the new system diagram
        
        '''        
        if not isinstance(system_diagram_name, str):
            raise RuntimeError('system_diagram_name must be a string type')
        #end if
        if not isinstance(new_system_diagram_name, str):
            raise RuntimeError('new_system_diagram_name must be a string type')
        #end if
        sys_diagram_name_list = self.system_diagram_name_list
        found_it = False
        sys_diag_idx = 1
        for sys_diag_name in sys_diagram_name_list:
            if system_diagram_name == sys_diag_name:
                found_it = True
                try:
                    self.awrde.Project.SystemDiagrams.Copy(sys_diag_idx, new_system_diagram_name)
                except:
                    raise RuntimeError('problem with copying system diagram')
                #end try
                break
                #
            #end if
            sys_diag_idx += 1
        #end for
        if not found_it:
            warnings.warn('copy system diagram failed: ' + system_diagram_name)
        #end if        
        #
    @property
    def system_frequencies(self) -> np.ndarray: #-------------------------------------------
        '''returns system frequecies from project defaults'''
        system_freq_list = list()
        for freq in self.awrde.Project.SystemDiagrams.RFBFrequencyOffsets:
            system_freq_list.append(freq.Value)
        #end for
        system_freq_ay = np.round(np.array(system_freq_list),1)
        return system_freq_ay
        #
    def set_system_frequencies(self, system_freq_ay: np.ndarray, units_str: str = 'Hz'):#-----------------------
        '''sets project frequencies'''
        #Cannot be made as a setter property due to multiple pass parameters
        units_dict = {'Hz':1, 'kHz':1e3, 'MHz':1e6, 'GHz':1e9}
        try:
            freq_multiplier = units_dict[units_str]
        except:
            raise RuntimeError('Incorrect units: ' + units_str)
        #end try
        system_freq_ay *= freq_multiplier
        try:
            self.awrde.Project.SystemDiagrams.RFBFrequencyOffsets.Clear()
            self.awrde.Project.SystemDiagrams.RFBFrequencyOffsets.AddMultiple(system_freq_ay)
        except:
            raise RuntimeError('Error in setting system frequencies')
        #end try
        #
    @property
    def system_options_dict(self) -> dict: #-----------------------------------------------
        '''returns dictionary of system default options'''
        system_options = self.awrde.Project.SystemDiagrams.Options
        sys_options_dict = {}
        for opt in system_options:
            if opt.Name != '':  #One of the options has blank as the name
                sys_options_dict[opt.Name] = opt.Value
            #end if
        #end for
        return sys_options_dict
        #
    def set_system_options_dict(self, system_options_dict: dict):#-------------------------------
        '''set system default options'''
        for opt_name, opt_value in system_options_dict.items():
            try:
                self.awrde.Project.SystemDiagrams.Options(opt_name).Value = opt_value
            except:
                raise RuntimeError('setting default system options failed: ' + opt_name + ' , ' + str(opt_value))
            #end try
        #end for
        #
    @property  
    def read_lpf_name(self) -> str:#-------------------------------------------------
        '''
        All system diagrams use the same layout process file which is the first 
        
        Returns
        -------
        sys_diag_lpf: string
        '''
        sys_diag_lpf = self.awrde.Project.ProcessDefinitions[0].name
        return sys_diag_lpf
        #
#
#**********************************************************************************************
#   
class _SystemDiagram(_Elements, _Equations):
    def __init__(self, awrde, system_diagram_name: str):#-----------------------------------------
        self.awrde = awrde
        self._initialize_system_diagram(system_diagram_name)
        #
    def _initialize_system_diagram(self, system_diagram_name):#--------------------------------------------------
        try:
            self._sys_diag = self.awrde.Project.SystemDiagrams(system_diagram_name)
        except:
            raise RuntimeError('System Diagram does not exist: ' + system_diagram_name)
        #end try
        #
        try:
            self._elem = self._sys_diag.Elements[0]
        except:
            self._elem = None
        #end try
        self._system_diagram_name = system_diagram_name
        _Elements.__init__(self, self._sys_diag, 'System')
        _Equations.__init__(self, self._sys_diag)
        #
    @property
    def system_diagram_name(self) -> str:#-----------------------------------------------------
        '''Returns name of System Diagram'''
        return self._system_diagram_name
        # 
    @property
    def frequencies(self) -> np.ndarray: #-------------------------------------------
        '''returns system frequecies from project defaults'''
        freq_list = list()
        for freq in self._sys_diag.RFBFrequencyOffsets:
            freq_list.append(freq.Value)
        #end for
        freq_array = np.round(np.array(freq_list),1)
        return freq_array
        #
    def set_frequencies(self, freq_array: np.ndarray, units_str: str = 'GHz'):#-----------------------
        '''sets project frequencies'''
        #Cannot be made as a setter property due to multiple pass parameters
        units_dict = {'Hz':1, 'kHz':1e3, 'MHz':1e6, 'GHz':1e9}
        try:
            freq_multiplier = units_dict[units_str]
        except:
            raise RuntimeError('Incorrect units: ' + units_str)
        #end try
        freq_array *= freq_multiplier
        try:
            self._sys_diag.RFBFrequencyOffsets.Clear()
            self._sys_diag.RFBFrequencyOffsets.AddMultiple(freq_array)
        except:
            raise RuntimeError('Error in setting system frequencies')
        #end try
        #
    @property
    def use_project_frequencies(self) -> bool:#----------------------------------------------
        return self._sys_diag.UseProjectRFBFrequencyOffsets
        #
    def set_use_project_frequencies(self, set_state: bool):#-------------------------------------
        if not isinstance(set_state, bool):
            raise TypeError('set_state must be a boolean')
        #end if
        self._sys_diag.UseProjectRFBFrequencyOffsets = set_state
        #
    @property
    def option_sets(self) -> dict:#----------------------------------------------------------
        '''returns dictionary of system diagram option sets'''
        sys_diagram_opt_set_dict = {}
        for optset in self._sys_diag.OptionSets:
            optset_dict = {}
            optset_name = optset.Name
            for optsubset in optset.SubSets:
                optsubset_name = optsubset.Name
                opt_dict = {}
                for opt in optsubset.Options:
                    opt_dict[opt.Name] = opt.Value
                #end for
                optset_dict[optsubset_name] = opt_dict
            #end for
            sys_diagram_opt_set_dict[optset_name] = optset_dict
        #end for
        return sys_diagram_opt_set_dict
        #
    def set_option_sets(self, sys_diagram_opt_set_dict: dict):#------------------------------
        '''sets dictionary of system diagram option sets'''
        for optset_name, optset_dict in sys_diagram_opt_set_dict.items():
            optset = self._sys_diag.OptionSets(optset_name)
            for optsubset_name, optsubset_dict in optset_dict.items():
                optsubset = optset.SubSets(optsubset_name)
                for opt_name, opt_value in optsubset_dict.items():
                    optsubset.Options(opt_name).Value = opt_value
                #end for
            #end for
        #end for
        #
    @property
    def show_options_sets(self):#---------------------------
        '''displays system diagram option sets'''
        sys_diagram_opt_set_dict = self.option_sets
        print('System Diagram Options')
        print('-'*40)        
        for optset_name, optset in sys_diagram_opt_set_dict.items():
            print('{:s}'.format(optset_name))
            for optsubset_name, optsubset in optset.items():
                print('   {:s}'.format(optsubset_name))
                for opt_name, opt_value in optsubset.items():
                    try:
                        if not isinstance(opt_value, str):
                            opt_value = str(opt_value)
                        #end if
                        print('      {:s} : {:s}'.format(opt_name, opt_value))
                    except:
                        print(opt_name, opt_value, type(opt_value))
                        raise RuntimeError('oops!')
                    #end try
                #end for
            #end for
        #end for
        #
    @property
    def option_sets_use_project_defaults(self) -> dict:#------------------------------------
        '''returns dictionary of UseProjectDefaults for options in  a system diagram'''
        use_project_defaults_dict = {}
        for optset in self._sys_diag.OptionSets:
            optsubset_dict = {}
            for optsubset in optset.SubSets:
                optsubset_dict[optsubset.Name] = optsubset.UseProjectDefaults
            #end for
            use_project_defaults_dict[optset.Name] = optsubset_dict
        #end for
        return use_project_defaults_dict
        #
    def set_option_sets_use_project_defaults(self, use_project_defaults_dict: dict):#----------
        '''sets UseProjectDefaults in system diagram options'''
        try:
            for optset_name, optset_dict in use_project_defaults_dict.items():
                optset = self._sys_diag.OptionSets(optset_name)
                for optsubset_name, use_defaults in optset_dict.items():
                    optsubset = optset.SubSets(optsubset_name)
                    optsubset.UseProjectDefaults = use_defaults
                #end for
            #end for
        except:
            raise RuntimeError('Error in applying dictionary for set_option_sets_use_project_defaults')
        #end try
        #
    @property
    def show_option_sets_use_project_defaults(self):
        '''displays the UseProjectDefaults dictionary'''
        print('Use Project Defaults')
        print('-'*40)
        use_project_defaults_dict = self.option_sets_use_project_defaults
        for optset_name, optset in use_project_defaults_dict.items():    #Print out UseDefaultOptions
            print('{:s}'.format(optset_name))
            for optsubset_name, use_defaults in optset.items():
                print('   {:s} : {:s}'.format(optsubset_name, str(use_defaults)))
            #end for
        #end for
        #