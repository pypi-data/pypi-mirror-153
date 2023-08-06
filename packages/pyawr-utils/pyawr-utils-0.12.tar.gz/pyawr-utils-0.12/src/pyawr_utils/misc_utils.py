import pyawr.mwoffice as mwo
from tkinter import messagebox
import warnings
#
#
#*****************************************************************************
#
class _DataFiles():
    '''
    Methods for collection of Data Files in the AWRDE project
    
     Parameters
    ----------
    awrde: The AWRDE object returned from awrde_utils.establish_link()
    
    '''
    def __init__(self, awrde):#----------------------------------------
        self.awrde = awrde
        #
    def _build_data_files_dict(self):#--------------------------------
        '''Create list of all graph names in project
    
        Parameters
        ----------
        None
    
        Returns
        -------
        graphs_dict: dict[element_objects]
                         Each element in the list is a graph name
        '''        
        self._data_files_dict = {}
        for df in self.awrde.Project.DataFiles:
            data_file = _DataFile(self.awrde, df.Name)
            self._data_files_dict[df.Name] = data_file
        #end for
        #
    @property
    def data_files_dict(self) -> dict:#-----------------------------------------------
        '''return data file dictionary'''
        self._build_data_files_dict()
        return self._data_files_dict
        #
    @property
    def data_file_names_list(self) -> list[str]:#-------------------------------------------
        '''returns list of data file names'''
        data_file_name_list = list()
        for df in self.awrde.Project.DataFiles:
            data_file_name_list.append(df.Name)
        #end for
        return data_file_name_list
        #
    def add_dc_iv_file(self, data_file_name: str):#-----------------------------------
        '''
        Add a DC-IV file
        
        Parameters
        ----------
        data_file_name: string
        '''
        self._add_data_file(data_file_name, 'DC-IV')
        #
    def add_dscr_file(self, data_file_name: str):#-----------------------------------
        '''
        Add a DSCR file
        
        Parameters
        ----------
        data_file_name: string
        '''
        self._add_data_file(data_file_name, 'DSCR')
        #
    def add_gmdif_file(self, data_file_name: str):#-----------------------------------
        '''
        Add a Generalized MDIF file
        
        Parameters
        ----------
        data_file_name: string
        '''
        self._add_data_file(data_file_name, 'GMDIF')
        #
    def add_gmdif_nport_file(self, data_file_name: str):#-----------------------------------
        '''
        Add a Generalized MDIF N-Port file
        
        Parameters
        ----------
        data_file_name: string
        '''
        self._add_data_file(data_file_name, 'GMDIF N-Port')
        #
    def add_mdif_file(self, data_file_name: str):#-----------------------------------
        '''
        Add a MDIF file
        
        Parameters
        ----------
        data_file_name: string
        '''
        self._add_data_file(data_file_name, 'MDIF')
        #
    def add_raw_port_parameters_file(self, data_file_name: str):#-----------------------------------
        '''
        Add a Raw Port Parameters file
        
        Parameters
        ----------
        data_file_name: string
        '''
        self._add_data_file(data_file_name, 'Raw Port Parameters')
        #
    def add_text_file(self, data_file_name: str):#-----------------------------------
        '''
        Add a Text file
        
        Parameters
        ----------
        data_file_name: string
        '''
        self._add_data_file(data_file_name, 'Text')
        #
    def add_touchstone_file(self, data_file_name: str):#-----------------------------------
        '''
        Add a Touchstone file
        
        Parameters
        ----------
        data_file_name: string
        '''
        self._add_data_file(data_file_name, 'Touchstone')
        #
    def remove_data_file(self, data_file_name: str) -> bool:
        '''
        Delete a data file from the AWRDE project
        
        Parameters
        ----------
        data_file_name: string,
                 name of the Data File to be deleted
        
        Returns
        -------
        data_file_removed: bool
                    True if data file successfully deleted,
                    False if data file could not be deleted
                    
        '''        
        if not isinstance(data_file_name, str):
            raise TypeError('data_file_name must be a string type')
        #end if
        data_file_removed = False               
        try:
            for df_idx in range(self.awrde.Project.DataFiles.Count):
                if self.awrde.Project.DataFiles[df_idx].Name == data_file_name:
                    self.awrde.Project.DataFiles.Remove(df_idx+1)
                    data_file_removed = True
                    break
                #end if
            #end for
        except:
            warnings.warn('remove_data_file: Data File ' + data_file_name + ' did not get removed')
        #end for
        return data_file_removed
        #
    def rename_data_file(self, data_file_name: str, new_data_file_name: str):#--------------------
        '''
        rename Data File
    
        Parameters
        ----------
        data_file_name: string
                         existing graph name
        new_data_file_name: string
                         new graph name
        '''        
        if not isinstance(data_file_name, str):
            raise TypeError('data_file_name must be a string')
        #end if
        if not isinstance(new_data_file_name, str):
            raise TypeError('new_data_file_name must be a string')
        #end if
        data_file_name_list = self.data_file_names_list
        found_it = False
        for data_file_name_from_list in data_file_name_list:
            if data_file_name_from_list == data_file_name:
                found_it = True
                if new_data_file_name in data_file_name_list:
                    YesNo = messagebox.askyesno('Rename Data File','Data File '\
                        + new_data_file_name + ' exists. Remove existing Data File ?')
                    if YesNo:
                        self.remove_data_file(new_data_file_name)
                    else:
                        new_data_file_name += ' 1'
                    #end if
                #end if
                try:
                    df = self.awrde.Project.DataFiles(data_file_name)
                    df.Name = new_data_file_name
                except:
                    raise RuntimeError('problem with renaming data file')
                #end try
            #end if
        #end for
        if not found_it:
            warnings.warn('data file rename failed: ' + data_file_name)
        #end if
        #
    def copy_data_file(self, data_file_name: str, new_data_file_name: str):#-----------------------
        '''
        copy Data File
    
        Parameters
        ----------
        data_file_name: string
                         existing data file name
        new_data_file_name: string
                         new data file name
        '''
        if not isinstance(data_file_name, str):
            raise TypeError('data_file_name must be a string')
        #end if
        if not isinstance(new_data_file_name, str):
            raise TypeError('new_data)file_name must be a string')
        #end if        
        for df in self.awrde.Project.DataFiles:
            if df.Name == new_data_file_name:
                new_data_file_name = new_data_file_name + ' 1'
            #end if
        #end for
        #
        try:
            for df_idx in range(1, self.awrde.Project.DataFiles.Count+1):
                df = self.awrde.Project.DataFiles(df_idx)
                if df.Name == data_file_name:
                    self.awrde.Project.DataFiles.Copy(df_idx, new_data_file_name)
                #end if
            #end for
        except:
            raise RuntimeError('problem with copying data file')
        #end try
        #
    def import_data_file(self, data_file_name: str, file_path: str, data_file_type: str):#------
        '''
        import data file
        
        Parameters
        ----------
        data_file_name: string
               name of the data file as it will appear in the project
               
        file_path: string
               full directory and file name of the file to be imported
               
        data_file_type: string
               valid values:
                    DC-IV File
                    DSCR File
                    Generalized MDIF Data File
                    Generalized MDIF N-Port File
                    MDIF File
                    Raw Port Parameters File
                    Text File
                    Touchstone File
        '''
        if not isinstance(data_file_name, str):
            raise TypeError('data_file_name must be string type')
        #end if
        if not isinstance(file_path, str):
            raise TypeError('file_path must be string type')
        #end if
        if not isinstance(data_file_type, str):
            raise TypeError('data_file_type must be string type')
        #end if
        #
        if data_file_type == 'DC-IV File':
            data_file_type_enum = mwo.mwDataFileType.mwDFT_IV
        elif data_file_type == 'DSCR File':
            data_file_type_enum = mwo.mwDataFileType.mwDFT_DSCR
        elif data_file_type == 'Generalized MDIF Data File':
            data_file_type_enum = mwo.mwDataFileType.mwDFT_GMDIF
        elif data_file_type == 'Generalized MDIF N-Port File':
            data_file_type_enum = mwo.mwDataFileType.mwDFT_GMDIFD
        elif data_file_type == 'MDIF File':
            data_file_type_enum = mwo.mwDataFileType.mwDFT_MDIF
        elif data_file_type == 'Raw Port Parameters File':
            data_file_type_enum = mwo.mwDataFileType.mwDFT_RAW
        elif data_file_type == 'Text File':
            data_file_type_enum = mwo.mwDataFileType.mwDFT_TXT
        elif data_file_type == 'Touchstone File':
            data_file_type_enum = mwo.mwDataFileType.mwDFT_SNP
        else:
            raise RuntimeError('data_file_type not recognized: ' + data_file_type)
        #end if
        if self._does_data_file_exist(data_file_name):
            YesNo = messagebox.askyesno('Import Data File','Data File ' + data_file_name + ' exists. Delete existing Data File?')
            if YesNo:
                self.remove_data_file(data_file_name)
            #end if
        #end if
        try:
            self.awrde.Project.DataFiles.Import(data_file_name, file_path, data_file_type_enum)
        except:
            raise RuntimeError('Problem with importing data file')
        #end try
        #
    def _does_data_file_exist(self, data_file_name: str) -> bool:#------------------------
        data_file_exists = False
        for df in self.awrde.Project.DataFiles:
            if df.Name == data_file_name:
                data_file_exists = True
            #end if
        #end for
        return data_file_exists
        #
    def _add_data_file(self, data_file_name, data_file_type):#----------------------------
        if data_file_type == 'DC-IV':
            data_file_type_enum = mwo.mwDataFileType.mwDFT_IV
        elif data_file_type == 'DSCR':
            data_file_type_enum = mwo.mwDataFileType.mwDFT_DSCR
        elif data_file_type == 'GMDIF':
            data_file_type_enum = mwo.mwDataFileType.mwDFT_GMDIF
        elif data_file_type == 'GMDIF N-Port':
            data_file_type_enum = mwo.mwDataFileType.mwDFT_GMDIFD
        elif data_file_type == 'MDIF':
            data_file_type_enum = mwo.mwDataFileType.mwDFT_MDIF
        elif data_file_type == 'Raw Port Parameters':
            data_file_type_enum = mwo.mwDataFileType.mwDFT_RAW
        elif data_file_type == 'Text':
            data_file_type_enum = mwo.mwDataFileType.mwDFT_TXT
        elif data_file_type == 'Touchstone':
            data_file_type_enum = mwo.mwDataFileType.mwDFT_SNP
        #end if
        if self._does_data_file_exist(data_file_name):
            YesNo = messagebox.askyesno('Add Data File','Data File ' + data_file_name + ' exists. Delete existing Data File?')
            if YesNo:
                self.remove_data_file(data_file_name)
            #end if
        #end if
        self.awrde.Project.DataFiles.AddNew(data_file_name, data_file_type_enum)
#
#*****************************************************************************
#
class _DataFile():
    def __init__(self, awrde, data_file_name: str):#-----------------------------------
        self.awrde = awrde
        self._initialize_data_file(data_file_name)
        #
    def _initialize_data_file(self, data_file_name: str):#-------------------------------------
        try:
            self._df = self.awrde.Project.DataFiles(data_file_name)
        except:
            raise RuntimeError('Data File does not exist: ' + data_file_name)
        #end try
        #
    @property
    def data_file_name(self) -> str:#------------------------------------------------------
        '''Returns name of the Data File'''
        return self._df.Name
        #
    @property
    def data_file_type(self) -> str:#--------------------------------------------------
        '''
        Reports data file type 
        
        Returns
        -------
        data_file_type_str: string
              DC-IV File, DSCR File, Generalized MDIF Data File, Generalized MDIF N-Port File,
              MDIF File, Raw Port Parameters File, Text File, Touchstone File
        
        ''' 
        data_file_type_enum = self._df.Type
        if mwo.mwDataFileType(data_file_type_enum) == mwo.mwDataFileType.mwDFT_IV:
            data_file_type_str = 'DC-IV File'
        elif mwo.mwDataFileType(data_file_type_enum) == mwo.mwDataFileType.mwDFT_DSCR:
            data_file_type_str = 'DSCR File'
        elif mwo.mwDataFileType(data_file_type_enum) == mwo.mwDataFileType.mwDFT_GMDIF:
            data_file_type_str = 'Generalized MDIF Data File'
        elif mwo.mwDataFileType(data_file_type_enum) == mwo.mwDataFileType.mwDFT_GMDIFD:
            data_file_type_str = 'Generalized MDIF N-Port File'
        elif mwo.mwDataFileType(data_file_type_enum) == mwo.mwDataFileType.mwDFT_MDIF:
            data_file_type_str = 'MDIF File'
        elif mwo.mwDataFileType(data_file_type_enum) == mwo.mwDataFileType.mwDFT_RAW:
            data_file_type_str = 'Raw Port Parameters File'
        elif mwo.mwDataFileType(data_file_type_enum) == mwo.mwDataFileType.mwDFT_TXT:
            data_file_type_str = 'Text File'
        elif mwo.mwDataFileType(data_file_type_enum) == mwo.mwDataFileType.mwDFT_SNP:
            data_file_type_str = 'Touchstone File'
        #end if
        return data_file_type_str
        #
    def export_data_file(self, file_path: str) -> bool:#--------------------------------------
        '''
        exports the data file to the directory and name specified by file_path
        
        Parameters
        ----------
        file_path: string
              full director and file name
        
        Returns
        -------
        export_successful: bool
        '''
        if not isinstance(file_path,str):
            raise TypeError('file_path must be string type')
        #end if
        #
        export_successful = True
        try:
            self._df.Export(file_path)
        except:
            export_successful = False
        #end try
        return export_successful
        
#
#*****************************************************************************
#