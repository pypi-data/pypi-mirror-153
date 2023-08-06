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


class sampling:
    """
    Application to run a CV measurement using the onboard source
    measurement unit of the CDB.

    Parameters
    ----------
    filename: string
        Filename for the plot and and the txt file. for the path it can be
        changed directly in the attribute.
    cdb : core.api_cdb
        Handler to an instance of a caonabo driving board.
    firstVal : float
        First value for holding before sampling. (Volts or Amps).   
    value : float
        Value to be aplied for starting the sweeping (Volts or Amps).
    iRange : integer
        From 0 to 5 in agreement with the ideal range for current meas.
    duration : float
        duration time in seconds.
    hold : float, optional
        Holding time in seconds at "firstVal" before starting sweep.
        The default is 1.
    amnt_points: integer, optional
        Amount of points per cycle. can not be larger than: 
        [duration]/meas_delay - (meas_delay aprox. 170ms)
    mode : string, optional
        To select the working mode as POTentiostat of GALvanostat.
        The default is "POT".
    conf : configuration
        Configuration for the app. Any configuration can be pass.
    
    comment: string
        Comment to be added to the data file and fhe figure.
    """
    def __init__(self, filename, cdb, firstVal, value, iRange, duration=0, hold=1,
                 amnt_points=100, mode="POT", comment="", lcd_enable = True):

        
        
        #Creating attributes from parameters        
        self.cdb = cdb
        self.firstVal = float(firstVal)
        self.value = float(value)
        self.iRange = iRange
        self.duration = float(duration)
        self.hold = float(hold)
        self.amnt_points = amnt_points
        self.mode = mode
        self.path = ""
        self.filename = filename
        self.comment = comment
        self.lcd_enable = lcd_enable
        
        self.conf_instr()
        
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
                
    def getDelay(self):
        """
        Method to get the delay from amount of points and duration.

        Returns
        -------
        delay between measurement: float
            delay in second.

        """
        self.delay = self.duration/self.amnt_points
        
        if self.delay <= self.cdb.conf.meas_delay:
            
            self.delay = self.cdb.conf.meas_delay
            self.amnt_points = int(self.duration/self.cdb.conf.meas_delay)
            
            cm1 = "Amount of points to high for required sampling duration. "
            cm2 = "Setting maximum possible amount at that duration: "
            cm3 = "{0}".format(self.amnt_points)
            
            print(cm1 + cm2 + cm3)
            
        return self.delay
    
           
            
        
    def conf_instr(self):
        """
        Method to create attributes and configure CDB for sampling measurement.
        """
        self.getDelay()
        
        #Attributes required for working.
        self.timeStamp = []
        self.setPoint = []
        self.voltage = []
        self.current = []
        
            
        #Create configuration Messsage:
        
        msg_cv_mode = "\nCV Mode: {0}\n".format(self.mode)
        msg_value = "Value: {0:1.2e}\n".format(self.value)
        msg_iRange = "Current range: {0}\n".format(self.iRange)
        msg_first="First value: {0:1.2e}\n".format(self.firstVal)
        msg_hold="Hold value: {0:.3}s\n".format(self.hold)
        msg_duration="Duration value: {0:.3}s\n".format(self.duration)
        msg_amnt_points="Amount of data points per cycles: {0}\n".format(self.amnt_points)
        
        self.conf_msg = msg_cv_mode + msg_value\
                        + msg_iRange + msg_first + msg_hold + msg_duration\
                        + msg_amnt_points + "\n\nComments:\n" + self.comment           
    def meas(self):
        
        #Attributes required for working.
        self.timeStamp = []
        self.voltage = []
        self.current = []
        self.iRangeMeas = []
        self.progress = 0
        
        #Message to tool LCD
        if self.lcd_enable:
            self.cdb.lcdBackLight("b")
            if self.mode == "POT":
                self.cdb.lcdMessage("SMP:{0:1.1f}s @ {1:1.1f}V ".format(self.duration, self.value))
            else:
                self.cdb.lcdMessage("SMP:{0:1.1f}s@{1:1.0e}A   ".format(self.duration, self.value))
        
        
        #Printed informationto the console
        print("\n*********************************************")
        print(self.conf_msg)
        
        print("")
        
        #Starting measurement
        self.cdb.setMode(self.mode)
        self.cdb.setRange(self.iRange)

        
        #Initial hold
        self.cdb.setSource(self.firstVal)
        time.sleep(self.hold)
        
        #sampling measurement
        
        self.cdb.setSource(self.value)
        
        if self.delay <= (self.cdb.conf.meas_delay + self.cdb.conf.time_delta):
            timeZero = time.time()
            present_time = 0
            
            while(present_time <= self.duration):
                [v_meas_val, i_meas_val, i_range_meas] = self.cdb.dMeas();
                self.voltage.append(v_meas_val)
                self.current.append(i_meas_val)
                self.iRangeMeas.append(i_range_meas)
                present_time = time.time()-timeZero
                self.timeStamp.append(present_time)
                
                #Printing progress to console
                if present_time <= self.duration:
                    self.progress = present_time
                else:
                    self.progress = self.duration
                print("\rProgress: {0} {1:.1f}%".format(self.progressBar[int(self.progress/self.duration*10)],
                                                        self.progress/self.duration*100), end="")
        else:
            timeZero = time.time()
            present_time = 0
            
            while(present_time <= self.duration):
                [v_meas_val, i_meas_val, i_range_meas] = self.cdb.dMeas();
                self.voltage.append(v_meas_val)
                self.current.append(i_meas_val)
                self.iRangeMeas.append(i_range_meas)
                present_time = time.time()-timeZero
                self.timeStamp.append(present_time)
                time.sleep(self.delay-self.cdb.conf.meas_delay)
            
                #Printing progress to console
                if present_time <= self.duration:
                    self.progress = present_time
                else:
                    self.progress = self.duration
                print("\rProgress: {0} {1:.1f}%".format(self.progressBar[int(self.progress/self.duration*10)],
                                                        self.progress/self.duration*100), end="")        
        
        print("\n*********************************************\n")
        
        #Message to tool LCD
        self.cdb.lcdBackLight("g")
        self.cdb.lcdMessage(" Samp Finished    ")
            
        self.data = [self.timeStamp,self.voltage,self.current,self.iRangeMeas]
            
        date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        self.file_comments = date_time + "\n" + self.conf_msg
    
    def run(self):
        
        self.meas()
        
        self.writeFile()

        return [self.timeStamp, self.setPoint, self.voltage,
        self.current, self.iRange]
    
    def append(self):
        
        self.meas()

        self.writeFile(append=True)

        return [self.timeStamp, self.setPoint, self.voltage,
        self.current, self.iRange]
    
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
        self.fig = plotSampling(self.data, self.comment, fname=self.path+self.filename)
    

#---------------------------------------------------------------------
#Plot 
#---------------------------------------------------------------------
class plotSampling:
    def __init__(self, data, title, fname="./graph"):
        
        self.data = data
        self.filename = fname
        self.plot_enable = True
        
        self.plot_x = "Time"
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
        self.title = "Sampling: " + title 
        
        self.matplotlib_backend = "qt5Agg"
        
        self.getPlot()


    def getPlot(self):
            
        #Creating plots   
        self.plot = gp.plotCV(vwc=self.data[0],
                              iw=self.data[2],
                              style="lin",
                              title = self.title,
                              plot = False,
                              label_x="Time",
                              label_y="Current WE",
                              units_x="s",
                              units_y="A")
        
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
    
        
    
    
        