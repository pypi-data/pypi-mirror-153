# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 11:04:18 2020

@author: dream
"""

import xlrd as xls

# -----------------------------------------------------------------------------    
# Tools for editing files
# -----------------------------------------------------------------------------
def row_to_col(row_vector):
    """
    Function to convert a row vector to a column vector. From [1, 2, 3, 4] to
    [[1], [2], [3], [4]].

    Parameters
    ----------
    row_vector : list
        
    Returns
    -------
    col_vector : list
        
    """
    col_vector = []
    for val in row_vector:
        col_vector.append([val])
    
    return col_vector

def rmv_row(path_file, rows_delete=[1], top_row=True):
    """
    Function to remove specified rows from a file.
    
    Parameters
    -----------
    path_file : string
        File name and path for the file from which the row will be removed.
    			
    rows_delete : integer list
        List with the number of the rows to be deleted starting from 1. By
        default the first row is deleted.
    
    top_row : boolean
        Specify if the counting is from the top or from the bottom. By default
        it is True (starting from the top)
    """
    
    #Atributtes initiation
    path = path_file
    row_number = rows_delete.copy()
    top = top_row
    
    #Reading of the lines
    file = open(path, "r")
    lines_original = file.readlines()
    file.close()
		
    amnt_lines = len(lines_original)
		
    #Adjustment of row number for starting in 0 and not in 1
    row_number[:] = [(number - 1) for number in row_number]
		
		#Adjustment of the row number to be deleted in case it start from bottom.
    if top == False :
		    row_number[:] = [(amnt_lines - number) for number in row_number]
		
		#Creation of a list with the final edited rows to write
    lines_edited = []
		
    for i_row in range(0, amnt_lines):
		    if not (i_row in row_number):
				    lines_edited.append(lines_original[i_row])
		
		#writing file
    file = open(path, "w")
    for i_row in range(0, len(lines_edited)):
        file.write(lines_edited[i_row])
		
    file.truncate()
    file.close()

# -----------------------------------------------------------------------------    
# Tools for writing files
# -----------------------------------------------------------------------------

def export_csv(name, data, headers=[" "], units=[" "], comments=[" "],
               cmt_start = "", delimiter=",", append = False):
    """
    Function to export data to a file to plot somewere else.
    
    Parameters
    ----------
    name : string
        File name for the file to be created.
        
    data : list of numpy arrays
        Numpy arrays to be recorded as columns in the file.
    
    headers : list of string
        Name of the columns in the data sets
        
    units : list of string
        Units to be used for the values of each column in data set
    
    Comments : list of string
        General comments to be describe each column.
    """
    
    AmountColumns = len(data)
    
    #Creating header, units and comments when they are not defined
    if headers == [" "]:
       for i in range(1, AmountColumns):
           headers.append(" ")
    
    if units == [" "]:
       for i in range(1, AmountColumns):
           units.append(" ")           
    
    if comments == [" "]:
       for i in range(1, AmountColumns):
           comments.append(" ")
            
    
    # Creating the header, units and comments lines
    h_line = headers[0]
    u_line = units[0]
    c_line = comments[0]
    
    if AmountColumns != 1:
        for i in range(1,AmountColumns):
            h_line = h_line + delimiter + headers[i]
            u_line = u_line + delimiter + units[i]
            c_line = c_line + delimiter + comments[i]
    
    
    header_string = h_line + "\n" + u_line + "\n" + c_line
    
    # Write file
    """
    # Numpy style ------------------------------------------------------------
    np.savetxt(name, np.column_stack(data), delimiter = ",",
               header=header_string, comments="")
    #-------------------------------------------------------------------------
    """
    
    #Python core style -------------------------------------------------------
    if not append:
        file = open(name, 'w')
    
    else:
        file = open(name, 'a')
    
    file.write("{0}\n************************************\n".format(cmt_start))
    file.write("{0}\n".format(header_string))
    
    col_amnt = len(data)
    row_amnt = len(data[0])
    
    for r in range(row_amnt):
        file_row = "{0}".format(data[0][r])
        
        for c in range(1, col_amnt):
            file_row = file_row + delimiter + "{0}".format(data[c][r])
        
        file_row = file_row + "\n"
        
        file.write(file_row)
    file.close()

# -----------------------------------------------------------------------------    
# Tools for reading data formats
# -----------------------------------------------------------------------------
class Data:
    """
    Basic class for the format to be delivered to further analysis to other
    classess and functions.
    
    Parameters
    ----------
    headers: list of strings
        Name of the different numpy arrays containing the data.
    
    data: list of numpy array
    
    """
    def __init__(self, header, data):
         self.header = header
         self.data = data

#General exel reader
class DataXls:
    """
    Class to obtain data using saved in xls format. It returns the data structure of device
    type.
    
    Parameters
    ----------
    path : string
         Path to the file from which to extract the data. Important to use '/'
         to separate directories.
    sheet_index : int
         Number of the excel book containing the data of the the device. If not
         specified '0' is used by default.
    header : list of strings
         List with the name of the data to be extracted from the book. For
         example ["VGS", "VDS", "ID", "IG"]. The names are case sensitive. If
         it is not specified or if the first value of the list is 1 the header
         will be taken from the first row of the data book. 
    
    
    Attributes
    ----------
    path : string
         Attribute containing the path passed as parameter.
    
    sheet_index : int
         Number of the sheet containing the data of interest.
         
    header : list of strings
         List containing the names for the different vectors on the data
         attribute.

    data : numpy array
         Extracted data from the exel file. Notice that the values are arranged
         in data vectors following the description of the header. For example,
         if the header is ["VGS", "ID", "VDS"] the first vector of the data
         attribute [0] will contain the values for VGS, the second vector [1]
         will contain ID values and third vector [2] will contain VDS.
         
    Methods
    -------
    get_data : void
         Method to extract data from file. It is automatically called by the
         constructor but can also be called after in case the source file with
         the data is changed.
    
    
    Example
    -------
    >>> import FileHandler
    >>> file = "C:/test.xls"
    >>> columns = ["VGS", "VDS", "IDS"]
    >>> test = Data_xls(path=file, book=1, header=columns)
    """
    
    def __init__(self, path, sheet_index=0, header=[1]):
        
        #Initialization of attributes that depend on the parameters.
        self.path = path
        self.sheet_index = sheet_index
        self.header = header
        
        #Execution of method to obtain data
        self.get_data()
    
    def get_data(self):
        #Method to get the data from the xls file.
        
        #Openning the book and the sheet where the data is
        self.book = xls.open_workbook(self.path) 
        self.sheet = self.book.sheet_by_index(self.sheet_index)
        
        #Parsing the header from the first line of the file. The file is
        #required to have a header.
        
        header_row = self.sheet.row_values(0)
        
        if self.header[0] != 1:
            
            #Creating list for valid indexes in the order of the passed headers
            valid_header_index = []
            
            #Parsing to obtain the index of the headers
            for i in range(len(self.header)):
                valid_header_index.append(header_row.index(self.header[i]))
            
            # Obtaining the data of the columns that are required
            data = []
            for i in range(len(valid_header_index)):
                vr = self.sheet.col_values(valid_header_index[i])[1:]
                data.append(vr)
            
            #Copying the extracted data to data attribute of the class
            self.data = data
        
        else:
            
            # Obtaining the data of the columns that are required
            data = []
            for i in range(len(header_row)):
                data.append(self.sheet.col_values(i)[1:])
            
            #Copying the extracted data to data attribute of the class
            self.data = data
            
            #Overwriting the extracted header_row to the attribute header
            self.header = header_row
            
class DataHp:
    """
    Class for reading plot files from hp parameter analyzer using the hp api.
    """
    def __init__(self, path, skip_line="auto", delimiter="\t", data_start=1):
        
        self.path = path
        self.header = []
        self.data = []
        self.delimiter=delimiter
        self.data_start=data_start #Index for data start from the header
        
        self.get_lines()
        
        if type(skip_line) == str:
            if skip_line.upper() == "FLEX":
                self.skip_line = 11
            else:
                self.get_skip()
                
        else:
            self.skip_line = skip_line
        
        self.lines = self.lines[self.skip_line:]
        
        self.parse_lines()
        
    def get_skip(self):
        i_line = 1
        line = self.lines[0]
        
        while(line[0] != "*" and i_line < len(self.lines)):
            line = self.lines[i_line]
            i_line = i_line + 1
        
        self.skip_line = i_line
                
    def get_lines(self):
        file = open(self.path, "r")
        self.lines = file.readlines()
        self.amnt_lines =  len(self.lines)
        file.close()
              
    def parse_lines(self):    
        
        self.header = self.lines[0].replace("\n","").split(self.delimiter)        
        amnt_col = len(self.header)
        amnt_row = len(self.lines)
        
        for i in range(amnt_col):
            if self.header[i] == "TIME":
                self.header[i] = "T_" + self.header[i+1]
            
        #initiation of the data vector
        self.data = [[] for i in range(amnt_col)]
        
        self.bad_row = []
        
        for i_row in range(self.data_start, amnt_row):
            line = self.lines[i_row][:-1].split(self.delimiter)
            
            #appending columns
            for i_col in range(amnt_col):
                if line[i_col] == "NULL":
                    line[i_col] = "INF"
                    self.bad_row.append(i_row-1)
                    
                self.data[i_col].append(float(line[i_col]))
                
        #Removing bad rows from max number to min that had "NULL" or others
        self.bad_row = list(set(self.bad_row))
        self.bad_row.sort()
        self.bad_row = self.bad_row[::-1]
        
        for i_row in self.bad_row:
            for column in self.data:
                column.pop(i_row)
        
        self.data = {self.header[i]:self.data[i] for i in range(amnt_col)}

        