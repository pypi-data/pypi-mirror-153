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


class pulse:
    """
    Application to execute a train of source values (current or voltage)
    with an specific duration.

    Parameters
    ----------
    filename: string
        Filename for the plot and and the txt file. For the path it can be
        changed directly in the attribute or put inside the filename.
    
    cdb : core.api_cdb
        Handler to an instance of a caonabo driving board.
    
    sourceVal : list float
        Values of the source (current or voltage) for each step.
    
    iRange :  integer or list of integers
        From 0 to 5 in agreement with the ideal range for current meas. 
        If it is an integer the value will be use for all the steps.
        if a list of integers is specified it must be in agreement with
        number of elements in the sourceVal list.
    
    duration : list float
        Duration in seconds for each step. The amount of elements of the
        list should be in agreement with the sourceVal. This value have to
        be bigger than the measurement delay value (180ms for adquiring
        voltage and current)
    
    mode : string, optional
        To select the working mode as POTentiostat of GALvanostat.
        The default is "POT".
        
    daqValues : string
        Values to be adquired for each off the steps. Can be "V"
        for the voltage, "I" for recording the current, "C" for
        temperature in centigrades, and "F" for the temperature in
        farenheit (The temperature in the DriveBox for measurement
        correction). Time in seconds is alwyas returned.
    
    cycles : integer, optional
        Amount of repetitions of the sweeping cycle. The default is 1.
    
    comment: string
        Comment to be added to the data file and fhe figure.
        
    lcd_enable : boolean
        To choose weather or not to refresh the status line of the caonabo
        DriveBox during the measurements.
    
    plot : boolean
        To enable (dissable) the automatic ploting of the data.
    """
    
    def __init__(self, filename, cdb, sourceVal, iRange, duration,
                 mode="POT", daqValues="VI", cycles=1, comment="",
                 lcd_enable=True, plot = True):
        
        #Creating attributes from parameters        
        self.filename = filename
        self.cdb = cdb
        self.sourceVal = sourceVal #list values in Volts or Ampers.
        self.iRange = iRange #list range for the measurement of I (from 0 - 4)
        self.duration = duration #list duration of steps in Seconds
        self.mode = mode.upper()
        self.daqValues = daqValues.upper()
        self.cycles = cycles
        self.comment = comment #in S
        self.lcd_enable = lcd_enable #in v/S
        self.plot_enable = plot
        self.path = ""
                
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
        
        self.conf_instr()
        
    def conf_instr(self):
        """
        Method to create attributes and configure CDB for pulse measurement.
        """
        self.amntSteps = len(self.sourceVal)
        
        # converting single entries to list
        if type(self.iRange) != list:
            self.iRange = [self.iRange for x in range(self.amntSteps)]
            
        if type(self.duration) != list:
            self.duration = [self.duration for x in range(self.amntSteps)]
        
        if type(self.iRange) != list:
            self.iRange = [self.iRange for x in range(self.amntSteps)]
            
        #Data header and units configuration
        self.dataHeaders = ["Time"]
        self.dataUnits = ["s"]
        
        for param in self.daqValues:
            if param == "V":
                self.dataHeaders.append("Voltage")
                self.dataUnits.append("V")
            elif param == "I":
                self.dataHeaders.append("Current")
                self.dataHeaders.append("Range")
                self.dataUnits.append("A")
                self.dataUnits.append("NA")
            elif param == "C":
                self.dataHeaders.append("Temperature")
                self.dataUnits.append("C")
            elif param == "F":
                self.dataHeaders.append("Teperature")
                self.dataUnits.append("F")
        
        #Setting the mode
        self.cdb.setMode(self.mode)
        
        #Estimation of total duration
        self.totalDuration = 0 #In seconds
        for stepDuration in self.duration:
            self.totalDuration = self.totalDuration + stepDuration
        
        self.totalDuration = self.totalDuration * self.cycles
            
        #Create configuration message
        msg_cdb_mode = "\nCV Mode: {0}\n".format(self.mode)
        msg_amntSteps = "Amount of steps: {0}".format(self.amntSteps)
        msg_valueSteps = "Steps values: {0}\n".format(self.sourceVal)
        msg_iRangeSteps = "Steps Current Range: {0}\n".format(self.iRange)
        msg_durationSteps = "Steps duration: {0}\n".format(self.duration)
        msg_cycles = "Amount of cycles: {0}\n".format(self.cycles)
        msg_daqValues = "Adquired values per step: {0}\n".format(self.daqValues)
        
        self.conf_msg = msg_cdb_mode +\
                        msg_amntSteps +\
                        msg_valueSteps +\
                        msg_iRangeSteps +\
                        msg_durationSteps +\
                        msg_cycles +\
                        msg_daqValues + "\n\nComments:\n" + self.comment   
        
    def meas(self):
        """
        Method to execute a measureme. does not save the data to a file. 
        only run the measurement.
        """
        #Configure insrtument
        self.conf_instr()

        self.timeStamp = []
        self.data = []
        
        #Starting measurement
        self.cdb.setMode(self.mode)
        
        #Message to tool LCD
        if self.lcd_enable:
            self.cdb.lcdBackLight("b")
            self.cdb.lcdMessage("PUL:{0}stp, {1}cyc] ".format(self.amntSteps, self.cycles))

        #Printed informationto the console
        print("\n*********************************************")
        print("Steps values: {0}".format(self.sourceVal))
        print("Steps duration: {0}".format(self.duration))
        print("Amount of steps per cycles: {0}".format(self.amntSteps))
        print("Amount of cycles: {0}".format(self.cycles))
        print("Duration of measurement: {0:3f}s".format(self.totalDuration))
        
        print("")
        
        
        #Measurement execution
        timeZero = time.time()
        self.progress = 0
        
        for cycle in range(self.cycles):
            for iStep in range(self.amntSteps):
                self.cdb.setRange(self.iRange[iStep])
                self.cdb.setSource(self.sourceVal[iStep])
                
                #data adquisition loop
                stepStartTime = time.time()
                while (time.time() - stepStartTime) < self.duration[iStep]:
                    measTime = time.time() - timeZero
                    self.timeStamp.append(measTime)
                    self.data.append(self.cdb.meas(self.daqValues))
                    
                    #Printing progress to console
                    self.progress = measTime/self.totalDuration
                    if self.progress > 1:
                        self.progress = 1
                    
                    print("\rProgress: {0} {1:.1f}%".format(self.progressBar[int(self.progress*10)], self.progress*100), end="")
                    
        print("\n*********************************************")
        
        #Message to tool LCD
        self.cdb.lcdBackLight("g")
        self.cdb.lcdMessage(" Pulse Finished    ")
        
        #Organizing data with same format as the sweep and sampling
        self.data = [self.timeStamp, *list(np.asarray(self.data).transpose())]
            
        date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        msg_time="Total time: {0}\n".format(self.timeStamp[-1])
        
        self.file_comments = date_time + "\n" + self.conf_msg +  msg_time
    
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

        return [self.dataHeaders, self.dataUnits, self.data]
    
    
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

        return [self.dataHeaders, self.dataUnits, self.data]
    
    def writeFile(self, append = False):
        """
        Method to write the content of self.data,
        to a file specified by self.path + self.filename.
        """
    
        fh.export_csv(name=self.path + self.filename + ".txt",
                      data=self.data,
                      headers=self.dataHeaders,
                      units=self.dataUnits,
                      cmt_start=self.file_comments, 
                      delimiter="\t",
                      append=append)
        
    def plot(self):
        self.fig = []
        time = self.data[0]
        
        for i in range(1,len(self.daqValues)+1):
            yHeader = self.dataHeaders[i]
            yUnits = self.dataUnits[i]
            y = self.data[i]
            
            self.fig.append(plotYT(y,
                                   yHeader,
                                   yUnits,
                                   time,
                                   self.comment,
                                   fname=self.path+self.filename+self.dataHeaders[i]))
    

#---------------------------------------------------------------------
#Plot 
#---------------------------------------------------------------------
class plotYT:
    """
    Class to create a plot of the data adquired.
    """
    
    def __init__(self, y, yHeader, yUnits, time, title, fname="./graph"):
        
        self.yUnits = yUnits
        self.yHeader = yHeader
               
        self.filename = fname
        self.plot_enable = True
        
        self.plot_x = time
        self.plot_y = y
        
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
        self.title = "Time dependent plot: " + title 
        
        self.matplotlib_backend = "qt5Agg"
        
        self.getPlot()


    def getPlot(self):
            
        #Creating plots   
        self.plot = gp.plotCV(vwc=self.plot_x,
                              iw=self.plot_y,
                              style="lin",
                              title = self.title,
                              plot = False,
                              label_x="Time",
                              units_x="s",
                              label_y=self.yHeader,
                              units_y=self.yUnits)
        
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
