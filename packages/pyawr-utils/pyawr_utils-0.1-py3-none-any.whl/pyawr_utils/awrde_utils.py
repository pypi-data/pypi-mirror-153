import pyawr.mwoffice as mwo
from pyawr_utils import schematic_utils, vss_utils, graph_utils, common_utils, misc_utils
import time as tm
import numpy as np
#
_Schematics = schematic_utils._Schematics
_SystemDiagrams = vss_utils._SystemDiagrams
_Graphs = graph_utils._Graphs
_DataFiles = misc_utils._DataFiles
#
def establish_link(version_str: str ='', clsid_str:str ='') -> object:
    '''
    returns object variable object that is the AWRDE instance
    
    Parameters
    ----------
    version_str: string, optional
            Revision number of AWRDE. Must be in form Major Revision.Minor Revision. For
            instance, AWRDE version 16.02 would be a version_str value of 16.0
            Default is empty string
    clsid_str: string, optional
           Unique identifier for AWRDE instance. This number can be found using VBA script command
           Debug.Print MWOffice.InstanceCLSID
           Only include the CLSID number in this format:
                5BF3163E-6734-4FB4-891E-FD9E3D4A2CFA
           Do not inlcude brackets: {}
           Default is empty string
    Returns
    -------
    awrde: object variable
    
    Note
    ----
    If only one instance of AWRDE is currently opened then CLSID is not required. CLSID is only required
    to link to a specific opened AWRDE instance
    
    If only one version of AWRDE is currently installed, then version_str is not required
    
    See Also
    --------
    https://kb.awr.com/display/awrscripts/AWR+Scripting+in+Python%3A+Using+the+AWRDE+API+Scripting+Guide
    '''
    
    if not isinstance(version_str, str):
        raise TypeError('version_str must be a string type')
    if not isinstance(clsid_str, str):
        raise TypeError('clsid_str must be a string type')
    #end if
    #
    if version_str == '' and clsid_str == '':
        try:
            awrde = mwo.CMWOffice()
        except:
            raise RuntimeError('Link between Python and AWRDE could not be established')
        #end try
    elif clsid_str != '':
        try:
            awrde = mwo.CMWOffice(clsid='{'+clsid_str+'}')
        except:
            print('CLSID Number: ' + clsid)
            raise RuntimeError('Link between Python and AWRDE using CSLID could not be established')
        #end try
    elif version_str != '':
        try:
            awrde = mwo.CMWOffice(version=version_str)
        except:
            print('Version_str: ' + version_str)
            raise RuntimeError('Link between Python and AWRDE using Version could not be established')
        #end try
    #end if
    return awrde
    #
class Project(_Graphs, _Schematics, _SystemDiagrams, _DataFiles):
    ''' 
    Highest level class in pyawr_utils. User interface to all classes,methods, properties,
    etc. are through the Project class
    
    Parameters
    ----------
    awrde: object variable 
         this variable is returned from awr_utils.establish_link()
    '''
    #
    def __init__(self, awrde):#-----------------------------------------------------------------------
        _Graphs.__init__(self, awrde)
        _Schematics.__init__(self, awrde.Project)
        _SystemDiagrams.__init__(self, awrde)
        _DataFiles.__init__(self, awrde)
        self._options_blacklist()
        self.awrde = awrde
        #
    #
    #----------------------------Project section------------------------------------------
    #
    def save_project(self):#---------------------------------------------------------
        ''' Equivalent to File > Save '''
        try:
            self.awrde.Project.Save()
        except:
            pass #project is already saved
        #end try
        #
    @property
    def project_name(self) -> str:#-------------------------------------------------------
        ''' returns name of currently opened project'''
        return self.awrde.Project.Name
        #
    @property
    def project_path(self) -> str:#------------------------------------------------------
        return self.awrde.Project.Path    
        #
    @property
    def project_frequencies(self) -> np.ndarray:#------------------------------------------------
        '''returns project frequencies in Hz as an array'''
        project_freq_list = list()
        for freq in self.awrde.Project.Frequencies:
            project_freq_list.append(freq.Value)
        #end for
        project_freq_ay = np.array(project_freq_list)        
        return project_freq_ay
        #
    def set_project_frequencies(self, project_freq_ay: np.ndarray, units_str: str = 'GHz'):#-----------------------
        '''sets project frequencies'''
        #Cannot be made as a setter property due to multiple pass parameters
        units_dict = {'Hz':1, 'kHz':1e3, 'MHz':1e6, 'GHz':1e9}
        try:
            freq_multiplier = units_dict[units_str]
        except:
            raise RuntimeError('Incorrect units: ' + units_str)
        #end try
        project_freq_ay *= freq_multiplier
        self.awrde.Project.Frequencies.Clear()  #Remove all existing frequencies
        try:
            self.awrde.Project.Frequencies.AddMultiple(project_freq_ay)  #Add new frequency arrray
        except:
            raise RuntimeError('Error in setting project frequencies')
        #end try
        #
    @property
    def environment_options_dict(self) -> dict:#----------------------------------------------
        '''returns dictionary of options found in Main Menu > Options > Environment Options'''
        env_options = self.awrde.Options
        env_options_dict = {}
        for opt in env_options:
            if opt.Name not in self._env_options_blacklist:
                env_options_dict[opt.Name] = opt.Value
            #end if
        #end for
        return env_options_dict
        #
    def set_environment_options_dict(self, environment_options_dict: dict):#--------------------------
        '''set options found in Main Menu > Options > Environment Options'''
        for opt_name, opt_value in environment_options_dict.items():
            try:
                self.awrde.Options(opt_name).Value = opt_value
            except:
                raise RuntimeError('setting environment options failed: ' + opt_name + ' , ' + str(opt_value))
            #end try
        #end for
        #
    @property
    def project_options_dict(self) -> dict:#---------------------------------------------------------
        '''returns dictionary of options found in Main Menu > Options > Project Options & Layout Options'''
        proj_options = self.awrde.Project.Options
        proj_options_dict = {}
        for opt in proj_options:
            if opt.Name not in self._project_options_blacklist:
                proj_options_dict[opt.Name] = opt.Value
            #end if
        #end for
        return proj_options_dict
        #
    def set_project_options_dict(self, project_options_dict: dict):#--------------------------
        '''set options found in Main Menu > Options > Project Options & Layout Options'''
        for opt_name, opt_value in project_options_dict.items():
            try:
                self.awrde.Project.Options(opt_name).Value = opt_value
            except:
                raise RuntimeError('setting environment options failed: ' + opt_name + ' , ' + str(opt_value))
            #end try
        #end for
        #
    def _options_blacklist(self):#-------------------------------------------------------------------
        ''' lists of option names that cause errors'''
        self._project_options_blacklist = ['FaceInsetOptions']
        self._env_options_blacklist = ['MouseCommandEntryMode']
        #
    #
    #-----------------------------Simulate/Analyze section----------------------------------------
    #
    def simulate_analyze(self, ping_interval = 1, max_time = 120) -> bool:
        '''
        Equivalent to Simulte > Analyze
    
        Parameters
        ----------
        awrde: object
            The AWRDE object returned from EstablishLink()
    
        ping_interval: int, optional
            Wait time in seconds before getting simulation status
            Defaul is 1 second
    
        max_time: int, optional
            Maximum simulation time in seconds
            Default is 120 seconds
    
        Returns
        -------
        measurement_done: bool
            True if simulation has completed
    
        '''
        #
        if not isinstance(ping_interval, int) and not isinstance(ping_interval, float):
            raise TypeError('ping_interval must be type int or float')
        if not isinstance(max_time, int) and not isinstance(max_time, float):
            raise TypeError('max_time must be type int or float')
        # end if
        #    
        measurement_done = False
        elapsed_time = 0
        start_time = tm.time()
        self.awrde.Project.Simulator.Analyze()
        while not measurement_done or elapsed_time>max_time:
            sim_status = self.awrde.Project.Simulator.AnalyzeState
            if sim_status == 3:
                measurement_done = True
            #end if
            tm.sleep(ping_interval)
            elapsed_time = tm.time() - start_time
        #end while
        return measurement_done
        #
    def simulate_run_system_simulator(self, ping_interval = 1, max_time = 120) -> bool:
        '''
        Equivalent to Simulate > Run/Stop System Simulators
        
        Parameters
        ----------
        awrde: object
            The AWRDE object returned from EstablishLink()
            
        ping_interval: int, optional
            Wait time in seconds before getting simulation status
            Defaul is 1 second
            
        max_time: int, optional
            Maximum simulation time in seconds
            Default is 120 seconds
            
        Returns
        -------
        measurement_done: bool
            True if simulation has completed
        
        '''    
        #
        if not isinstance(ping_interval, int) and not isinstance(ping_interval, float):
            raise TypeError('ping_interval must be type int or float')
        if not isinstance(max_time, int) and not isinstance(max_time, float):
            raise TypeError('max_time must be type int or float')
        #end if
        #
        measurement_done = False
        elapsed_time = 0
        start_time = tm.time()
        self.awrde.Project.Simulator.RunStop()
        while (not measurement_done) and (elapsed_time < max_time):
            sim_status = self.awrde.Project.Simulator.state
            if sim_status == 0:
                measurement_done = True
            #end if
            tm.sleep(ping_interval)
            elapsed_time = tm.time() - start_time
        #end while
        return measurement_done
        #
    def stop_system_simulator(self):#---------------------------------------------------
        '''Stops a running system simulation'''
        sim_status = self.awrde.Project.Simulator.state
        if sim_status != 0:  #Stop simulator if still running after maximum time
            self.awrde.Project.Simulator.stop()
        #end if    
        #

    
    