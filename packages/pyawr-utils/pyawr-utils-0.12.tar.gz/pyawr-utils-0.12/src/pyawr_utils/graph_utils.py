import pyawr.mwoffice as mwo
from pyawr_utils import vss_utils, common_utils
from tkinter import messagebox
import warnings
import numpy as np
#
_SystemDiagrams = vss_utils._SystemDiagrams
_ProcessDefinitions = common_utils._ProcessDefinitions
#
#*****************************************************************************
#
class _Graphs():
    '''
    Methods for the collection of Graphs in the AWRDE project
    
    Parameters
    ----------
    awrde: The AWRDE object returned from awrde_utils.establish_link()

    '''    
    def __init__(self, awrde):#-----------------------------------------------------------
        self.awrde = awrde
        self._build_graphs_dict()
        #
    def _build_graphs_dict(self) -> dict:#--------------------------------------------------
        '''Create list of all graph names in project
    
        Parameters
        ----------
        None
    
        Returns
        -------
        graphs_dict: dict[element_objects]
                         Each element in the list is a graph name
        '''
        self._graphs_dict = {}
        for gr in self.awrde.Project.Graphs:
            graph = _Graph(self.awrde, gr.Name)
            self._graphs_dict[graph.graph_name] = graph
        #end for
        #
    @property
    def graph_dict(self) -> dict:#---------------------------------------------------------
        '''returns graph dictionary'''
        self._build_graphs_dict()
        return self._graphs_dict
        #    
    @property
    def graph_name_list(self) -> list[str]:#----------------------------------------------
        '''
        Creates list of all graph names in project
        
        Parameters
        ----------
        None
        
        Returns
        -------
        graph_name_list: list[string]
                   Each item in the list is a graph name
        '''
        graph_name_list = list()
        for gr in self.awrde.Project.Graphs:
            graph_name_list.append(gr.Name)
        #end for
        return graph_name_list
        #
    def add_rectangular_graph(self, graph_name: str) -> object:#-----------------------------
        '''
        Add a rectangular graph
        
        Parameters
        ----------
        graph_name: string,
                 name of the Graph to be added
             
        '''
        self._add_graph(graph_name, 'Rectangular')
        #
    def add_rectangular_real_imag_graph(self, graph_name: str) -> object:
        '''
        Add a Rectangular - Real/Imag graph
        
        Parameters
        ----------
        graph_name: string,
                 name of the Graph to be added
        
        '''
        self._add_graph(graph_name, 'Rect_RealImag')
        #    
    def add_smith_chart_graph(self, graph_name: str) -> object:#-----------------------------
        '''
        Add a Smith Chart graph
        
        Parameters
        ----------
        graph_name: string,
                 name of the Graph to be added
             
        '''
        self._add_graph(graph_name, 'Smith')
        #
    def add_polar_graph(self, graph_name: str) -> object:#------------------------------------
        '''
        Add a Polar graph
        
        Parameters
        ----------
        graph_name: string,
                 name of the Graph to be added
             
        '''
        self._add_graph(graph_name, 'Polar')
        #
    def add_histogram_graph(self, graph_name: str) -> object:#-------------------------------
        '''
        Add a Histogram graph
        
        Parameters
        ----------
        graph_name: string,
                 name of the Graph to be added
             
        '''
        self._add_graph(graph_name, 'Histogram')
        #
    def add_antenna_plot_graph(self, graph_name: str) -> object:#------------------------------
        '''
        Add an Antenna Plot graph
        
        Parameters
        ----------
        graph_name: string,
                 name of the Graph to be added
             
        '''
        self._add_graph(graph_name, 'Antenna')
        #
    def add_tabular_graph(self, graph_name: str) -> object:#---------------------------------
        '''
        Add a Tabular graph
        
        Parameters
        ----------
        graph_name: string,
                 name of the Graph to be added
        
           '''
        self._add_graph(graph_name, 'Tabular')
        #
    def add_constellation_graph(self, graph_name: str) -> object:#-----------------------------
        '''
        Add a Constellation graph
        
        Parameters
        ----------
        graph_name: string,
                 name of the Graph to be added
             
        '''
        self._add_graph(graph_name, 'Constellation')
        #
    def add_3D_graph(self, graph_name: str) -> object: #-------------------------------------
        '''
        Add a 3D graph
        
        Parameters
        ----------
        graph_name: string,
                 name of the Graph to be added
            
        '''
        self._add_graph(graph_name, '3D')
        #    
    def remove_graph(self, graph_name: str) -> bool:#--------------------------------------------
        '''
        Delete a graph from the AWRDE project
        
        Parameters
        ----------
        graph_name: string,
                 name of the Graph to be deleted
        
        Returns
        -------
        graph_removed: bool
                    True if graph successfully deleted, False if graph could not be deleted
                    
        '''
        if not isinstance(graph_name, str):
            raise TypeError('graph_name must be a string type')
        #end if
        graph_removed = False               
        try:
            for gr_idx in range(self.awrde.Project.Graphs.Count):
                if self.awrde.Project.Graphs[gr_idx].Name == graph_name:
                    self.awrde.Project.Graphs.Remove(gr_idx+1)
                    graph_removed = True
                    break
                #end if
            #end for
        except:
            warnings.warn('remove_graph: Graph ' + graph_name + ' did not get removed')
        #end for
        return graph_removed
        #
    def rename_graph(self, graph_name: str, new_graph_name: str):#--------------------
        '''
        rename Graph
    
        Parameters
        ----------
        graph_name: string
                         existing graph name
        new_graph_name: string
                         new graph name
        '''        
        if not isinstance(graph_name, str):
            raise TypeError('graph_name must be a string')
        #end if
        if not isinstance(new_graph_name, str):
            raise TypeError('new_graph_name must be a string')
        #end if
        graph_name_list = self.graph_name_list
        found_it = False
        for graph_name_from_list in graph_name_list:
            if graph_name_from_list == graph_name:
                found_it = True
                if new_graph_name in graph_name_list:
                    YesNo = messagebox.askyesno('Rename Graph','Graph '\
                        + new_graph_name + ' exists. Remove existing Graph ?')
                    if YesNo:
                        self.remove_graph(new_graph_name)
                    else:
                        new_graph_name += ' 1'
                    #end if
                #end if
                try:
                    gr = self.awrde.Project.Graphs(graph_name)
                    gr.Name = new_graph_name
                except:
                    raise RuntimeError('problem with renaming graph')
                #end try
            #end if
        #end for
        if not found_it:
            warnings.warn('graph rename failed: ' + graph_name)
        #end if
        #
    def copy_graph(self, graph_name: str, new_graph_name: str):#-----------------------
        '''
        copy Graph
    
        Parameters
        ----------
        graph_name: string
                         existing graph name
        new_graph_name: string
                         new graph name
        '''
        if not isinstance(graph_name, str):
            raise TypeError('graph_name must be a string')
        #end if
        if not isinstance(new_graph_name, str):
            raise TypeError('new_graph_name must be a string')
        #end if        
        for gr in self.awrde.Project.Graphs:
            if gr.Name == new_graph_name:
                new_graph_name = new_graph_name + ' 1'
            #end if
        #end for
        #
        try:
            for gr_idx in range(1, self.awrde.Project.Graphs.Count+1):
                gr = self.awrde.Project.Graphs(gr_idx)
                if gr.Name == graph_name:
                    self.awrde.Project.Graphs.Copy(gr_idx, new_graph_name)
                    graph_copied = True
                #end if
            #end for
        except:
            raise RuntimeError('problem with copying graph')
        #end try
        #        
    def _does_graph_exist(self, graph_name: str) -> bool:#---------------------------------------
        graph_exists = False
        for gr in self.awrde.Project.Graphs:
            if gr.Name == graph_name:
                graph_exists = True
            #end if
        #end for
        return graph_exists
        #
    def _add_graph(self, graph_name, graph_type):
        if graph_type == 'Rectangular':
            graph_type_enum = mwo.mwGraphType.mwGT_Rectangular
        elif graph_type == 'Rect_RealImag':
            graph_type_enum = mwo.mwGraphType.mwGT_RectangularComplex
        elif graph_type == 'Smith':
            graph_type_enum = mwo.mwGraphType.mwGT_SmithChart
        elif graph_type == 'Polar':
            graph_type_enum = mwo.mwGraphType.mwGT_Polar
        elif graph_type == 'Histogram':
            graph_type_enum = mwo.mwGraphType.mwGT_Histogram
        elif graph_type == 'Antenna':
            graph_type_enum = mwo.mwGraphType.mwGT_Antenna
        elif graph_type == 'Tabular':
            graph_type_enum = mwo.mwGraphType.mwGT_Tabular
        elif graph_type == 'Constellation':
            graph_type_enum = mwo.mwGraphType.mwGT_Constellation
        elif graph_type == '3D':
            graph_type_enum = mwo.mwGraphType.mwGT_ThreeDim
        else:
            raise RuntimeError(graph_type + ' not recognized')
        #end if
        #
        if type(graph_name) != str:
            raise RuntimeError('graph_name must be a string type')
        #end if
        if self._does_graph_exist(graph_name):
            YesNo = messagebox.askyesno('AddGraph','Graph ' + graph_name + ' exists. Delete existing Graph?')
            if YesNo:
                self.remove_graph(graph_name)
            #end if
        #end if
        #
        self.awrde.Project.Graphs.Add(graph_name, graph_type_enum)       
        #    

#
#*****************************************************************************
#
class _Measurements():
    '''
    Methods for collection of measurements within a graph
    
    Parameters
    ----------
    awrde: object variable
         The AWRDE object returned from awrde_utils.establish_link()
    
    graph_name: string
         Name of the graph that the measurement belongs to
         
    built_dict: bool, optional
           dtermines whether _build_measurements_dict() is run at initialization
    '''    
    def __init__(self, awrde, graph_name: str):#---------------------------
        self.awrde = awrde
        self._initialize_mesaurements(graph_name)
        self._build_measurements_dict()
        #
    def _initialize_mesaurements(self, graph_name):#-------------------------------------
        if not isinstance(graph_name, str):
            raise TypeError('graph_name must be a string')
        #end if
        try:
            self._gr = self.awrde.Project.Graphs(graph_name)
        except:
            raise RuntimeError('Graph not recognized ' + graph_name)
        #end try
        self._graph_name = graph_name
        #
    def _build_measurements_dict(self):#--------------------------------------------------------
        '''
        creates a dictionary of measurements in a graph
        '''
        self._graphs_dict = {}
        meas_idx = 0
        for meas in self._gr.Measurements:
            measurement = _Measurement(self.awrde, self._gr.Name, meas.Name)
            self._graphs_dict[meas_idx] = measurement
            meas_idx += 1
        #end for
        #
    @property
    def measurements_dict(self) -> dict:#---------------------------------------------------
        '''returns measurements dictionary'''
        self._build_measurements_dict()
        return self._graphs_dict
        #
    @property
    def measurement_name_list(self) -> list[str]:#-----------------------------------------
        '''Returns list of measurement names in the graph'''
        measurement_name_list = list()
        for meas in self._gr.Measurements:
            measurement_name_list.append(meas.Name)
        #end for
        return measurement_name_list
        #
    def add_measurement(self, source_doc: str, measurement: str):#------------------------
        '''
        Add measurement to graph
        
        Parameters
        ----------
        Source Doc: string
                name of the source document: Circuit schematic name, Systeme diagram name,
                Data File name, EM doc name
        measurement: string
                The measurement as a string
        '''
        try:
            self._gr.Measurements.Add(source_doc, measurement)
        except:
            raise RuntimeError('Invalid measurement add: ' + source_doc + ' , ' + measurement)
        #end try
        #
    def remove_measurement(self, measurement_name: str) -> bool:#-----------------------------
        '''
        Delete a measurement from the graph
        
        Parameters
        ----------
        measurement_name: string
              The measurement name in format source_doc:measurement
              
        Returns
        -------
        measurement_removed: bool
              True if measurement successfully removed
        '''
        measurement_removed = False
        try:
            if self._gr.Measurements.Exists(measurement_name):
                self._gr.Measurements.Remove(measurement_name)
                measurement_removed = True
            #end if
        except:
            measurement_removed = False
            warnings.warn('remove_measurement: measurement ' + measurement_name + ' did not get removed')
        #end try
        return measurement_removed
        #    
#
#*****************************************************************************
#
class _Measurement(_ProcessDefinitions):
    '''
    Methods for an individulal measurement within a graph
    
    Parameters
    ----------
    awrde: object variable
         The AWRDE object returned from awrde_utils.establish_link() 
    graph_name: string
         Name of the graph that the measurement belongs to
    measurement_name: string
         Full name of the measurement
    
    '''    
    def __init__(self, awrde, graph_name: str, measurement_name: str):#---------------------------------------
        self.awrde = awrde
        _ProcessDefinitions.__init__(self, awrde)
        self._initialize_measurement(graph_name, measurement_name)
        #
    def _initialize_measurement(self, graph_name, measurement_name):#---------------------------------
        try:
            self._gr = self.awrde.Project.Graphs(graph_name)
        except:
            raise RuntimeError('Graph does not exist: ' + graph_name)
        #end try
        #
        try:
            self._meas = self._gr.Measurements(measurement_name)
        except:
            raise RuntimeError(measurement_name + ' does not exist')
        #end try
        #
    @property
    def measurement_name(self) -> str:#-----------------------------------------------------
        '''Returns name of measurement'''
        return self._meas.Name
        #
    @property
    def measurement_enabled(self) -> bool:#---------------------------------------
        return self._meas.Enabled
        #
    @measurement_enabled.setter
    def measurement_enabled(self, enabled_state: bool):#----------------------------
        self._meas.Enabled = enabled_state
        #
    @property
    def measurement_axis(self):#----------------------------------------------------------
        return self._meas.AxisIndex, self._meas.OnLeftAxis
        #
    def set_measurement_axis(self, axis_index: int, on_left_axis: bool):#-------------------
        if not isinstance(axis_index, int):
            raise TypeError('axis_index must by type int')
        #end if
        if not isinstance(on_left_axis, bool):
            raise TypeError('on_left_axis must be type boolean')
        #end if
        try:
            self._meas.AxisIndex = axis_index
        except:
            raise RuntimeError('problem with setting axis index')
        #end try
        self._meas.OnLeftAxis = on_left_axis
        #
    @property
    def num_traces(self) -> int:#--------------------------------------------------
        ''' Returns number of traces in measurement'''
        return self._meas.TraceCount
        #
    @property
    def trace_data(self) -> list[np.ndarray]:#------------------------------------
        '''
        Returns a list of arrays. Each array corresponds to a measurement trace
        
        '''
        trace_data_list = list()
        if self.measurement_enabled:
            NumTraces = self.num_traces
            for trace_idx in range(1, NumTraces+1):
                trace_data_tuple = self._meas.TraceValues(trace_idx) #returns tuple
                trace_data_ay = np.asarray(trace_data_tuple) #convert tuple into array
                trace_data_list.append(trace_data_ay)
            #end for
            #
            trace_data_list = self._cleanup_vss_spectrum(trace_data_list)
            trace_data_list = self._scale_trace_data_to_project_units(trace_data_list)
        #end if
        #
        return trace_data_list
        #
    @property
    def sweep_var_labels(self) -> list:#-----------------------------------------------
        '''returns list of sweep variables'''
        sweep_param_dict = self._sweep_parameters
        sweep_var_list = list()
        for sweep_var_name in sweep_param_dict['SWPVAR Labels']:
            sweep_var_list.append(sweep_var_name)
        #end for
        return sweep_var_list
        #
    @property
    def sweep_var_trace_info(self) -> list:#--------------------------------------------
        '''returns list. Each list is a dictionary of sweep var parameters for each trace'''
        sweep_param_dict = self._sweep_parameters
        return sweep_param_dict['Trace Information']
        #
    @property
    def _sweep_parameters(self) -> dict:#-------------------------------------------------
        '''
        returns dictionary of SWPVAR items
        
        Returns
        -------
        sweep_param_dict: dictionary
               "Num SWPVARs" : Number of SWPVAR blocks detected
               "SWPVAR Labels" : list of strings. Each element is the sweep variable name
               "Trace Information" : list of dictionary of SWPVAR label:value for each trace.
        '''
        sweep_param_dict = {}
        num_traces = self.num_traces
        num_swpvars = self._meas.SweepLabels(1).Count
        sweep_param_dict['Num SWPVARs'] = num_swpvars
        #
        if num_swpvars > 0:
            swpvar_lbls_list = list()
            for lbl_idx in range(1, num_swpvars+1):
                swpvar_lbl = self._meas.SweepLabels(1).Item(lbl_idx).Name
                swpvar_lbls_list.append(swpvar_lbl)
            #end for
            sweep_param_dict['SWPVAR Labels'] = swpvar_lbls_list
            #
            trace_info_list = list()
            for trace_idx in range(1, num_traces+1):
                Trace_info_dict = {}
                for swpvar_idx in range(1, num_swpvars+1):
                    swpvar_name = self._meas.SweepLabels(trace_idx).Item(swpvar_idx).Name
                    swpvar_val = self._meas.SweepLabels(trace_idx).Item(swpvar_idx).Value
                    Trace_info_dict[swpvar_name] = swpvar_val
                #end for
                trace_info_list.append(Trace_info_dict)
            #end for
            sweep_param_dict['Trace Information'] = trace_info_list
            #
        else:
            sweep_param_dict['SWPVAR Labels'] = []
            sweep_param_dict['Trace Information'] = []
        #end if
        #
        return sweep_param_dict
        #
    def _scale_trace_data_to_project_units(self, trace_data_list: list) -> list:#-------------------------------
        '''
        measurement trace data read back in base units.
        This routine scales the data to project units.
        '''
        source_doc = self._meas.Source
        source_doc_type = self._source_doc_type(source_doc)
        if source_doc_type == 'Circuit Schematic':
            schem = self.awrde.Project.Schematics(source_doc)
            lpf_name = schem.ProcessDefinition
        elif source_doc_type == 'System Diagram':
            sys_diags = SystemDiagrams(self.awrde)
            lpf_name = sys_diags.Which_LPF
        #end if
        lpf_units_dict = self._project_units(lpf_name)
        #
        for axis_idx in range(2): #0=Xaxis, 1=Yaxis
            unit_type_enum = self._meas.UnitType(axis_idx+1)
            unit_type_str = self._unit_type_str(unit_type_enum)
            unit_string = lpf_units_dict[unit_type_str]
            #
            unit_scale_factor_dict = self._unit_scale_factor(unit_type_str, unit_string)
            offset1 = unit_scale_factor_dict['Offset1']
            offset2 = unit_scale_factor_dict['Offset2']
            multiplier = unit_scale_factor_dict['Multiplier']
            for trace_idx in range(len(trace_data_list)):
                trace_data_ay = trace_data_list[trace_idx]
                trace_data_ay[:,axis_idx] = (trace_data_ay[:,axis_idx] + offset2)*multiplier + offset1
                trace_data_list[trace_idx] = trace_data_ay
            #end for
        #end for
        return trace_data_list
        #
    def _cleanup_vss_spectrum(self, trace_data_list: list) -> list[np.ndarray]:#---------------------
        '''
        VSS time domain spectrum's last data point is some unusually large value.
        This routine strips off the last data point
        '''
        valid_cleanup_measurement = False
        measurement_type = self._meas.Type
        if 'V_SPEC' in measurement_type and (not 'RFI' in measurement_type):
            valid_cleanup_measurement = True
        elif ('PWR_SPEC' in measurement_type) and (not 'RFI' in measurement_type):
            valid_cleanup_measurement = True
        #end if
        #
        if valid_cleanup_measurement:
            temp_trace_data_list = copy.deepcopy(trace_data_list)
            trace_data_list = list()
            NumTraces = len(temp_trace_data_list)
            for trace_idx in range(NumTraces):
                trace_data_ay = temp_trace_data_list[trace_idx]
                trace_data_ay = trace_data_ay[:-1] #Remove last data point
                trace_data_list.append(trace_data_ay)
            #end for
        #end if
        return trace_data_list
        #
    def _source_doc_type(self, source_doc: str) -> str:#------------------------------------------------------
        ''' returns Source document type: System Diagram, Circuit Schematic'''
        source_doc_type = ''
        
        system_diags = _SystemDiagrams(self.awrde)
        system_diagram_name_list = system_diags.system_diagram_name_list
        #
        schematic_diagram_list = list()
        for schem in self.awrde.Project.Schematics:
            schematic_diagram_list.append(schem.Name)
        #end 
        #
        if source_doc in system_diagram_name_list:
            source_doc_type = 'System Diagram'
        elif source_doc in schematic_diagram_list:
            source_doc_type = 'Circuit Schematic'
        #end if
        return source_doc_type
        #
        
#
#*****************************************************************************
#
class _Axes():
    ''' 
    methods for all axes in the graph
    
    Parameters
    ----------
    awrde: object variable
         The AWRDE object returned from awrde_utils.establish_link() 
    
    graph_name: string
    
    '''
    def __init__(self, awrde, graph_name: str):#---------------------
        self.awrde = awrde
        self._initialize_axes(graph_name)
        self._build_axes_dict()
        #
    def _initialize_axes(self, graph_name):#------------------------------
        try:
            self._gr = self.awrde.Project.Graphs(graph_name)
        except:
            raise RuntimeError('Graph does not exist: ' + graph_name)
        #end try
        self._graph_name = graph_name
        #
    def _build_axes_dict(self):#-----------------------------------------
        ''' creates a dictionary of all the axes in the graph'''
        num_axes = self._gr.Axes.Count
        self._axes_dict = {}
        for ax_idx in range(1, num_axes+1):
            axis = _Axis(self.awrde, self._graph_name, ax_idx)
            self._axes_dict[axis.axis_name] = axis
        #end for
        #
    @property
    def axes_dict(self) -> dict:#-----------------------------------------
        '''returns axes dictionary'''
        return self._axes_dict
        #
    @property
    def axes_name_list(self) -> list:
        '''returns list of the axes names'''
        axes_name_list = list()
        for ax in self._gr.Axes:
            axes_name_list.append(ax.Name)
        #end for
        return axes_name_list
        #
#
#*****************************************************************************
#
class _Axis():
    '''
    Methods for an individulal measurement within a graph
    
    Parameters
    ----------
    awrde: object variable
         The AWRDE object returned from awrde_utils.establish_link()
    graph_name: string
         Name of the graph that the measurement belongs to
    axis_index: int
    '''
    def __init__(self, awrde, graph_name: str, axis_index: int):#-------------------
        self.awrde = awrde
        self._initialize_axis(graph_name, axis_index)
        #
    def _initialize_axis(self, graph_name, axis_index):#------------------------------
        if not isinstance(axis_index, int):
            raise TypeError('axis_index must be int type')
        #end if
        try:
            self._gr = self.awrde.Project.Graphs(graph_name)
        except:
            raise RuntimeError('Graph does not exist: ' + graph_name)
        #end try
        try:
            self._axis = self._gr.Axes(axis_index)
        except:
            raise RuntimeError('could not acces axis. Axis index='+str(axis_index))
        #end try
        #
    @property
    def axis_name(self) -> str: #---------------------------------------
        '''returns name of the axis'''
        return self._axis.Name
        #
    @property
    def axis_auto_scale(self) -> bool:#-------------------------------------------------------------
        return self._axis.AutoScale
        #
    @axis_auto_scale.setter
    def axis_auto_scale(self, auto_scale: bool):#------------------------------------------------
        if not isinstance(auto_scale, bool):
            raise TypeError('auto_scale must be boolean type')
        #end if
        self._axis.AutoScale = auto_scale
        #
    @property
    def axis_minimum_scale(self) -> float:#--------------------------------------------------
        return self._axis.MinimumScale
        #
    @axis_minimum_scale.setter
    def axis_minimum_scale(self, min_scale_val: float):#------------------------------------------
        self._axis.MinimumScale = min_scale_val
        #
    @property
    def axis_maximum_scale(self) -> float:#--------------------------------------------------
        return self._axis.MaximumScale
        #
    @axis_maximum_scale.setter
    def axis_maximum_scale(self, max_scale_val: float):#------------------------------------------
        self._axis.MaximumScale = max_scale_val
        #
    @property
    def axis_grid_step(self) -> float:#--------------------------------------------------------
        return self._axis.MajorGridlinesStep
        #
    @axis_grid_step.setter
    def axis_grid_step(self, step_size: float):#-------------------------------------------------
        self._axis.MajorGridlinesStep = step_size    
#
#*****************************************************************************
#
class _Markers():
    '''
    Methods for markers within a graph
    
    Parameters
    ----------
    awrde: object variable
         The AWRDE object returned from awrde_utils.establish_link() 
    graph_name: string
         Name of the graph that the measurement belongs to
    '''    
    def __init__(self, awrde, graph_name: str):#--------------------------------------------
        self.awrde = awrde
        self._initialize_markers(graph_name)
        self._build_markers_dict()
        #
    def _initialize_markers(self, graph_name):#---------------------------------------------
        try:
            self._gr = self.awrde.Project.Graphs(graph_name)
        except:
            raise RuntimeError('Graph does not exist: ' + graph_name)
        #end try
        self._graph_name = graph_name
        #
    def _build_markers_dict(self):#-------------------------------------------------
        '''creates a dictionary of all the markers in the graph'''
        self._markers_dict = {}
        marker_idx = 0
        for marker in self._gr.Markers:
            marker = _Marker(self.awrde, self._graph_name, marker.Name)
            self._markers_dict[marker_idx] = marker
            marker_idx += 1
        #end for
        #
    @property
    def markers_dict(self) -> dict:#-------------------------------------------
        '''returns markers dictionary'''
        self._build_markers_dict()
        return self._markers_dict
        #
    @property
    def marker_name_list(self) -> list[str]:#--------------------------------------------------
        '''
        Creates list of all the marker names in the graph
        
        Returns
        -------
        marker_name_list: list[string]
                  Each item in the list is a marker name
        '''
        marker_name_list = list()
        for mkr in self._gr.Markers:
            marker_name_list.append(mkr.Name)
        #end for
        return marker_name_list
        #
    @property
    def remove_all_markers(self):#-----------------------------------------------------------
        self._gr.Markers.RemoveAll()
        #
    def remove_marker(self, marker_name: str) -> bool:#--------------------------------------
        marker_removed = False
        try:
            for mkr_idx in range(1, self._gr.Markers.Count+1):
                if self._gr.Markers(mkr_idx).Name == marker_name:
                    self._gr.Markers.Remove(mkr_idx)
                    marker_removed = True
                    break
                #end if
            #end if
        except:
            warnings.warn('Could not remove marker')
        #end try
        return marker_removed
        #
    def add_marker(self, measurement: str, sweep_value, trace_index: int=0):#---------
        if not isinstance(measurement, str):
            raise TypeError('measurement must be string type')
        #end if
        if not isinstance(sweep_value, float) and not isinstance(sweep_value,int):
            raise TypeError('sweep_value must be int or float type')
        #
        if not isinstance(trace_index, int):
            raise TypeError('trace_index must be int type')
        #end
        try:
            self._gr.Markers.AddEx(measurement, 1, sweep_value, trace_index + 1)
        except:
            raise RuntimeError('Could not add marker to graph')
        #end if
        #      
#
#*****************************************************************************
#
class _Marker():
    '''
    Methods for an dividual marker
    
    Parameters
    ----------
    awrde: object variable
         The AWRDE object returned from awrde_utils.establish_link() 
    graph_name: string
         Name of the graph that the measurement belongs to
    marker_name: string
    '''        
    def __init__(self, awrde, graph_name, marker_name):#----------------------------------------
        self.awrde = awrde
        self._initialize_marker(graph_name, marker_name)
        #
    def _initialize_marker(self, graph_name, marker_name):#---------------------------------
        try:
            self._gr = self.awrde.Project.Graphs(graph_name)
        except:
            raise RuntimeError('Graph does not exist: ' + graph_name)
        #end try
        #
        try:
            self._mkr = self._gr.Markers(marker_name)
        except:
            raise RuntimeError('marker not recognized: ', marker_name)
        #end try
        #       
    @property
    def marker_name(self) -> str:#----------------------------------------------------------------
        return self._mkr.Name     
        #
    @property
    def marker_measurement(self) -> str:#----------------------------------------------------------
        return self._mkr.Measurement
        #
    @property
    def marker_data_text(self) -> str:#--------------------------------------------------------
        return self._mkr.DataValueText
        #
    @property
    def marker_data_value_x(self) -> float:#----------------------------------------------------
        return self._mkr.DataValue(1)
        #
    @property
    def marker_data_value_y1(self) -> float:#----------------------------------------------------
        return self._mkr.DataValue(2)
        #    
    @property
    def marker_data_value_y2(self) -> float:#----------------------------------------------------
        try:
            mkr_data_value = self._mkr.DataValue(3)
        except:
            raise RuntimeError('marker Y2 invalid')
        #end try
        return mkr_data_value
        #
    @property
    def marker_sweep_value(self) -> float:#-------------------------------------------------------
        return self._mkr.SweepValue
        #
    @marker_sweep_value.setter
    def marker_sweep_value(self, x_axis_value: float):#----------------------------------------------
        self._mkr.SweepValue = x_axis_value
        #
    @property
    def trace_index(self) -> int:#-----------------------------------------------------------
        #0 base indexing
        return int(self._mkr.TraceIndex - 1)
        #
    @trace_index.setter
    def trace_index(self, trace_index: int):#-----------------------------------------------
        try:
            self._mkr.TraceIndex =  trace_index + 1
        except:
            pass #let it lie
        #end try
        #
    @property
    def marker_to_max(self):#-----------------------------------------------------------------
        self._mkr.MoveToMaximum()
        #
    @property
    def marker_to_min(self):#-----------------------------------------------------------------
        self._mkr.MoveToMinimum()
        #
    
#
#*****************************************************************************
#
class _Graph(_Measurements, _Axes, _Markers):
    '''
    Methods for an individual graph in the AWRDE project
    
    Parameters
    ----------
    awrde: object variable
         The AWRDE object returned from awrde_utils.establish_link()
    
    Graph name: string
          name of an existing graph in the AWRDE project
    
    '''
    def __init__(self, awrde, graph_name: str):#---------------------------------------------
        self.awrde = awrde
        _Axes.__init__(self, awrde, graph_name)
        _Measurements.__init__(self, awrde, graph_name)
        _Markers.__init__(self, awrde, graph_name)
        self._initialize_graph(graph_name)
        #
    def _initialize_graph(self, graph_name):#-------------------------------------------------------
        try:
            self._gr = self.awrde.Project.Graphs(graph_name)
        except:
            raise RuntimeError('Graph does not exist: ' + graph_name)
        #end try
        #
    @property
    def graph_name(self) -> str:#----------------------------------------------------------------
        '''Returns name of Graph'''
        return self._gr.Name
        #
    @property
    def graph_type(self) -> str: #----------------------------------------------------------
        '''
        Reports graph type 
        
        Returns
        -------
        graph_type_str: string
              Rectangular, Rectangular-Real/Imag, Smith Chart, Polar, Histogram, Antenna Plot,
              Tabular, Constellation, 3D Plot
        
        '''
        graph_type_enum = self._gr.Type
        if mwo.mwGraphType(graph_type_enum) == mwo.mwGraphType.mwGT_Rectangular:
            graph_type_str = 'Rectangular'
        elif graph_type_enum == mwo.mwGraphType.mwGT_RectangularComplex:
            graph_type_str = 'Rectangular-Real/Imag'
        elif mwo.mwGraphType(graph_type_enum) == mwo.mwGraphType.mwGT_SmithChart:
            graph_type_str = 'Smith Chart'
        elif graph_type_enum == mwo.mwGraphType.mwGT_Polar:
            graph_type_str = 'Polar'
        elif mwo.mwGraphType(graph_type_enum) == mwo.mwGraphType.mwGT_Histogram:
            graph_type_str = 'Histogram'
        elif mwo.mwGraphType(graph_type_enum) == mwo.mwGraphType.mwGT_Antenna:
            graph_type_str = 'Antenna Plot'
        elif mwo.mwGraphType(graph_type_enum) == mwo.mwGraphType.mwGT_Tabular:
            graph_type_str = 'Tabular'
        elif mwo.mwGraphType(graph_type_enum) == mwo.mwGraphType.mwGT_Constellation:
            graph_type_str = 'Constellation'
        elif mwo.mwGraphType(graph_type_enum) == mwo.mwGraphType.mwGT_ThreeDim:
            graph_type_str = '3D Plot'
        else:
            warnings.warn('Graph Type cannot be determined')
            graph_type_str = '???'
        #end if
        return graph_type_str
        #
    def freeze_traces(self, freeze_traces: bool):#-----------------------------------------------------------------
        '''Sets Freeze Traces or Clear Frozen'''
        if not isinstance(freeze_traces,bool):
            raise TypeError('freeze_trace_cmd must be boolean')
        #end if
        if freeze_traces == True:
            self._gr.FreezeTraces()
        else:
            self._gr.ClearFrozenTraces()
        #end if
        #       