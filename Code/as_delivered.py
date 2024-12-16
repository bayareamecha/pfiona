#TRACY HUNTER,TIM LY, ANDREW SILVA
#NUTRIENT ANALYZER MLML Test
#5/10/2022

from ast import While
from pickle import TRUE
import serial                           
import io                              
import time                            
import seabreeze                       
import pandas as pd                    
import numpy as np                     
import matplotlib.pyplot as plt        
import RPi.GPIO as GPIO                
ser = serial.Serial('/dev/ttyUSB0')


                                # SPECTROMETER INITIALIZATION VARIABLES

from seabreeze.spectrometers import Spectrometer
spec = Spectrometer.from_first_available()
spec.integration_time_micros(50000) ##integration time in microseconds

#define monitoring and reference wavelengths to be used
monitoringlambda = 880
reflambda = 600

known_concentration = 2

 

                                #CHEM VALVE PORT VARIABLES

#Port Positions
port_p1 = 1340                          # Waste Port position (Currently not in use)
port_p2 = 1090                          # Flow Cell position
port_p3 = 840                           # Molybdate position
port_p4 = 590                           # PO4 Sample position
port_p5 = 350                           # Ascorbic Acid position
port_p6 = 130                           # PO4 Standard position

                                # PUMP SPEED VARIABLES
#System Flush
flush_p1_speed = 150                    # pump 1 speed in uL/sec      
flush_p1_amount = 1000                  # pump 1 amount in uL (+ for dispense, - for aspirate)
flush_p2_speed = 150                    # pump 2 speed in uL/sec
flush_p2_amount = 1000                  # pump 2 amount in uL (+ for dispense, - for aspirate)         

#Blank Sample
blank_p1_speed = 60                     # pump 1 speed in uL/sec 
blank_p1_amount = 600                   # pump 1 amount in uL (+ for dispense, - for aspirate)

#Molybdate Reagent
molybdate_p1_speed = 32                 # pump 1 speed in uL/sec 
molybdate_p1_amount = 320               # pump 1 amount in uL (+ for dispense, - for aspirate)
molybdate_p2_speed = 40                 # pump 2 speed in uL/sec
molybdate_p2_amount = -400              # pump 2 amount in uL (+ for dispense, - for aspirate)

#Ascorbic Acid Reagent
ascorbic_p1_speed = 40                  # pump 1 speed in uL/sec
ascorbic_p1_amount = -400               # pump 1 amount in uL (+ for dispense, - for aspirate)
ascorbic_p2_speed = 32                  # pump 2 speed in uL/sec
ascorbic_p2_amount = 320                # pump 2 amount in uL (+ for dispense, - for aspirate)

#Flow Cell
flow_cell_p1_speed = 25                 # pump 1 speed in uL/sec
flow_cell_p1_amount = 400               # pump 1 amount in uL (+ for dispense, - for aspirate)

#PO4 Standard
po4_standard_p1_speed = 60              # pump 1 speed in uL/sec
po4_standard_p1_amount = -600           # pump 1 amount in uL (+ for dispense, - for aspirate)

#PO4 Sample
po4_sample_p1_speed = 60                # pump 1 speed in uL/sec
po4_sample_p1_amount = -600             # pump 1 amount in uL (+ for dispense, - for aspirate)

                                # PUMP PRIMING VARAIBLES

totalprimes = 2                         # indicates number of times prime cycle should repeat (set by end-user)

port1_pp1speed = 100                    # port 1, pump 1, priming speed in uL/sec
port1_pp1amount = 1000                  # port 1, pump 1, priming amount uL (+ for dispense, - for aspirate)

port2_pp1speed = 150                    # port 2, pump 1, priming speed in uL/sec
port2_pp1amount = 2000                  # port 2, pump 1, priming amount uL (+ for dispense, - for aspirate)
port2_pp2speed = 150                    # port 2, pump 2, priming speed in uL/sec
port2_pp2amount = 2000                  # port 2, pump 1, priming amount uL (+ for dispense, - for aspirate)

port3_pp1speed = 100                    # port 3, pump 1, priming speed in uL/sec
port3_pp1amount = -200                  # port 3, pump 1, priming amount uL (+ for dispense, - for aspirate)

port4_pp1speed = 100                    # port 4, pump 1, priming speed in uL/sec
port4_pp1amount = -200                  # port 4, pump 1, priming amount uL (+ for dispense, - for aspirate)

port5_pp1speed = 100                    # port 5, pump 1, priming speed in uL/sec
port5_pp1amount = -200                  # port 5, pump 1, priming amount uL (+ for dispense, - for aspirate)

port6_pp1speed = 100                    # port 6, pump 1, priming speed in uL/sec
port6_pp1amount = -200                  # port 6, pump 1, priming amount uL (+ for dispense, - for aspirate)




                                # TIME VARIABLES

t0 = 0.001                              # time for running pumps simutaneously
t1 = 3                                  # sleep time for valve movement and pump pause ( may be adjusted to suit end-user needs)
t3 = 30                                 # flow cell wait time for absorbance measurement (set based on end-user needs)
auxtime = 5                             # aux pump time for drawing sample seawater to refill sample (set based on end-user needs)
darkscantime = 5
refscantime = 5
flushtime = abs(flush_p1_amount/flush_p1_speed)+t1                              # This area calculates the time needed for pumps to run.
blanktime = abs(blank_p1_amount/blank_p1_speed)+t1                              # It takes the absolute value of the pump 1 ratio of amount
molybdatetime = abs(molybdate_p1_amount/molybdate_p1_speed)+t1                  # of volume to move and the speed at which the volume is moved.
po4sampletime = abs(po4_sample_p1_amount/po4_sample_p1_speed)+t1                # This is done to ensure accurate numbers due to dispensing and
po4standardtime = abs(po4_standard_p1_amount/po4_standard_p1_speed)+t1          # aspirating values being +-. This value is then added to sleep
ascorbicacidtime = abs(ascorbic_p1_amount/ascorbic_p1_speed)+t1                 # time for valve movement and pump pause to ensure adequate time
flowcelltime = abs(flow_cell_p1_amount/flow_cell_p1_speed)+t1                   # for sequence to finish.
p1primetime = abs(port1_pp1amount/port1_pp1speed)+t1   
p2primetime = abs(port2_pp1amount/port2_pp1speed)+t1
p3primetime = abs(port3_pp1amount/port3_pp1speed)+t1
p4primetime = abs(port4_pp1amount/port4_pp1speed)+t1
p5primetime = abs(port5_pp1amount/port5_pp1speed)+t1
p6primetime = abs(port6_pp1amount/port6_pp1speed)+t1

                                #AUX MOTOR AND LIGHTSOURCE PIN CALLOUT

motorPin=17                             # Define Pins for aux motor and lightsource
ledPin=27

GPIO.setmode(GPIO.BCM)                  
GPIO.setup(motorPin,GPIO.OUT)           # Set aux motor pin to output
GPIO.setup(ledPin,GPIO.OUT)             # Set lightsouce to ouput
GPIO.output(motorPin,GPIO.LOW)          # Aux motor output initial state of 0
GPIO.output(ledPin,GPIO.LOW)            # Lightsource output initial state of 0


                                #CHEM on VALVE PORT POSITION FUNCTIONS

def port_1():
        print("Moving to port 1")               

        port_1_pos ='AMA '+ str(port_p1)+'\r\n'         #Uses port_1 variable. AMA is absolute position from 0 refernce on valve.
        port1position = bytes(port_1_pos,'UTF-8')       #Creates the output and encodes it 
        ser.write(port1position)                        #Sends encoded command to the Chem-on Valve
        time.sleep(t1)                                  #Wait for n seconds (based on end-user needs)

def port_2():
        print("Moving to port 2")           

        port_2_pos ='AMA '+ str(port_p2)+'\r\n'         #Uses port_2 variable. AMA is absolute position from 0 refernce on valve.
        port2position = bytes(port_2_pos,'UTF-8')       #Creates the output and encodes it
        ser.write(port2position)                        #Position of port 2 relative to absolute position at initiliziation
        time.sleep(t1)                                  #Wait for n seconds

def port_3():
        print("Moving to port 3")           

        port_3_pos ='AMA '+ str(port_p3)+'\r\n'         #Uses port_3 variable. AMA is absolute position from 0 refernce on valve.
        port3position = bytes(port_3_pos,'UTF-8')       #Creates the output and encodes it
        ser.write(port3position)                        #Position of port 3 relative to absolute position at initiliziation
        time.sleep(t1)                                  #Wait for n seconds

def port_4():
        print("Moving to port 4")          

        port_4_pos ='AMA '+ str(port_p4)+'\r\n'         #Uses port_4 variable. AMA is absolute position from 0 refernce on valve.
        port4position = bytes(port_4_pos,'UTF-8')       #Creates the output and encodes it
        ser.write(port4position)                        #Position of port 4 relative to absolute position at initiliziation
        time.sleep(t1)                                  #Wait for n seconds

def port_5():
        print("Moving to port 5")       

        port_5_pos ='AMA '+ str(port_p5)+'\r\n'         #Uses port_5 variable. AMA is absolute position from 0 refernce on valve.
        port5position = bytes(port_5_pos,'UTF-8')       #Creates the output and encodes it
        ser.write(port5position)                        #Position of port 5 relative to absolute position at initiliziation
        time.sleep(t1)                                  #Wait for n seconds

def port_6():
        print("Moving to port 6")       
        port_6_pos ='AMA '+ str(port_p6)+'\r\n'         #Uses port_6 variable. AMA is absolute position from 0 refernce on valve.
        port6position = bytes(port_6_pos,'UTF-8')       #Creates the output and encodes it
        ser.write(port6position)                        #Position of port 6 relative to absolute position at initiliziation
        time.sleep(t1)                                  #Wait for n seconds


                                        #SYSTEM FLUSH FUNCTION
def system_flush():
        print("System Flush In Progress")

        # This section encodes the parameters set from PUMP VARIABLES section for Flush pump 1 speed and amount

        p1_flush_speed ='CVM '+ str(flush_p1_speed)+'*EU\r\n'           
        flushp1speed = bytes(p1_flush_speed,'UTF-8')
        p1_flush_amount = 'CMR '+ str(flush_p1_amount)+'*EU\r\n'
        flushp1amount = bytes(p1_flush_amount,'UTF-8')

        # This section encodes the parameters set from PUMP VARIABLES section for Flush pump 2 speed and amount

        p2_flush_speed ='DVM '+ str(flush_p2_speed)+'*EU\r\n'
        flushp2speed = bytes(p2_flush_speed,'UTF-8')
        p2_flush_amount = 'DMR '+ str(flush_p2_amount)+'*EU\r\n'
        flushp2amount = bytes(p2_flush_amount,'UTF-8')


        ser.write(flushp1speed)                         #Pump 1 moves at speed set by flush_p1_speed variable
        ser.write(flushp1amount)                        #Pump 1 dispenses amount set by flush_p1_amount varaible
        time.sleep(t0)          
        ser.write(flushp2speed)                         #Pump 2 moves at speed set by flush_p2_speed variable
        ser.write(flushp2amount)                        #Pump 2 dispenses amount set by flush_p2_amount varaible
        time.sleep(flushtime)

                                        
                                        #DISPENSE/ASPIRATE FUNCTIONS

def blank_sample():
        print("Dispensing Blank Sample")    

        # This section encodes the parameters set from PUMP VARIABLES section for Blank pump 1 speed and amount

        p1_blank_speed ='CVM '+ str(blank_p1_speed)+'*EU\r\n'
        blankp1speed = bytes(p1_blank_speed,'UTF-8')
        p1_blank_amount = 'CMR '+ str(blank_p1_amount)+'*EU\r\n'
        blankp1amount = bytes(p1_blank_amount,'UTF-8')

        ser.write(blankp1speed)                         #Pump 1 moves at speed set by blank_p1_speed variable
        ser.write(blankp1amount)                        #Pump 1 dispenses amount set by blank_p1_amount varaible
        time.sleep(blanktime)                           #wait for n seconds

def molybdate_reagent():
        print("Dispensing 320 ul pump_1/ aspirating 400 ul pump_2") 

        # This section encodes the parameters set from PUMP VARIABLES section for Molybdate pump 1 speed and amount

        p1_molybdate_speed ='CVM '+ str(molybdate_p1_speed)+'*EU\r\n'
        molybdatep1speed = bytes(p1_molybdate_speed,'UTF-8')
        p1_molybdate_amount = 'CMR '+ str(molybdate_p1_amount)+'*EU\r\n'
        molybdatep1amount = bytes(p1_molybdate_amount,'UTF-8')

        # This section encodes the parameters set from PUMP VARIABLES section for Molybdate pump 2 speed and amount

        p2_molybdate_speed ='DVM '+ str(molybdate_p2_speed)+'*EU\r\n'
        molybdatep2speed = bytes(p2_molybdate_speed,'UTF-8')
        p2_molybdate_amount = 'DMR '+ str(molybdate_p2_amount)+'*EU\r\n'
        molybdatep2amount = bytes(p2_molybdate_amount,'UTF-8')

        ser.write(molybdatep1speed)                     #Pump 1 moves at speed set by molybdate_p1_speed variable
        ser.write(molybdatep1amount)                    #Pump 1 dispenses amount set by molybdate_p1_amount varaible
        time.sleep(t0)                       
        ser.write(molybdatep2speed)                     #Pump 2 moves at speed set by molybdate_p2_speed variable
        ser.write(molybdatep2amount)                    #Pump 2 aspirates amount set by molybdate_p2_amount varaible
        time.sleep(molybdatetime)                       #Wait for n seconds

def ascorbic_acid_reagent():
        print("Aspirating 400 ul pump_1/ Dispensing 320 ul pump_2") 

        #This section encodes the parameters set from PUMP VARIABLES section for Ascorbic Acid pump 1 speed and amount

        p1_ascorbic_speed ='CVM '+ str(ascorbic_p1_speed)+'*EU\r\n'
        ascorbicp1speed = bytes(p1_ascorbic_speed,'UTF-8')
        p1_ascorbic_amount = 'CMR '+ str(ascorbic_p1_amount)+'*EU\r\n'
        ascorbicp1amount = bytes(p1_ascorbic_amount,'UTF-8')

        # This section encodes the parameters set from PUMP VARIABLES section for Ascorbic Acid pump 2 speed and amount

        p2_ascorbic_speed ='DVM '+ str(ascorbic_p2_speed)+'*EU\r\n'
        ascorbicp2speed = bytes(p2_ascorbic_speed,'UTF-8')
        p2_ascorbic_amount = 'DMR '+ str(ascorbic_p2_amount)+'*EU\r\n'
        ascorbicp2amount = bytes(p2_ascorbic_amount,'UTF-8')
       

        ser.write(ascorbicp1speed)                      #Pump 1 moves at speed set by ascorbic_p1_speed variable
        ser.write(ascorbicp1amount)                     #Pump 1 aspirates amount set by ascorbic_p1_amount varaible
        time.sleep(t0)                      
        ser.write(ascorbicp2speed)                      #Pump 2 moves at speed set by ascorbic_p2_speed variable
        ser.write(ascorbicp2amount)                     #Pump 2 aspirates amount set by ascorbic_p2_amount varaible
        time.sleep(ascorbicacidtime)                    #Wait for n seconds

def flow_cell():
        print("Dispensing 400 ul pump_1 into flow cell")

        # This section encodes the parameters set from PUMP VARIABLES section for Flow Cell pump 1 speed and amount

        p1_flow_cell_speed ='CVM '+ str(flow_cell_p1_speed)+'*EU\r\n'           
        flowcellp1speed = bytes(p1_flow_cell_speed,'UTF-8')
        p1_flow_cell_amount = 'CMR '+ str(flow_cell_p1_amount)+'*EU\r\n'
        flowcellp1amount = bytes(p1_flow_cell_amount,'UTF-8')


        ser.write(flowcellp1speed)                      #Pump 1 moves at speed set by flow_cell_p1_speed variable
        ser.write(flowcellp1amount)                     #Pump 1 dispenses amount set by flow_cell_p1_amount varaible
        time.sleep(flowcelltime)                        #Wait for n seconds                                     

def po4_standard():
        print("Aspirating 600 ul pump_1 ")

        # This section encodes the parameters set from PUMP VARIABLES section for Po4 Standard pump 1 speed and amount

        p1_po4_standard_speed ='CVM '+ str(po4_standard_p1_speed)+'*EU\r\n'           
        po4standardp1speed = bytes(p1_po4_standard_speed,'UTF-8')
        p1_po4_standard_amount = 'CMR '+ str(po4_standard_p1_amount)+'*EU\r\n'
        po4standardp1amount = bytes(p1_po4_standard_amount,'UTF-8')

        ser.write(po4standardp1speed)                   #Pump 1 moves at speed set by po4_standard_p1_speed variable
        ser.write(po4standardp1amount)                  #Pump 1 aspirates amount set by po4_standard_p1_amount varaible
        time.sleep(po4standardtime)                     #Wait for n seconds

def po4_sample():
        print("Aspirating 600 ul pump_1 ")  

        # This section encodes the parameters set from PUMP VARIABLES section for Po4 Sample pump 1 speed and amount

        p1_po4_sample_speed ='CVM '+ str(po4_sample_p1_speed)+'*EU\r\n'           
        po4samplep1speed = bytes(p1_po4_sample_speed,'UTF-8')
        p1_po4_sample_amount = 'CMR '+ str(po4_sample_p1_amount)+'*EU\r\n'
        po4samplep1amount = bytes(p1_po4_sample_amount,'UTF-8')

        ser.write(po4samplep1speed)                     #Pump 1 moves at speed set by po4_sample_p1_speed variable
        ser.write(po4samplep1amount)                    #Pump 1 aspirates amount set by po4_sample_p1_amount varaible
        time.sleep(po4sampletime)                       #Wait for n seconds

                                        #SPECTOMETER FUNCTIONS
def spectro_darkscan(spec):
        #place code for darkscan
        '''
        Inputs:
        -Spectrophotometer read from Seabreeze Library

        Outputs:
        -Intensity values across all wavelengths taken with lamp off.
        '''

        time.sleep(10) #sleep 10s to ensure no light transmission after lamp turned off

        wavelengths = spec.wavelengths()
        intensities = spec.intensities()
        column_names = ['wavelengths','intensities']
        combine = np.vstack((wavelengths, intensities)).T
        np.shape(combine)

        darkscan = pd.DataFrame(data=combine, columns=column_names) #produces dataframe from most recent scan taken from spec.

        dark_spec = darkscan['intensities']

        plt.figure()
        plt.xlabel('Wavelength nm')
        plt.ylabel('Intensity')
        plt.title('Darkscan Calibration')
        plt.plot(wavelengths,dark_spec)
        plt.show()
        time.sleep(5)

        return dark_spec

def spectro_refscan(spec):
	#place code for reference scan
        '''
        Inputs:
        -Spectrophotometer read from Seabreeze Library
    
        Outputs:
        -Intensity values across all wavelengths taken with lamp on, no sample in flow cell.
        '''

        refscan_intensity = []

        samples_to_average = 20

        for i in range(samples_to_average):

            wavelengths = spec.wavelengths()
            intensities = spec.intensities()
            column_names = ['wavelengths','intensities']
            combine = np.vstack((wavelengths, intensities)).T
            np.shape(combine)
            refscan = pd.DataFrame(data=combine, columns=column_names) #produces dataframe from most recent scan taken from spec.

            refscan_intensity.append(refscan['intensities'])
            time.sleep(0.25)

        ref_spec = np.array(refscan_intensity).mean(axis=0)

        plt.figure()
        plt.xlabel('Wavelength nm')
        plt.ylabel('Intensity')
        plt.title('Reference Scan')
        plt.plot(wavelengths,intensities)
        plt.show()
        time.sleep(5)
        return ref_spec

def spectro_samplescan(spec):
        #place code for sample scans
        '''
        Inputs:
        -Spectrophotometer read from Seabreeze Library

        Outputs:
        -Intensity values across all wavelengths taken with lamp on, sample in flow cell.
        '''

        sampscan_intensity = []
   
        samples_to_average = 20

        for i in range(samples_to_average):

            wavelengths = spec.wavelengths()
            intensities = spec.intensities()
            column_names = ['wavelengths','intensities']
            combine = np.vstack((wavelengths, intensities)).T
            np.shape(combine)
            sampscan = pd.DataFrame(data=combine, columns=column_names) #produces dataframe from most recent scan taken from spec.

            sampscan_intensity.append(sampscan['intensities'])
   
            time.sleep(0.25)

        samp_spec = np.array(sampscan_intensity).mean(axis=0)

        samp_lambdas = sampscan['wavelengths']

        plt.figure()
        plt.xlabel('Wavelength nm')
        plt.ylabel('Intensity')
        plt.title('Sample Scan')
        plt.plot(wavelengths,intensities)
        plt.show()
        time.sleep(5)

        return samp_spec, samp_lambdas
    
def spectro_calcAbsorbance(dark_spec,ref_spec,samp_spec,samp_lambdas):

        '''
        This function uses outputs from the following functions for its input: "darkscan", "referencescan", "samplescan". Note that these functions must be run prior to running this function.

        The inputs are defined are follows:
        dark_spec = darkscan(spec)
        ref_spec = referencescan(spec)
        samp_spec, samp_lambdas = samplescan(spec)[:]

        Absorbance is calculated using the equation: A = log_10 (Io - dark signal / I - dark signal), where Io is the intensity from the reference scan, and I is the intensity from the sample scan.

        Outputs:
        -Final absorbance value to be used in calculating concentration of analyte.
        -Absorbance spectrum across all available wavelengths
        '''

        absorbances_unfiltered = np.log10((ref_spec - dark_spec) / (samp_spec - dark_spec))     #absorbance ranges 0 to 1

        ##smoothing spectrum using moving average
        window_size = 20
        numbers_series = pd.Series(absorbances_unfiltered)
        windows = numbers_series.rolling(window_size)
        moving_averages = windows.mean()
        moving_averages_list = moving_averages.tolist()
        absorbances_filtered = moving_averages_list[window_size - 1:]
        wavelengths_filtered = samp_lambdas[:-19]

        #organizing filtered outputs into dataframe
        column_names = ['wavelengths_filtered','absorbances_filtered']
        combine = np.vstack((wavelengths_filtered, absorbances_filtered)).T
        absorbances_final = pd.DataFrame(data=combine, columns=column_names)

        #calculating absorbance value at monitoring wavelength
        abs_monitoring = absorbances_final[(absorbances_final['wavelengths_filtered'] < (monitoringlambda + 1)) & (absorbances_final['wavelengths_filtered'] > (monitoringlambda - 1))]
        abs_monitoring_mean = np.mean(abs_monitoring['absorbances_filtered'])

        ##calculating absorbance value at reference wavelength
        abs_reference = absorbances_final[(absorbances_final['wavelengths_filtered'] < (reflambda + 1)) & (absorbances_final['wavelengths_filtered'] > (reflambda - 1))]
        abs_reference_mean = np.mean(abs_reference['absorbances_filtered'])

        abs_final = abs_monitoring_mean - abs_reference_mean
        print('abs_final')
        print(abs_final)

        #plotting absorbance spectrum

        plt.figure()
        plt.ylabel('Absorbance')
        plt.xlabel('Wavelength (nm)')
        plt.title('Sample Absorbance')
        plt.xlim(400,1000)
        plt.plot(absorbances_final['wavelengths_filtered'],absorbances_final['absorbances_filtered'])
        plt.show()
        time.sleep(5)

        return abs_final

                                        #SYSTEM PRIMING FUNCTION
def port_1prime():
        port_1()
        port1_primep1speed ='CVM '+ str(port1_pp1speed)+'*EU\r\n'           
        port1primep1speed = bytes(port1_primep1speed,'UTF-8')
        port_1primep1amount = 'CMR '+ str(port1_pp1amount)+'*EU\r\n'
        port1primep1amount = bytes(port_1primep1amount,'UTF-8')
        ser.write(port1primep1speed)
        ser.write(port1primep1amount)
        time.sleep(p1primetime)

def port_2prime():
        port_2()
        port2_primep1speed ='CVM '+ str(port2_pp1speed)+'*EU\r\n'           
        port2primep1speed = bytes(port2_primep1speed,'UTF-8')
        port_2primep1amount = 'CMR '+ str(port2_pp1amount)+'*EU\r\n'
        port2primep1amount = bytes(port_2primep1amount,'UTF-8')

        port2_primep2speed ='DVM '+ str(port2_pp2speed)+'*EU\r\n'           
        port2primep2speed = bytes(port2_primep2speed,'UTF-8')
        port_2primep2amount = 'DMR '+ str(port2_pp2amount)+'*EU\r\n'
        port2primep2amount = bytes(port_2primep2amount,'UTF-8')

        ser.write(port2primep1speed)
        ser.write(port2primep1amount)
        time.sleep(t0)
        ser.write(port2primep2speed)
        ser.write(port2primep2amount)
        time.sleep(p2primetime)

def port_3prime():
        port_3()
        port3_primep1speed ='CVM '+ str(port3_pp1speed)+'*EU\r\n'           
        port3primep1speed = bytes(port3_primep1speed,'UTF-8')
        port_3primep1amount = 'CMR '+ str(port3_pp1amount)+'*EU\r\n'
        port3primep1amount = bytes(port_3primep1amount,'UTF-8')
        ser.write(port3primep1speed)
        ser.write(port3primep1amount)
        time.sleep(p3primetime)

def port_4prime():
        port_4()
        port4_primep1speed ='CVM '+ str(port4_pp1speed)+'*EU\r\n'           
        port4primep1speed = bytes(port4_primep1speed,'UTF-8')
        port_4primep1amount = 'CMR '+ str(port4_pp1amount)+'*EU\r\n'
        port4primep1amount = bytes(port_4primep1amount,'UTF-8')
        ser.write(port4primep1speed)
        ser.write(port4primep1amount)
        time.sleep(p4primetime)

def port_5prime():
        port_5()
        port5_primep1speed ='CVM '+ str(port5_pp1speed)+'*EU\r\n'           
        port5primep1speed = bytes(port5_primep1speed,'UTF-8')
        port_5primep1amount = 'CMR '+ str(port5_pp1amount)+'*EU\r\n'
        port5primep1amount = bytes(port_5primep1amount,'UTF-8')
        ser.write(port5primep1speed)
        ser.write(port5primep1amount)
        time.sleep(p5primetime)

def port_6prime():
        port_6()
        port6_primep1speed ='CVM '+ str(port6_pp1speed)+'*EU\r\n'           
        port6primep1speed = bytes(port6_primep1speed,'UTF-8')
        port_6primep1amount = 'CMR '+ str(port6_pp1amount)+'*EU\r\n'
        port6primep1amount = bytes(port_6primep1amount,'UTF-8')
        ser.write(port6primep1speed)
        ser.write(port6primep1amount)
        time.sleep(p6primetime)

def prime():
        for i in range(totalprimes):
                port_1()
                port_2prime()
                port_1prime()
                port_3prime()
                port_1prime()
                port_4prime()
                port_1prime()
                port_5prime()
                port_1prime()
                port_6prime()
                port_1prime()
                auxMotor()
        print('Prime Complete')

                                        #AUX MOTOR AND LIGHTSOURCE FUNCTIONS
def auxMotor():
        print('Aux start')
        GPIO.output(motorPin,GPIO.HIGH)
        time.sleep(auxtime)
        GPIO.output(motorPin,GPIO.LOW)
        print('Aux stopped')
        time.sleep(t1)

def lightOn():
        GPIO.output(ledPin,GPIO.HIGH)
        print('Light On')

def lightOff():
        GPIO.output(ledPin,GPIO.LOW)
        print('Light Off')

                                        #BLANK/STANDARD/SAMPLE RUN FUNCTIONS
def blank_sample_run():
        port_1()
        port_2()
        system_flush()
        lightOff()
        time.sleep(darkscantime)
        dark_spec=spectro_darkscan(spec)
        lightOn()
        time.sleep(refscantime)
        ref_spec=spectro_refscan(spec)

        blank_sample()
        port_3()
        molybdate_reagent()
        port_5()
        ascorbic_acid_reagent()
        port_2()
        flow_cell()
        samp_spec, samp_lambdas = spectro_samplescan(spec)[:]
        absorbance_blank=spectro_calcAbsorbance(dark_spec,ref_spec,samp_spec, samp_lambdas)
        return absorbance_blank

def po4_standard_run():
        port_1()
        port_2()
        system_flush()
        lightOff()
        time.sleep(darkscantime)
        dark_spec=spectro_darkscan(spec)
        lightOn()
        time.sleep(refscantime)
        ref_spec=spectro_refscan(spec)
        

        port_6()
        po4_standard()
        port_3()
        molybdate_reagent()
        port_5()
        ascorbic_acid_reagent()
        port_2()
        flow_cell()
        samp_spec, samp_lambdas = spectro_samplescan(spec)[:]
        absorbance_po4std=spectro_calcAbsorbance(dark_spec,ref_spec,samp_spec, samp_lambdas)
        return absorbance_po4std

def po4_sample_run():
        port_1()
        port_2()
        system_flush()
        lightOff()
        time.sleep(darkscantime)
        dark_spec=spectro_darkscan(spec)
        lightOn()
        time.sleep(refscantime)
        ref_spec=spectro_refscan(spec)


        auxMotor()
        port_4()
        po4_sample()
        port_3()
        molybdate_reagent()
        port_5()
        ascorbic_acid_reagent()
        port_2()
        flow_cell()
        samp_spec, samp_lambdas = spectro_samplescan(spec)[:]
        absorbance_po4samp=spectro_calcAbsorbance(dark_spec,ref_spec,samp_spec, samp_lambdas)
        lightOff()
        return absorbance_po4samp


#START OF CODE
#The system will run the blank sample sequence twice, then it will follow with the PO4 standard twice, then
#there will be one PO4 seawater sample run only three times. The system will then post process to calculate the
#the PO4 concentration. The system will then sleep for ~40 mins., then run only the PO4 seawater sample again, followed by
#and additional sleep cycle. This will be repeated again, then calibration process will be restarted(Running the complete
#code from the beginning)

#po4_sample_run()
#auxMotor()
blank = [0, 0]
stand = [0,0]
sample = [0,0,0]
po4conc_array=[]
#blank_sample_run()
while TRUE:

        for i in range(2):
                #blank_sample_run()
                blank[i]= blank_sample_run()

        for i in range(2):
                #po4_standard_run()
                stand[i] = po4_standard_run()

        mean_abs_blank=(blank[0]+blank[1])/2
        mean_abs_stand=(stand[0]+stand[1])/2

        for i in range(3):
                #po4_sample_run()
                sample[i]=po4_sample_run()      
                po4conc=(sample(i)-mean_abs_blank)*(known_concentration/(mean_abs_stand-mean_abs_blank))
                po4conc_array.append(po4conc)


GPIO.cleanup()
ser.close()
