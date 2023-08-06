import pyawr.mwoffice as mwo
import numpy as np
from tkinter import messagebox
import warnings
#
#*****************************************************************************
#
class _Parameter():

    def __init__(self, parameter, document_type):
        self._parameter = parameter
        self._document_type = document_type

    @property
    def name(self):
        return self._parameter.Name

    @property
    def value(self):
        if self._document_type == 'System':
            raise RuntimeError('Only value_str is valid for System Diagram element parameters')
        #end if
        return self._parameter.ValueAsDouble

    @value.setter
    def value(self, value):
        if not isinstance(value, float) or not isinstance(value, int):
            raise RuntimeError('value must be float or int type')
        #end if        
        if self._document_type == 'System':
            raise RuntimeError('Only value_str is valid for System Diagram element parameters')
        #end if
        self._parameter.ValueAsDouble = value

    @property
    def value_str(self):
        return self._parameter.ValueAsString

    @value_str.setter
    def value_str(self, value_str: str):
        if not isinstance(value_str, str):
            raise RuntimeError('value_str must be string type')
        #end if
        self._parameter.ValueAsString = value_str


class _Parameters():
    def __init__(self, element, document_type):
        self._element = element
        self._document_type = document_type

    def _build_parameters_dict(self):
        self._parameters_dict = {}

        for parameter in self._element.Parameters:
            try:
                self._parameters_dict[parameter.Name] = _Parameter(self._element.Parameters(parameter.Name), self._document_type)
            except:
                raise RunetimeError('Failed to create dictionary of Parameters')
    
    @property
    def parameters_dict(self):
        '''
        I made this a getter with the @property decorator to keep this consistent with _Elements
        and _Equations. mainclean.py will error out on schem_LPF_C1_parameters = schem_LPF_C1.parameters_dict()
        '''
        self._build_parameters_dict()
        return self._parameters_dict
    
    @property
    def parameter_names_list(self) -> list[str]:#----------------------------------------------------
        '''
        creates a list of element names of all the elements in the document
        
        Parameters
        ----------
        None
        
        Returns
        -------
        param_list: list[string]
                   Each item in the list is parameter name
        '''        
        param_list = list()
        for parameter in self._element.Parameters:
            param_list.append(parameter.Name)

        return param_list

#
#**********************************************************************************************
#
class _Elements():
    def __init__(self, document, document_type):
        self._document = document
        self._document_type = document_type
        self._build_elements_dict()

    def _build_elements_dict(self):
        self._elements_dict = {}
        for element in self._document.Elements:
            try:
                self._elements_dict[element.Name] = _Element(self._document.Elements(element.Name), self._document_type)
            except:
                raise RuntimeError('Failed to create dictionary of Elements')

    @property
    def elements_dict(self) -> dict:
        return self._elements_dict
    
    @property
    def element_names_list(self) -> list[str]:#------------------------------------------
        '''
        creates a list of element names of all the elements in the document
        
        Parameters
        ----------
        None
        
        Returns
        -------
        elements_list: list[string]
                   Each item in the list is an element name
        '''
        elements_list = list()
        for element in self._document.Elements:
            elements_list.append(element.Name)

        return elements_list

    def add_element(self, element_name, x_pos: float, y_pos: float, rotation: float=0, flipped: bool=False):

        #TODO!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #
        '''
        Add an element to the document
        
        Parameters
        ----------
        element_name: string,
                 name of the element to be added. 
        x_pos: float
        y_pos: float
        rotation: float, optional
                 default = 0
        flipped: bool, optional
                 default = False
                 
        Returns
        -------
        none
                    
        '''          
        pass
        #
    def remove_element(self, element_name_n_id: str) -> bool:#-----------------------------------------
        #
        #TODO!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #
        '''
        Delete an element from the document
        
        Parameters
        ----------
        element_name_n_id: string,
                 name of the element to be deleted. Must include ID
                 Format:  element_Name.element_ID. For instance: 'CAP.C1'
        
        Returns
        -------
        element_removed: bool
                    True if element successfully deleted
                    False if element could not be deleted
                    
        '''          
        pass
        #
#
#**********************************************************************************************
#
class _Element(_Parameters):
    def __init__(self, element, document_type):
        _Parameters.__init__(self, element, document_type)
        self._element = element
        self._document_type = document_type
        #
    def set_optimization(self, optimization_bounds: np.ndarray ) -> bool:
        pass
#
#**********************************************************************************************
#
class _Equations():
    '''
    methods for equations
    
    Parameters
    ----------    
    document: object
          schematic, system diagram or output equation documement object variable       
    '''
    def __init__(self, document):#----------------------------
        self._eqns_doc = document
        self._eqns_document_name = self._eqns_doc.Name
        self._build_equations_dict()
        #
    def _build_equations_dict(self):#--------------------------------------------------
        '''
        creates dictionary of equation names whose value is the variable type
        '''
        self._equations_dict = {}
        eqn_idx = 0
        for eqn in self._eqns_doc.Equations:
            equation = _Equation(eqn.Expression, self._eqns_doc)
            self._equations_dict[eqn_idx] = equation
            eqn_idx += 1
        #end for
        #
    @property
    def equations_dict(self) -> dict: #----------------------------------------------
        '''
        returns dictionary of equations. Key is the equaion name, vaue is the 
        equaiton value
        '''
        self._build_equations_dict()
        try:
            return self._equations_dict
        except:
            raise RuntimeError('equations_dict not available')
        #end try
        #
    @property
    def expression_list(self) -> list[str]:#-----------------------------------------
        '''
        Creates list of all expression in the document
        
        Parameters
        ----------
        None
        
        Returns
        -------
        expression_list: list[string]
                   Each item in the list is an expression in the document
        '''        
        expression_list = list()
        for eqn in self._eqns_doc.Equations:
            expression_list.append(eqn.Expression)
        #end for
        return expression_list
        #
    def remove_equation(self, expression: str):#----------------------------------
        '''
        Remove equation from system diagram
        
        Parameters
        ----------
        expression: string
        
        Returns
        -------
        equation_removed: boolean
        '''        
        if not isinstance(expression, str):
            raise TypeError('expression must be a string')
        #end if
        equation_removed = False
        for eqn_idx in range(1, self._eqns_doc.Equations.Count+1):
            eqn_expression = self._eqns_doc.Equations(eqn_idx).Expression
            if eqn_expression == expression:
                self._eqns_doc.Equations.Remove(eqn_idx)
                equation_removed = True
                break
            #end if
        #end for
        if not equation_removed:
            warnings.warn('equations did not get removed')
        #end if
        return equation_removed
        #
    def add_equation(self, equation_name: str, variable_type: str, equation_value, x_pos: float, y_pos: float):
        '''
        Add equation to system diagram
        
        Parameters
        ----------
        equation_name: string
        variable_type: string
                 Valid stings: Variable definition, Parameter definition, Display value
        equation_value: string, int or float
        x_pos: float
        y_pos: float
        '''        
        if not isinstance(equation_name, str):
            raise TypeError('equation_name must be a string')
        if not isinstance(variable_type, str):
            raise TypeError('variable_type must be a sting')
        #end if
        #
        if isinstance(equation_value, int) or isinstance(equation_value, float):
            equation_value = str(equation_value)
        elif not isinstance(equation_value, str):
            raise TypeError('equation_value type must be str, float or int')
        #end if        
        #
        equation_name = equation_name.lstrip() #Remove leading blanks
        equation_name = equation_name.rstrip() #Remove trialing blanks
        #
        equation_value = equation_value.lstrip() #Remove leading blanks
        equation_value = equation_value.rstrip() #Remove trialing blanks
        #
        variable_type = variable_type.lstrip()
        variable_type = variable_type.rstrip()
        variable_type_list = ['Variable definition', 'Parameter definition', 'Display value']
        found_it = False
        for i in range(len(variable_type_list)):
            var_type_from_list = variable_type_list[i]
            if variable_type.lower() == var_type_from_list.lower():
                variable_type = variable_type_list[i]
                found_it = True
                break
            #end if
        #end for
        if not found_it:
            raise RuntimeError('variable_type ' + variable_type + 'not recognized')
        #end if
        variable_sign_dict = {'Variable definition':' = ', 'Parameter definition':' << ', 'Display value':':'}
        variable_sign = variable_sign_dict[variable_type]
        #
        if variable_type == 'Display value':
            equation_str = equation_name + variable_sign
        else:
            equation_str = equation_name + variable_sign + equation_value
        #end if
        #
        expression_list = self.expression_list
        if equation_str in expression_list:
            YesNo = messagebox.askyesno('Add Equation','Equation ' + equation_str + ' exists. Remove existing equation ?')
            if YesNo:
                self.remove_equation(equation_str)
            #end if
        #end if
        #
        try:
            self._eqns_doc.Equations.Add2(equation_str, x_pos, y_pos)
        except:
            raise RuntimeError('Could not add equation')
        #end try
        #
#
#**********************************************************************************************
#
class _Equation():
    '''
    Operations on a single equation
    
    Parameters
    ----------
    expression: str
           Expression is the term used for the string associated with the equation. Must be in the form:
           "x = 2", "x << 2" or "x:"
            
    document: object
          schematic, system diagram or output equation documement object variable 
    '''
    def __init__(self, expression: str, document: object):
        self._initialize_equation(document, expression)
        #
    def _initialize_equation(self, document: object, expression: str):#------------------------------
        self._eqn_doc = document
        self._equation_name, self._equation_value = self._split_expression(expression)
        self._variable_type = self._determine_variable_type(expression)
        self._expression = expression
        self._eqn_index = self._determine_eqn_index()
        #
    @property
    def equation_name(self) -> str: #------------------------------------------
        '''returns equation name'''
        return self._equation_name
        #
    @equation_name.setter
    def equation_name(self, equation_name: str):
        '''modify equation name'''
        if not isinstance(equation_name, str):
            raise TypeError('equation_name must be string type')
        #end if
        self._equation_name = equation_name
        self._update_equation()
        #
    @property
    def equation_value(self) -> str:#--------------------------------------------
        ''' returns equation value as string'''
        return self._equation_value
        #
    @equation_value.setter
    def equation_value(self, equation_value):#-----------------------------
        ''' set equation value'''
        if isinstance(equation_value, int) or isinstance(equation_value, float):
            equation_value = str(equation_value)
        elif not isinstance(equation_value, str):
            raise TypeError('equation_value type must be str, float or int')
        #end if
        self._equation_value = equation_value
        self._update_equation()
        #
    @property
    def variable_type(self) -> str:#------------------------------------------------
        '''returns variable type: Variable definition, Parameter definition, Display value'''
        return self._variable_type
        #
    @variable_type.setter
    def variable_type(self, variable_type: str):#------------------------------------
        '''sets the variable type'''
        variable_type_list = ['Variable definition', 'Parameter definition', 'Display value']
        found_it = False
        for i in range(len(variable_type_list)):
            var_type_from_list = variable_type_list[i]
            if variable_type.lower() == var_type_from_list.lower():
                self._variable_type = variable_type_list[i]
                self._update_equation()
                found_it = True
                break
            #end if
        #end for
        #
        if not found_it:
            raise RuntimeError('variable_type ' + variable_type + 'not recognized')
        #end if
        #
    @property
    def expression(self) -> str:#--------------------------------------------------
        ''' returns expression'''
        return self._expression
        #
    @property
    def xy_position(self) -> tuple:#-------------------------------------------------
        x_position = self._eqn_doc.Equations(self._eqn_index).x
        y_position = self._eqn_doc.Equations(self._eqn_index).y
        xy_position_tuple = (x_position, y_position)
        return xy_position_tuple
        #
    def set_xy_position(self, xy_position_tuple: tuple):#------------------------------
        '''set xy position'''
        self._eqn_doc.Equations(self._eqn_index).x = xy_position_tuple[0]
        self._eqn_doc.Equations(self._eqn_index).y = xy_position_tuple[1]
        #
    def _update_equation(self):#---------------------------------------------------------
        '''write equation to AWR document'''
        variable_sign_dict = {'Variable definition':' = ', 'Parameter definition':' << ', 'Display value':':'}
        variable_sign = variable_sign_dict[self._variable_type]
        if self._variable_type == 'Display value':
            self._expression = self._equation_name + variable_sign
        else:
            self._expression = self._equation_name + variable_sign + self._equation_value
        #end if
        self._eqn_doc.Equations(self._eqn_index).Expression = self._expression
        #
    def _determine_eqn_index(self):#-----------------------------------------------------
        '''returns the equation index in the collection of equations in the document'''
        for eqn_idx in range(1, self._eqn_doc.Equations.Count+1):
            eqn_expression = self._eqn_doc.Equations(eqn_idx).Expression
            eqn_name, eqn_value = self._split_expression(eqn_expression)
            eqn_var_type = self._determine_variable_type(eqn_expression)
            if (self._equation_name == eqn_name) and (self._variable_type == eqn_var_type):
                break
            #end if
        #end for
        return eqn_idx
        #
    def _split_expression(self, expression: str) -> str:#-----------------------------------------
        '''
        splits full equation into equation name and its value as string
        
        Parameters
        ----------
        expression: string
                 full expression from document
        
        Returns
        -------
        equation_name: string
        equation_value: string
        '''
        variable_type_list = ['=', '<<', ':']
        for i in range(len(variable_type_list)):
            if variable_type_list[i] in expression:
                variable_type_str = variable_type_list[i]
                break
            #end if
        #end if
        
        equation_split = expression.split(variable_type_str)
        equation_name = equation_split[0]
        equation_name = equation_name.lstrip()
        equation_name = equation_name.rstrip()
        if variable_type_str == ':':
            equation_value = ''
        else:
            equation_value = equation_split[1]
            equation_value = equation_value.lstrip()
            equation_value = equation_value.rstrip()
        #end if
        return equation_name, equation_value
        #
    def _determine_variable_type(self, expression: str):#----------------------------------------
        ''' returns variable type from the expression'''
        variable_type_dict = {'=':'Variable definition', '<<':'Parameter definition', ':':'Display value'}
        for variable_type_key in list(variable_type_dict):
            if variable_type_key in expression:
                variable_type_str = variable_type_dict[variable_type_key]
                break
            #end if
        #end if
        return variable_type_str
        #  
#
#**********************************************************************************************
#    
class _ProcessDefinitions():
    '''
    Methods related to Layout Process 
    
    Parmeters
    ---------
    awrde: object variable
         The AWRDE object returned from awrde_utils.EstablishLink()
         
    '''
    def __init__(self, awrde):#-------------------------------------------------
        self.awrde = awrde
        #
    def _unit_type_str(self, unit_type_enum: int) -> str:#-------------------------------------
        '''
        Returns a string that is used as a key for the dictionary returned from _project_units
        
        Parameters
        ----------
        unit_type_enum: integer
                   This value is returned from element parameter UnitType and measurement UnitType
        
        Returns
        -------
        unit_type_str: string
               String that corresponds to the dictionary keys returned from _project_units
        '''
        if mwo.mwUnitType(unit_type_enum) == mwo.mwUnitType.mwUT_Frequency:
            unit_type_str = 'Frequency'
        elif mwo.mwUnitType(unit_type_enum) == mwo.mwUnitType.mwUT_Capacitance:
            unit_type_str = 'Capacitance'
        elif mwo.mwUnitType(unit_type_enum) == mwo.mwUnitType.mwUT_Inductance:
            unit_type_str = 'Inductance'
        elif mwo.mwUnitType(unit_type_enum) == mwo.mwUnitType.mwUT_Resistance:
            unit_type_str = 'Resistance'
        elif mwo.mwUnitType(unit_type_enum) == mwo.mwUnitType.mwUT_Conductance:
            unit_type_str = 'Conductance'
        elif mwo.mwUnitType(unit_type_enum) == mwo.mwUnitType.mwUT_Length:
            unit_type_str = 'Length'
        elif mwo.mwUnitType(unit_type_enum) == mwo.mwUnitType.mwUT_Temperature:
            unit_type_str = 'Temperature'
        elif mwo.mwUnitType(unit_type_enum) == mwo.mwUnitType.mwUT_Angle:
            unit_type_str = 'Angle'
        elif mwo.mwUnitType(unit_type_enum) == mwo.mwUnitType.mwUT_Time:
            unit_type_str = 'Time'
        elif mwo.mwUnitType(unit_type_enum) == mwo.mwUnitType.mwUT_Voltage:
            unit_type_str = 'Voltage'
        elif mwo.mwUnitType(unit_type_enum) == mwo.mwUnitType.mwUT_Current:
            unit_type_str = 'Current'
        elif mwo.mwUnitType(unit_type_enum) == mwo.mwUnitType.mwUT_PowerLog:
            unit_type_str = 'Power in dB'
        elif mwo.mwUnitType(unit_type_enum) == mwo.mwUnitType.mwUT_Power:
            unit_type_str = 'Power'
        elif mwo.mwUnitType(unit_type_enum) == mwo.mwUnitType.mwUT_None:
            unit_type_str = 'None'
        else:
            warnings.warn('unit_type_enum not recognized')
        #end if
        return unit_type_str
        #
    def _project_units(self, lpf_name: str) -> dict:#---------------------------------------------
        '''
        returns dictionary of unit strings according to the layout process file LPF_Name
        
        Parameters
        ----------
        lpf_name: string
                Layout Process File name
        
        Returns
        -------
        lpf_units_dict: dictionary
              keys are the unit type
              values are the unit string for each unit type
              
        '''
        for lpf in self.awrde.Project.ProcessDefinitions:
            if lpf.Name == lpf_name:
                break
            #end if
        #end for
        #
        lpf_units_dict = {}
        lpf_units_dict['Frequency'] = lpf.Units.Item(mwo.mwUnitType.mwUT_Frequency).UnitString
        lpf_units_dict['Capacitance'] = lpf.Units.Item(mwo.mwUnitType.mwUT_Capacitance).UnitString
        lpf_units_dict['Inductance'] = lpf.Units.Item(mwo.mwUnitType.mwUT_Inductance).UnitString
        lpf_units_dict['Resistance'] = lpf.Units.Item(mwo.mwUnitType.mwUT_Resistance).UnitString
        lpf_units_dict['Conductance'] = lpf.Units.Item(mwo.mwUnitType.mwUT_Conductance).UnitString
        lpf_units_dict['Length'] = lpf.Units.Item(mwo.mwUnitType.mwUT_Length).UnitString
        lpf_units_dict['Temperature'] = lpf.Units.Item(mwo.mwUnitType.mwUT_Temperature).UnitString
        lpf_units_dict['Angle'] = lpf.Units.Item(mwo.mwUnitType.mwUT_Angle).UnitString
        lpf_units_dict['Time'] = lpf.Units.Item(mwo.mwUnitType.mwUT_Time).UnitString
        lpf_units_dict['Voltage'] = lpf.Units.Item(mwo.mwUnitType.mwUT_Voltage).UnitString
        lpf_units_dict['Current'] = lpf.Units.Item(mwo.mwUnitType.mwUT_Current).UnitString
        lpf_units_dict['Power in dB'] = lpf.Units.Item(mwo.mwUnitType.mwUT_PowerLog).UnitString
        lpf_units_dict['Power'] = lpf.Units.Item(mwo.mwUnitType.mwUT_Power).UnitString
        lpf_units_dict['None'] = 'None'
        return lpf_units_dict
        #
    def _unit_scale_factor(self, unit_type_str: str, unit_string: str) -> dict:#----------------------------------------------------
        '''
        returns a dictionary for applying offset and scaling to project units
        
        Parameters
        ----------
        unit_type_str: string
              String corresponding to dictionary key returned from _PojectUnits
              
        unit_string: string
               UnitType parameter from element or measurement
        
        Returns
        -------
        unit_scale_factor_dict: dictionary
               keys: Offset1, Offset2, Multiplier
               y = (x + Offset2)*Multiplier +  Offset1
               
        
        '''
        offset1_val = 0
        offset2_val = 0
        multiplier_val = 1
        #
        if unit_type_str == 'Frequency':
            freq_dict = {'THz':1e-12, 'GHz':1e-9, 'MHz':1e-6, 'kHz':1e-3, 'Hz':1}
            multiplier_val = freq_dict[unit_string]
            #
        elif unit_type_str == 'Capacitance':
            capacitance_dict ={'fF':1e15, 'pF':1e12, 'nF':1e9, 'uF':1e6, 'mF':1e3, 'F':1}
            multiplier_val = capacitance_dict[unit_string]
            #
        elif unit_type_str == 'Inductance':
            inductance_dict ={'fH':1e15, 'pH':1e12, 'nH':19, 'uH':1e6,
                              'mH':1e3, 'H':1, 'kH':1e-3, 'MH':1e-6, 'GH':1e-9, 'TH':1e-12}
            multiplier_val = inductance_dict[unit_string]
            #
        elif unit_type_str == 'Resistance':
            resistance_dict = {'fOhm':1e15, 'pOhm':1e12, 'nOhm':1e9, 'uOhm':1e6, 'mOhm':1e3,
                               'Ohm':1, 'kOhm':1e-3, 'MOhm':1e-6, 'GOhm':1e-9, 'TOhm':1e-12}
            multiplier_val = resistance_dict[unit_string]
            #
        elif unit_type_str == 'Conductance':
            conductance_dict = {'fS':1e15, 'pS':1e12, 'nS':1e9, 'uS':1e6, 'mS':1e3, 'S':1}
            multiplier_val = Conductancce_dict[unit_string]
            #
        elif unit_type_str == 'Length':
            length_dict = {'fm':1e15, 'pm':1e12, 'nm':1e9, 'um':1e6, 'mmm':1e3, 'cm':1e2, 'm':1, 'km':1e-3,
                           'mil':(100*1000/2.54), 'inch':(100/2.54), 'foot':(100/(2.54*12)), 'mile':(100/(2.54*12*5280))}
            multiplier_val = length_dict[unit_string]
            #
        elif unit_type_str == 'Temperature':
            temperature_mult_dict ={'DegC':1, 'DegK':1, 'DegF':(9/5)}
            temperature_offset1_dict ={'DegC':273.15, 'DegK':0, 'DegF':32}
            temperature_offset2_dict ={'DegC':0, 'DegK':0, 'DegF':273.15}
            multiplier_val = temperature_mult_dict[unit_string]
            offset1_val = TemperatureOffset_dict[unit_string]
            #
        elif unit_type_str == 'Angle':
            angle_dict = {'Rad':1, 'Deg':(180/np.pi)}
            multiplier_val = angle_dict[unit_string]
            #
        elif unit_type_str == 'Time':
            time_dict = {'fs':1e15, 'ps':1e12, 'ns':1e9, 'us':1e6, 'ms':1e3, 's':1, 'ks':1e-3, 'Ms':1e-6, 'Gs':1e-9, 'Ts':1e-12}
            multiplier_val = time_dict[unit_string]
            #
        elif unit_type_str == 'Voltage':
            voltage_dict = {'fV':1e15, 'pV':1e12, 'nV':1e9, 'mV':1e3, 'V':1, 'kV':1e-3, 'MV':1e-6, 'GV':1e-9, 'TV':1e-12}
            multiplier_val = voltage_dict[unit_string]
            #
        elif unit_type_str == 'Current':
            current_dict = {'fA':1e15, 'pA':1e12, 'nA':1e9, 'uA':1e6, 'mA':1e3, 'A':1, 'kA':1e-3, 'MA':1e-6, 'GA':1e-9, 'TA':1e-12}
            multiplier_val = current_dict[unit_string]
            #
        elif unit_type_str == 'Power in dB':
            power_offset_dict = {'dBm':30, 'dBW':0}
            offset1_val = power_offset_dict[unit_string]
            #
        elif unit_type_str == 'Power':
            power_dict = {'fW':1e-15, 'pW':1e-12, 'nW':1e-9, 'uW':1e-6, 'mW':1e-3, 'W':1, 'kW':1e3, 'MW':1e6, 'GW':1e9, 'TW':1e12}
            multiplier_val = power_dict[unit_string]
            #
        elif unit_type_str == 'None':
            pass
        else:
            warnings.warn('unit_type_str not recognized: ' + unit_type_str)
        #end if
        #    
        unit_scale_factor_dict = {}
        unit_scale_factor_dict['Offset1'] = offset1_val
        unit_scale_factor_dict['Offset2'] = offset2_val
        unit_scale_factor_dict['Multiplier'] = multiplier_val
        return unit_scale_factor_dict
        #
        