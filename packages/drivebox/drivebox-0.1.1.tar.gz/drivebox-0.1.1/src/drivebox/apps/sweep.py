# -*- coding: utf-8 -*-
"""
Created on Wed May 12 13:41:07 2021

@author: dream
"""
import drivebox.file_handlers as fh
import drivebox.graph_plots as gp
import time
import datetime
import matplotlib
import numpy as np


class sweeping:
    """
    Application to run a CV measurement using the onboard source
    measurement unit of the CDB. It can be used either specifying a delay
    and an deltaVal (the step size) or a rate. If rate is spcified delay
    and step size is ignored.

    Parameters
    ----------
    filename: string
        Filename for the plot and and the txt file. for the path it can be
        changed directly in the attribute.
    cdb : core.api_cdb
        Handler to an instance of a caonabo driving board.
    firstVal : float
        First value for starting the sweeping (Volts or Amps).
    minVal : float
        Minimum value to be reach during the sweeping (Volts or Amps).
    maxVal : float
        Maximum value for the sweeping.
    iRange : integer
        From 0 to 5 in agreement with the ideal range for current meas.
    deltaVal : float
        Steps increments for sourced signal (in volts or amps). if not
        specified rate and amount of points must be specified.
    delay : float
        delay time in seconds to wait between steps (outside of the
        measurement time that is around 170ms).
    hold : float, optional
        Holding time in seconds at "firstVal" before starting sweep.
        The default is 1.
    cycles : integer, optional
        Amount of repetitions of the sweeping cycle. The default is 1.
    rate : float, optional
        rate in [voltage or current]/second.
        The default is "NA". if specified over rule delay and deltaVal.
    mode : string, optional
        To select the working mode as POTentiostat of GALvanostat.
        The default is "POT".
    direction : string
        Direction of sweep: "INC"rease or "DEC"rease
    conf : configuration
        Configuration for the app. Any configuration can be pass.
    
    comment: string
        Comment to be added to the data file and fhe figure.
    """
    def __init__(self, filename, cdb, firstVal, minVal, maxVal, iRange,
                 deltaVal="NA", delay=0, hold=1, cycles=1,  rate="NA",
                 mode="POT", direction="INC", comment="", lcd_enable=True):
        
        
        #Creating attributes from parameters        
        self.cdb = cdb
        self.firstVal = float(firstVal) #when POT (GAL) in V (A)
        self.minVal = float(minVal) #when POT (GAL) in V (A)
        self.maxVal = float(maxVal) #when POT (GAL) in V (A)
        self.iRange = iRange
        self.deltaVal = float(deltaVal) #when POT (GAL) in V (A)
        self.delay = float(delay) + self.cdb.conf.meas_delay #in S
        self.hold = float(hold) #in S
        self.cycles = cycles
        self.rate = rate #in v/S
        self.mode = mode
        self.direction = direction
        self.path = ""
        self.filename = filename
        self.comment = comment
        self.max_points_sec = 1/self.cdb.conf.meas_delay
        self.rate_exp="NA"
        self.lcd_enable = lcd_enable
        
        if type(rate) == str:
            self.rateOrDelay = "delay"
        else:
            self.rateOrDelay = "rate"
        
        self.progressBar = {0: "[..........]",
                            1: "[#.........]",
                            2: "[##........]",
                            3: "[###.......]",
                            4: "[####......]",
                            5: "[#####.....]",
                            6: "[######....]",
                            7: "[#######...]",
                            8: "[########..]",
                            9: "[#########.]",
                           10: "[##########]",}
        
        if self.firstVal == self.minVal:
            self.direction = "INC"
        elif self.firstVal == self.maxVal:
            self.direction = "DEC"
        
        
        self.conf_instr()
        
    def getRate(self):
        """
        Method to get the rate from the delay and the delta Value.
        
        Returns
        -------
        rate: float
            rate in volts[amps] per second.

        """
        rate =  (self.deltaVal / self.delay)
        return rate
    
    def getDeltaVal(self):
        self.deltaVal_n = 0
        self.deltaVal_p = 0
        
        """
        delta_value = self.rate / self.max_points_sec
        self.deltaVal = delta_value
        """
        
        #Define step size for incremental side.
        if self.maxVal != self.firstVal:
            self.value_window = self.maxVal - self.firstVal
            self.time_window = self.value_window / self.rate
            self.amnt_points_window = int(self.time_window * self.max_points_sec)
            self.deltaVal = self.value_window / (self.amnt_points_window-1)
        
            if self.mode.upper() == "POT":
                if self.deltaVal < 1e-3:
                    self.deltaVal = 1e-3
                    self.rate = self.deltaVal * self.max_points_sec
                    print("Required step value for the amount points smaller than 1mV.\
                          delta_value set to 1mV and rate set \
                          to {0}".format(self.rate))
                          
            self.deltaVal_p = self.deltaVal
        
        #Define step size for decremental side.
        if self.minVal != self.firstVal:
            self.value_window = self.firstVal - self.minVal
            self.time_window = self.value_window / self.rate
            self.amnt_points_window = int(self.time_window * self.max_points_sec)
            self.deltaVal = self.value_window / (self.amnt_points_window-1)
            
            if self.mode.upper() == "POT":
                if self.deltaVal < 1e-3:
                    self.deltaVal = 1e-3
                    self.rate = self.deltaVal * self.max_points_sec
                    print("Required step value for the amount points smaller than 1mV.\
                          delta_value set to 1mV and rate set \
                          to {0}".format(self.rate))
                          
            self.deltaVal_n = self.deltaVal
        
        self.deltaVal = np.asarray([self.deltaVal_p, self.deltaVal_n])
        
        return self.deltaVal 

            
        
    def conf_instr(self):
        """
        Method to create attributes and configure CDB for sweeping measurement.
        """
        
        #Seting mode and range
        self.cdb.setMode(self.mode)
        self.cdb.setRange(self.iRange)
        
        if self.rateOrDelay[0].upper() == "D":
            print("\nIdeal rate of experiment {0}".format(self.getRate()))
            if type(self.deltaVal) != list and type(self.deltaVal) != np.ndarray:
                self.deltaVal = [self.deltaVal, self.deltaVal]
            
            if type(self.deltaVal) != np.ndarray:
                self.deltaVal = np.asarray(self.deltaVal)
            
        else:
            self.rate = float(self.rate)
            self.getDeltaVal()
            self.delay = 0
        
        
        #Attributes required for working.
        self.timeStamp = []
        self.setPoint = []
        self.voltage = []
        self.current = []
        
        #Create setPoint list
        
        if self.direction.upper() == "INC":  
            self.setPoint = self.createWSP(self.minVal, self.maxVal,
                                           self.deltaVal, self.firstVal)
                
        elif self.direction.upper() == "DEC":
            deltaValDec = -1*self.deltaVal[::-1]
            self.setPoint = self.createWSP(self.maxVal, self.minVal,
                                           deltaValDec, self.firstVal)

        
        #To create all the required cycles
        initialSetPoints = self.setPoint
        initialDeltaT = self.deltaT
        
        #To readjust the amount of points per cycle to the real value
        self.amnt_points = len(initialSetPoints)
        
        for i_cycle in range(1, self.cycles):
            self.setPoint = self.setPoint + initialSetPoints
            self.deltaT = self.deltaT + initialDeltaT
            
        #To create the IdealTimeStamp
        self.idealTimeStamp = [self.deltaT[0]]
        for i_time in range(1,len(self.deltaT)):
            self.idealTimeStamp.append(self.idealTimeStamp[i_time-1]
                                       + self.deltaT[i_time])
            

        #Create configuration Messsage:
        msg_cv_mode = "\nCV Mode: {0}\n".format(self.mode)
        msg_val_range = "Value range: [{0:e}, {1:e}]\n".format(self.minVal,
                                                               self.maxVal)
        msg_step_size_p = "Delta value positive: {0:e}\n".format(self.deltaVal[0])
        msg_step_size_n = "Delta value negative: {0:e}\n".format(self.deltaVal[1])
        msg_iRange = "Current range: {0}\n".format(self.iRange)
        msg_first="First value: {0:e}\n".format(self.firstVal)
        msg_hold="Hold value: {0:.3}s\n".format(self.hold)
        msg_delay="Delay between steps: {0:.3}\n".format(float(self.delay))
        msg_rate="Sweeping rate: {0} V(P) or A(G) per s\n".format(self.rate)
        msg_amnt_points="Amount of data points per cycles: {0}\n".format(self.amnt_points)
        msg_amnt_cycles="Amount of cycles : {0}\n".format(self.cycles)
        msg_direction="Sweeping Direction: {0}\n".format(self.direction)
        
        self.conf_msg = msg_cv_mode + msg_val_range + msg_direction\
                        + msg_step_size_p + msg_step_size_n + msg_iRange\
                        + msg_first + msg_hold\
                        + msg_delay + msg_rate + msg_amnt_points\
                        + msg_amnt_cycles + "\n\nComments:\n" + self.comment           
    
    def createWSP(self, minVal, maxVal, step, startValue=0):
        """
        Method to create the working setpoints to be measured.

        Parameters
        ----------
        minVal : float
            minimum value to go to.
        maxVal : float
            maximum value to achieve.
        step : float
            Steps in between the setpoints.
        startValue : float, optional
            Value to start. The default is 0.

        Returns
        -------
        float
            List with the values of the set points.

        """
        oneSideSweep="NA"
        wsp=[]
        deltaT=[]
        
        if minVal==startValue:
            oneSideSweep="inc"
        elif maxVal==startValue:
            oneSideSweep="dec"
        
        maxVal = maxVal + step[0]/10
        minVal = minVal - step[1]/10
        
        if oneSideSweep=="NA" or oneSideSweep=="inc":
            wsp_p = np.arange(startValue, maxVal, step[0])
            
            if type(self.rate) != str:
                deltaT_p = [abs(self.deltaVal[0]/self.rate) for x in wsp_p]
            else:
                deltaT_p = [self.delay for x in wsp_p]
            
            wsp=np.concatenate((wsp_p[:-1], wsp_p[::-1]))
            deltaT=np.concatenate((deltaT_p[:-1], deltaT_p[::-1]))
            

        if oneSideSweep=="NA" or oneSideSweep=="dec":                  
            wsp_n = np.arange(startValue, minVal, -1*step[1])
            
            if type(self.rate) != str:
                deltaT_n = [abs(self.deltaVal[1]/self.rate) for x in wsp_n]
            else:
                deltaT_n = [self.delay for x in wsp_n]
        
            wsp=np.concatenate((wsp, wsp_n[1:-1], wsp_n[::-1]))
            deltaT=np.concatenate((deltaT, deltaT_n[1:-1], deltaT_n[::-1]))
        
        self.deltaT = list(deltaT)
        
        return list(wsp)

    def meas(self):
        """
        Method to execute a measureme. does not save the data to a file. 
        only run the measurement.
        """
        #Attributes required for working.
        self.timeStamp = []
        self.voltage = []
        self.current = []
        self.iRangeMeas = []
        self.progress = 0
        amnt_setPoints = len(self.setPoint)
        
        #Starting measurement
        self.cdb.setMode(self.mode)
        self.cdb.setRange(self.iRange)
        time.sleep(0.5)
        
        #Message to tool LCD
        if self.lcd_enable:
            self.cdb.lcdBackLight("b")
            if self.mode == "POT":
                self.cdb.lcdMessage("SWP:[{0:1.1f}V,{1:1.1f}V] ".format(self.minVal, self.maxVal))
            else:
                self.cdb.lcdMessage("SWP:{0:1.0e},{1:1.0e}   ".format(self.minVal, self.maxVal))

        #Printed informationto the console
        print("\n*********************************************")
        print("Starting value: {0}".format(self.firstVal))
        print("Measurement interval [min, max]: [{0},{1}]".format(self.minVal,
                                                                  self.maxVal))
        print("Amount of points per cycles: {0}".format(self.amnt_points))
        print("Amount of cycles: {0}".format(self.cycles))
        print("Duration of measurement: {0:3f}s".format(self.hold + 
                                                    self.idealTimeStamp[-1]))
        
        print("")
        
        
        
        #Initial hold
        self.cdb.setSource(self.firstVal)
        time.sleep(self.hold)
        
        #CV measurement for the case delay is specified
        if type(self.rate) == str:
            if self.delay <= (self.cdb.conf.meas_delay + self.cdb.conf.time_delta):
                timeZero = time.time()
                
                for workingSetPoint in self.setPoint:
                    self.cdb.setSource(workingSetPoint)
                    [v_meas_val, i_meas_val, i_range_val] = self.cdb.dMeas();
                    self.voltage.append(v_meas_val)
                    self.current.append(i_meas_val)
                    self.iRangeMeas.append(i_range_val)
                    self.timeStamp.append(time.time()-timeZero)
                    
                    #Printing progress to console
                    self.progress = self.progress + 1
                    print("\rProgress: {0} {1:.1f}%".format(self.progressBar[int(self.progress/amnt_setPoints*10)],
                                                            self.progress/amnt_setPoints*100), end="")
            else:
                timeZero = time.time()
                
                for workingSetPoint in self.setPoint:
    
                    self.cdb.setSource(workingSetPoint)
                    time.sleep(self.delay)
                    [v_meas_val, i_meas_val, i_range_val] = self.cdb.dMeas(); 
                    self.voltage.append(v_meas_val)
                    self.current.append(i_meas_val)
                    self.iRangeMeas.append(i_range_val)
                    self.timeStamp.append(time.time()-timeZero)
                    
                    #Printing progress to console
                    self.progress = self.progress + 1
                    print("\rProgress: {0} {1:.1f}%".format(self.progressBar[int(self.progress/amnt_setPoints*10)],
                                                            self.progress/amnt_setPoints*100), end="")
        
        
        #CV measurement for the case rate is specified
        if type(self.rate) != str:          
            
            
            timeZero = time.time()
            for i_setPoint in range(len(self.setPoint)):
                workingSetPoint = self.setPoint[i_setPoint]
                self.cdb.setSource(workingSetPoint)
                [v_meas_val, i_meas_val, i_range_val] = self.cdb.dMeas();
                time_meas = time.time()-timeZero
                time_present = time_meas
                
                #To wait for the correct time to get the requried rate
                while time_present < self.idealTimeStamp[i_setPoint]:
                    time_present = time.time()-timeZero
                    
                self.voltage.append(v_meas_val)
                self.current.append(i_meas_val)
                self.iRangeMeas.append(i_range_val)
                self.timeStamp.append(time_meas)
                
                #Printing progress to console
                self.progress = self.progress + 1
                print("\rProgress: {0} {1:.1f}%".format(self.progressBar[int(self.progress/amnt_setPoints*10)],
                                                 self.progress/amnt_setPoints*100), end="")
                
                
        print("\n*********************************************")
        
        #Message to tool LCD
        self.cdb.lcdBackLight("g")
        self.cdb.lcdMessage(" Sweep Finished    ")
        
        self.data = [self.timeStamp,self.voltage,self.current,self.iRangeMeas]
            
        date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        

        
        self.rate_exp = abs(np.diff(self.voltage) / np.diff(self.timeStamp)).mean()
        
        msg_rate_exp="\n\nExperimental rate: {0}\n".format(self.rate_exp)
        msg_time="Total time: {0}\n".format(self.timeStamp[-1])
        
        self.file_comments = date_time + "\n" + self.conf_msg + msg_rate_exp + msg_time
    
    def run(self):
        """
        Method for runing a CV measure. The configuration must be runned first
        by using the method conf_instr(). This will create (or replace) the 
        file specified with the parameter filename.
        

        Returns
        -------
        list
            [timeStamp, setPoint, voltage, current, iRange]

        """
        
        self.meas()

        self.writeFile()

        return [self.timeStamp, self.setPoint, self.voltage,
        self.current, self.iRangeMeas]
    

    
    def append(self):
        """
        Method for runing a CV measure. The configuration must be runned first
        by using the method conf_instr(). This will append to an existing file 
        specified with the parameter filename.
        

        Returns
        -------
        list
            [timeStamp, setPoint, voltage, current, iRange]

        """
        self.meas()

        self.writeFile(append=True)

        return [self.timeStamp, self.setPoint, self.voltage,
        self.current, self.iRangeMeas]
    
    def writeFile(self, append = False):
        """
        Method to write the content of self.timeStamp, self.voltage, self.current, self.i_rangeMeas,
        to a file specified by self.path + self.filename.
        """
        DMeas = [self.timeStamp, self.voltage, self.current, self.iRangeMeas]
    
        fh.export_csv(name=self.path + self.filename + ".txt",
                      data=DMeas,
                      headers=["Time", "Voltage", "Current", "Range"],
                      units=["s", "V", "A", "NA"],
                      cmt_start=self.file_comments, 
                      delimiter="\t",
                      append=append)
    
    def plot(self):
        self.fig = plotCV(self.data, self.comment, fname=self.path+self.filename)
    

#---------------------------------------------------------------------
#Plot 
#---------------------------------------------------------------------
class plotCV:
    """
    Class to create a plot of the data adquired.
    """
    
    def __init__(self, data, title, fname="./graph"):
        
        self.data = data
        self.filename = fname
        self.plot_enable = True
        
        self.plot_x = "VRS"
        self.plot_y = "IWE"
        
        self.title_font = {'fontname': 'Arial',
                           'size': '16',
                           'color': 'black',
                           'weight': 'normal',
                           'verticalalignment': 'bottom'}
        
        self.axis_font = {'fontname': 'Arial', 'size': '16'}
        self.ticks_text_size = 15
        
        self.border_width = 2
        self.width = 20
        self.height = 15
        self.units = 15
        self.title = "Cyclic-voltammetry plot: " + title 
        
        self.matplotlib_backend = "qt5Agg"
        
        self.getPlot()


    def getPlot(self):
            
        #Creating plots   
        self.plot = gp.plotCV(vwc=self.data[1],
                              iw=self.data[2],
                              style="lin",
                              title = self.title,
                              plot = False)
        
        self.plot.title_font = self.title_font
        self.plot.axis_font = self.axis_font
        self.plot.ticks_text_size = self.ticks_text_size
        self.plot.border_width = self.border_width
        

        
        if not(self.plot_enable):
            matplotlib.use("Agg")
        else:
            matplotlib.use(self.matplotlib_backend)

        
        self.plot.plot()
        
        #saving pdf
        plt_name = self.filename + ".pdf"
        gp.save(self.plot.fig, plt_name,
                width=self.width,
                height=self.height,
                units=self.units,
                format="pdf")
        
        #saving png
        plt_name = self.filename + ".png"
        gp.save(self.plot.fig, plt_name,
                width=self.width,
                height=self.height,
                units=self. units,
                format="png")
