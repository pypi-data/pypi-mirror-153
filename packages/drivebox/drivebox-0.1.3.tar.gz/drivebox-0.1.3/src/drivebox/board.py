# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 13:34:53 2019
api_cmb_vXX.py: Api to control the Caonabo Driving Board for DNA synthesis.

Version:
    V1.0.0: Initial release.
    V2.0.0 (2021-06-29): Write acknowledgement implemented.

author = César J. Lockhart de la Rosa
copyright = Copyright 2021, imec
license = GPL
email = lockhart@imec.be, cesar@lockhart-borremans.com
status = Release

"""

import serial
import serial.tools.list_ports as ls_ports
import drivebox.config as config
import drivebox.common as cf
import time
import math

# Python conventional header

class cdb:
    """
    Class for interfacing the Caonabo Driving Board (CDB).
    """


    def __init__(self, port="NA", board_id="NA",
                 board_description="NA",
                 conf=config.confGlobal()):
        
        self.conf = conf
        
        if board_id == "NA" :
            self.board_id = self.conf.board_id
        else:
            self.board_id = "ID:" + board_id
            self.conf.board_id = board_id
            
        self.board_id_ok = False, 
        

        if board_description == "NA" :
            self.board_description = self.conf.board_description
        else:
            self.board_description = board_description

        if port != "NA" :
            self.conf.port = port           
        

        if self.conf.port == "AUTO":
            self.discoverPort()
        else:
            self.com()
            
        self.range = self.getRange()
        self.getMeasDelay()
        
    def getMeasDelay(self):
        """
        Method to obtain the delay it takes to the CDB to measure a data point
        [V,I]. The result is stored in self.conf.meas_delay in seconds.
        """
        
        avrg_meas_time = 0
        amnt_iterations = self.conf.meas_time_max_iterations
        
        #Dummy measurements to avoid autoRanging playing a role in the process
        self.dMeas()
        self.dMeas()
        
        for iteration in range(amnt_iterations):    
            start_time = time.time()
            self.dMeas()
            finish_time = time.time()
            
            meas_time = finish_time - start_time
            avrg_meas_time = avrg_meas_time + meas_time/amnt_iterations
        
        avrg_meas_time = math.ceil(100*avrg_meas_time)/100
        
        print("Average measurement delay (For [V,I]):"
              " {}ms".format(1000*avrg_meas_time))
        
        self.conf.meas_delay = avrg_meas_time
            
    def discoverPort(self):
        """
        Method to auto discover the port were the CDB is connected.

        """
        port_list = list(ls_ports.comports())
        
        port_name=[]
        
        for p in port_list:
            
            if self.conf.board_vid_pid in p.hwid: #It is an arduino 33 BLE
                port_name.append(p.device)
        
        for p in port_name:
            try:
                self.com(port=p, bit_rate=self.conf.bit_rate,
                board_id=self.board_id, timeout=self.conf.timeout)
                portOpen = True
            except:
                portOpen = False

            if not self.board_id_ok:
                if portOpen:
                    self.serial.close()
            else:
                self.conf.port = p
                break        

                
    def com(self, port='NA', bit_rate='NA', board_id="NA", timeout="NA"):
        """
        Method to start the serial communication.

        Parameters
        ----------
        port : str, optional
            Name of the port where the CDB is connected or "AUTO". Default is 
            "AUTO" (from the configuration file).
        bit_rate : int, optional
            Bit rate for comunication. Default is 'NA' (taken from conf file).
        board_id : str, optional
           ID of the board that must be connected. The default is "000".
           (from conf file)
        timeout : TYPE, optional
            Time out to wait before giving error for comunication.
            The default is 1s (from conf file).

        """
        
        #Taking default values if nothing is specified.
        if port == "NA":
            port = self.conf.port
            
        if bit_rate == "NA":
            bit_rate = self.conf.bit_rate
            
        if board_id == "NA":
            board_id = self.conf.board_id
        
        if timeout == "NA":
            timeout = self.conf.timeout
            
        # Starting serial communication
        self.serial = serial.Serial(port=port, baudrate=bit_rate,
                                    timeout=timeout)
        
        # Getting ID and verifying that right board is connected.
        time.sleep(1)
        
        id_hw = self.getID().split("_")
        
        board_version = id_hw[0]
        firmware_version = id_hw[1]
        board_id_hw = id_hw[2]
        
        if board_id == board_id_hw:
            print("Caonabo DriveBox (CDB) with correct ID" + 
                  " initiated in port: {0}.".format(port))
            self.board_id_ok = True
            self.board_version = board_version
            self.firmware_version = firmware_version
        
        else:
            self.board_id_ok = False
        

    def write(self, string):
        """
        Write string to the serial interface of the CDB.
        
        Parameters
        ----------
        
        string: str
            String to be written.
        """
        response = self.serial.write(string.encode('utf-8'))
        return response
    
    def read(self):
        """
        Read a line of string (up to the \n charater) from the serial
        interface of the CDB.
        """
        return self.serial.readline().decode('utf-8')[0:-2]

    def acknowledgeWrite(self):
        """
        Check that a write call was performed correctly. 

        Raises
        ------
        ValueError
            If the read does not return the correct acknowledgment string.
        """

        if  self.read() != self.conf.ACKNOWLEDGE:
            raise ValueError('Could not acknowledge the write command.')

    
    def getID(self):
        """
        Method to get the board id.
        """
        
        s_cmd = 'ID?\n'
        self.write(s_cmd)
        return self.read()
    
    def setCMB(self, data):
        """
        Function to set the status of the CMB through a vector with 69
        specified values array. Takes about 32µs.

        Parameters
        ----------
        data : list
            Vector representing the new status of the MUX.
        """
        
        s_cmd = 'SET' + data + '\n'    
        self.write(s_cmd)
        self.acknowledgeWrite()
    
    def getCMB(self):
        """
        Function to get the vector representing the status of the MUX.
        """
        s_cmd = 'GET' + '\n'    
        self.write(s_cmd)
        return self.read()
    
    def confIO(self, portType):
        """
        Method to configure the IO pins accessible to the user. is an string
        with 5 characters which value define the pin type (0 for output and 1
        for input).

        Parameters
        ----------
        portType : string
            Five character specifying if the pin is an output or an input. 
            Ex.: confIO("01100") for output, input, input, output, output.
        """
        
        s_cmd = 'CIO' + portType + '\n'    
        self.write(s_cmd)
        self.acknowledgeWrite()
    
    def setIO(self, port):
        """
        Function to set the status of the digital IO ports in J1 from an
        string of five characters representing each pin og the IO port.
        
        Parameters
        ----------
        port : string
            Name of the port to be manupulated (can be 0 or 1).
        """
        
        s_cmd = 'SIO' + port + '\n'    
        self.write(s_cmd)
        self.acknowledgeWrite()
    
    def getIO(self):
        """
        Function to get the status of the digital IO ports in J1 from an
        string of five characters representing each pin og the IO port.
        Only the pins set as input will return a value. If the pin is an 
        output and X will be returned in that possition.
        
        Returns
        -------
        portStatus : string
            string with 5 characters descriving the status of the pins. 
        """
        
        s_cmd = 'GIO' + '\n'    
        self.write(s_cmd)
        portStatus = self.read()
        
        return portStatus
    
    def setAll(self):
        """
        Function to set all the switches from group A, B and C ON. Takes 12µs.
        """
        s_cmd = 'SON' + '\n'
        self.write(s_cmd)
        self.acknowledgeWrite()
    
    def clearAll(self):
        """
        clear all the switches from group A, B and C. Takes about 32µs.
        """
        s_cmd = 'SOF' + '\n'
        self.write(s_cmd)
        self.acknowledgeWrite()
    
    def setSw(self, group, sw_number):
        """
        Function to set ON an specific switch. Takes about 4µs.
        
        Parameters
        ----------
        group : string
            Group where the switch is located (A, B or C).
        sw_number : integer
            Number off the switch be activated (from 1 to 16).
        """        
        
        s_cmd = 'SSW{0:s}{1:02d}'.format(group, sw_number) + '\n'
        
        self.write(s_cmd)
        self.acknowledgeWrite()
    
    def clearSw(self, group, sw_number):
        """
        Function to clear (set OFF) an specific switch. Takes about 4µs.
        
        Parameters
        ----------
        group : string
            Group where the switch is located (A, B or C).
        sw_number : integer
            Number of the switch to be activated.
        """        
        
        if sw_number > 9:
            s_cmd = 'CSW' + group + str(sw_number) + '\n'
        else:
            s_cmd = 'CSW' + group + '0' + str(sw_number) + '\n'
        
        self.write(s_cmd)
        self.acknowledgeWrite()
        
    def setSignal(self, group, signal):
        """
        Function to set the signals going to each group
        
        Parameters
        ----------
        group : string
            Identifier for the group to wish the signal will be directed. It
            can be A, B, C, CE1 or CE2.
        signal : integer
            Signal from the J7 terminal block to be redirected to the group. It
            can be C, W, R or J for CE, WE, RE or their respective group
            terminals in J7.
        """
        if group == "CE1":
            group = 'D'
        
        if group == "CE2":
            group = 'E'
        
        s_cmd = 'SSG' + group + signal + '\n'    
        self.write(s_cmd)
        self.acknowledgeWrite()
        
    def setToJ(self, group='all'):
        """
        Function to clear signal going to a group (i.e., set to "J")
        
        Parameters
        ----------
        group : string or list
            Identifier for the group to wish the signal will be directed. It
            can be A, B, C, CE1 or CE2 or 'all' (default).
        """
        
        if group == 'all':
            group = ['A', 'B', 'C', 'CE1', 'CE2']
        if type(group) is str:
            group = [group]
            
        for grp in group:
            self.setSignal(grp, 'J')
    
    
    def pulse(self, on_delay, off_delay, amnt_periods, switch):
        """
        Method to generate a pulse train by specifying the on_delay, the
        off_delay and the amount of periods (amnt_periods). The values are
        specified as integers from 0 to 999999. In the case of the delay the 
        value can be link to the duration by: delay = 2.7006*value + 20.212 µs
        The minimum delay (value = 0) is 20.212µs.

        Parameters
        ----------
        on_delay : int
            Used to set the delay of the ON state of the pulse train.
        off_delay : int
            Used to set the delay of the OFF state of the pulse train.
        amnt_periods : int
            Specify the amount of periods to be generated.
        """
        digits = 6
        str_ondelay = cf.int_2_str(integer=on_delay, 
                                   amnt_digits=digits,
                                   spacer="0")
        
        str_offdelay = cf.int_2_str(integer=off_delay, 
                                    amnt_digits=digits,
                                    spacer="0")
        
        str_amntperiods = cf.int_2_str(integer=amnt_periods, 
                                       amnt_digits=digits,
                                       spacer="0")
        
        switch = switch.upper()
        
        s_cmd = 'PTG' + str_ondelay + str_offdelay + str_amntperiods
        s_cmd = s_cmd + switch + '\n'
        
        self.write(s_cmd)
        self.acknowledgeWrite()
        
    def pulse_us(self, on_delay, off_delay, duration, switch):
        """
        Same as the pulse function but you can input values in us.
        """
        
        period = on_delay + off_delay
        amnt_periods = int(duration/period)
        
        on_delay = cf.ustoint(on_delay)
        off_delay = cf.ustoint(off_delay)
                        
        self.pulse(on_delay, off_delay, amnt_periods, switch)
    
    def ovpReset(self):
        """
        Method to reset the overvoltage protection.
        """
        
        s_cmd = 'OVR' + '\n'    
        self.write(s_cmd)
        self.acknowledgeWrite()
        
    def ovpStatus(self):
        """
        Method to get the status of the over voltage protections in the CE, RE,
        and WE inputs.
        
        Return
        ------
        
        status: int
            Integer (from 0 to 7) representing what port was activated. If the
            the 3 channels are ON you get a 7 if OV was triggered and the 
            channels are OFF you get 0.
        """

        s_cmd = 'OVS' + '\n'    
        self.write(s_cmd)
        return self.read()
    
#*****************************************************************************
#Methods for onboard potentiostat
#*****************************************************************************

    def setMode(self, mode):
        """
        Method to set the mode of the sourcing unit("P" for potentiostat and
        "G" for galvanostat).
        
        Parameters
        ----------
        mode : string
            Mode of the sourcing unit, can be "P" or "G".
        """
        
        mode = mode.upper()
        
        s_cmd = 'SMD' + mode + '\n'    
        self.write(s_cmd)
        self.acknowledgeWrite()

    def getMode(self):
        """
        Method to get the mode of the sourcing unit("P" for potentiostat and
        "G" for galvanostat).
        
        Returns
        -------
        mode : string
            Mode of the sourcing unit, can be "P" or "G".
        """
        
        s_cmd = 'GMD' + '\n'
        self.write(s_cmd)
        
        return self.read()
    
    def setRange(self, iRange):
        """
        Method to set the current range can be from 0 to 4:
     
        RANGE 0 I_MAX 250e-3 A (resolution = 120nA)
        RANGE 1 I_MAX  25e-3 A (resolution =  12nA)
        RANGE 2 I_MAX 250e-6 A (resolution = 120pA)
        RANGE 3 I_MAX 2.5e-6 A (resolution = 1.2pA)
        RANGE 4 I_MAX 250e-9 A (resolution = 120fA)
        
        Parameters
        ----------
        iRange : integer
            Current range
        """
        
        s_cmd = 'SRG' + str(iRange) + '\n'    
        self.write(s_cmd)
        self.acknowledgeWrite()
        self.range = iRange
    
    def getRange(self):
        """
        Method to get the current range can be from 0 to 4:
     
        RANGE 0 I_MAX 250e-3 A (resolution = 120nA)
        RANGE 1 I_MAX  25e-3 A (resolution =  12nA)
        RANGE 2 I_MAX 250e-6 A (resolution = 120pA)
        RANGE 3 I_MAX 2.5e-6 A (resolution = 1.2pA)
        RANGE 4 I_MAX 250e-9 A (resolution = 120fA)
        
        Returns
        -------        
        iRange : integer
            Current range
        """
        
        s_cmd = 'GRG' + '\n'    
        self.write(s_cmd)
        
        self.range = int(self.read())
        return self.range
    
    def setSource(self, value):
        """
        Method to set the value of the source (voltage for potentiostat
        and current for galvanostat). In case of galvanostat remember to set
        the appropriate range.
     
        Parameters
        ----------
        value : float
            Value to be et at the source
        """
        
        s_cmd = 'SVS' + repr(value) + '\n'    
        self.write(s_cmd)
        self.acknowledgeWrite()
    
    def vMeas(self):
        """
        Method to measure the voltage between S(ense) and R(eference)
        electrodes in the potentiostat.
        
        Returns
        -------
        voltage : float
            Measured voltage in volts.
        """
        
        s_cmd = 'VMS' + '\n'    
        self.write(s_cmd)
        
        return float(self.read())

    def iMeas(self):
        """
        Method to measure the current at the working electrode.
        
        Returns
        -------
        current : float
            Measured current in amps.
        """
        
        s_cmd = 'IMS' + '\n'    
        self.write(s_cmd)
        
        return [float(self.read()), int(self.read())]

    def dMeas(self):
        """
        Method to measure a data point (current plus voltage) at the working
        electrode.
        
        Returns
        -------
        [voltage, current] : list float
            Measured current and voltages in volts and amps. The current
            is currected with respect to calibration data. if no correction
            is required the respective parameter in the configuration file for
            the r_mean and residue should be put to 0.
        """
        
        s_cmd = 'DMS' + '\n'    
        self.write(s_cmd)
        

        voltage = float(self.read())
        current = float(self.read())
        i_range = int(self.read())
        
        
        return [voltage, current, i_range]
    
    def meas(self, daqValues = "VI"):
        """
        Method to adquire values. can be "V" for the voltage, 
        "I" for recording the current, "C" for temperature in centigrades,
        and "F" for the temperature in farenheit (The temperature in the
        DriveBox for measurementcorrection).

        Parameters
        ----------
        daqValues : string
            Values to be adquired the string can be I, V, C or F. The data
            will be returned in the same order it is passed.

        Returns
        -------
        data: list
            lsit with the values required to be reported.

        """
        daqValues = daqValues.upper()
        data = []
        
        for param in daqValues:
            if param == "V":
                data.append(self.vMeas())
            elif param == "I":
                [current, irange] = self.iMeas()
                data.append(current)
                data.append(irange)
            elif param == "C":
                self.setTempUnits("C")
                data.append(self.getTemp())
            elif param == "F":
                self.setTempUnits("F")
                data.append(self.getTemp())
        
        return data
            
    
    def resetSMU(self):
        """Method to reset SMU unit."""
        
        s_cmd = 'RSM' + '\n'    
        self.write(s_cmd)
        time.sleep(60e-3) #wait 60ms after delay
        self.acknowledgeWrite()
    
#*****************************************************************************
#Methods for onboard sensors
#*****************************************************************************
    def setTempUnits(self, units="C"):
        """
        Method to set the units to be returned for the on board temperatrue 
        measurement.

        Parameters
        ----------
        units : string
            "C" for Celsius and "F" for Fahrenheit. Default is "C".
        """

        units = units.upper()
        s_cmd = 'STU' + units + '\n'    
        self.write(s_cmd)
        self.acknowledgeWrite()

    def getTempUnits(self):
        """
        Method to get the units to be returned for the on board temperatrue 
        measurement.

        Returns
        -------
        units : string
            "C" for Celsius and "F" for Fahrenheit. Default is "C".
        """
        
        s_cmd = 'GTU' +  '\n'    
        self.write(s_cmd)
        return self.read()

    def getTemp(self):
        """
        Method to get the  on board temperatrue measurement.

        Returns
        -------
        temp : float
            Temperature in the specified unit.
        """
        
        s_cmd = 'GTV' +  '\n'    
        self.write(s_cmd)
        return float(self.read())

    def getHumidity(self):
        """
        Method to get the  on board humidity measurement. Units is %rH

        Returns
        -------
        humidity : float
            Humidity in %rH.
        """
        
        s_cmd = 'GHV' +  '\n'    
        self.write(s_cmd)
        return float(self.read())
    
#-----------------------------------------------------------------------------
#LCD Methods
    
    def lcdBackLight(self, color):
        """
        Method to choose the color for the lcd backligth

        Parameters
        ----------
        color : character or integer
            Can be an integer from 0 to 7 representing RGB in binary or a
            letter representing a color code (standard colors) according to the
            following table:
                
            'k' : 0 : All lights off,
            'b' : 1 : blue light on,
            'g' : 2 : green light on,
            'c' : 3 : blue and green on (cyan), 
            'r' : 4 : red light on,
            'm' : 5 : blue and red on (magenta),
            'y' : 6 : green and red on (yello),
            'w' : 7 : red, green and blue on (white).
            
            it can be caps or small, they will be change to small cap
        """
        self.lcdBackLigthDic = { 'k' : 0,
                                 'b' : 1,
                                 'g' : 2,
                                 'c' : 3, 
                                 'r' : 4,
                                 'm' : 5,
                                 'y' : 6,
                                 'w' : 7}
        
        if type(color) == str:
            color = self.lcdBackLigthDic[color.lower()];
        
        s_cmd = 'LBL' + str(color) + '\n'    
        self.write(s_cmd)
        self.acknowledgeWrite()
    
    def lcdMessage(self, message):
        """
        Method to print a message the first line of the CDB lcd

        Parameters
        ----------
        message : string
            Text (16 characters) to be send.
        """
        
        s_cmd = 'MSG' + message + '\n'    
        self.write(s_cmd)
        self.acknowledgeWrite()
    
    def lcdClear(self):
        """
        Clear lcd
        """
        
        s_cmd = 'LCL' + '\n'    
        self.write(s_cmd)
        self.acknowledgeWrite()

#*****************************************************************************
#General methods
#*****************************************************************************

    def close(self):
        """Close the serial port."""
        self.serial.close()
    
    def open(self):
        """Open the serial port."""
        self.serial.open()

        
        
        
        
     