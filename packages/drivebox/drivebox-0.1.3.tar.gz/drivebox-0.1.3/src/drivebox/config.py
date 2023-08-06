    # -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 13:33:19 2019

@author: lockhart
"""

class confGlobal:
    """
    With the configuration parameters fro the cmb serial interface.
    """
    def __init__(self):    

        self.bit_rate = 115200  #bit rate for the communication
        self.board_id = "000" # Board identifier to discover.
        self.board_description = "Nano 33 BLE"
        self.board_vid_pid = "VID:PID=2341:805A"
        self.timeout = 1 #timeout in seconds.
        self.port = "AUTO" #Port where the cmb is connected

        #Acknowledge
        self.ACKNOWLEDGE = 'OK'
        
        #Configurations for the mux
        self.v_delta = 1e-4
        self.i_delta = 1e-15
        self.meas_time_max_iterations = 5
        self.meas_delay = 174.0e-3 #delay for adquiring a datapoing in seconds.
        self.time_delta = 5e-3 #time frame delta for measurements In seconds.
        self.time_response = 5e-3 #Response time between meas functions in S
        
        #Measurement calbiration
        self.r_mean = [0, 0, 0, 0, 0]
        self.residue = [0, 0, 0, 0, 0]

