#TRACY HUNTER,TIM LY, ANDREW SILVA, CAMERON HAYES
#NUTRIENT ANALYZER
#4/28/2022

import serial
import io
import time
import seabreeze
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ser = serial.Serial('/dev/ttyUSB0')

                                # TIME VARIABLES

t0 = 0.001                              # time for running pumps simutaneously
t1 = 2                                  # sleep time for valve movement and pump pause
t3 = 300                                # flow cell wait time for absorbance measurement (5 mins.)
flushtime = 8                           # flush sequence time needed for pumps to run
blanktime = 12
molybdatetime = 12
po4sampletime = 12
po4standardtime = 12
ascorbicacidtime = 12
flowcelltime = 18

                                #CHEM VALVE PORT VARIABLES

#Port Positions
port_p1 = 960                            #Waste Port position (Currently not in use)
port_p2 = 720                            #Flow Cell position
port_p3 = 480                            #Molybdate position
port_p4 = 240                            #PO4 Sample position
port_p5 = 0                              #Ascorbic Acid position
port_p6 = 1200                           #PO4 Standard position

                                # PUMP VARIABLES
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


                                #CHEM VALVE PORT POSITION FUNCTIONS

def port_1():
        print("Moving to port 1")               

        port_1_pos ='AMA '+ str(port_p1)+'\r\n'
        port1position = bytes(port_1_pos,'UTF-8')
        ser.write(port1position)                        #Position of port 1 relative to absolute position at initiliziation
        time.sleep(t1)                                  #Not used at this time

def port_2():
        print("Moving to port 2")           

        port_2_pos ='AMA '+ str(port_p2)+'\r\n'
        port2position = bytes(port_2_pos,'UTF-8')
        ser.write(port2position)                        #Position of port 2 relative to absolute position at initiliziation
        time.sleep(t1)                                  #Wait for n seconds

def port_3():
        print("Moving to port 3")           

        port_3_pos ='AMA '+ str(port_p3)+'\r\n'
        port3position = bytes(port_3_pos,'UTF-8')
        ser.write(port3position)                        #Position of port 3 relative to absolute position at initiliziation
        time.sleep(t1)                                  #Wait for n seconds

def port_4():
        print("Moving to port 4")          

        port_4_pos ='AMA '+ str(port_p4)+'\r\n'
        port4position = bytes(port_4_pos,'UTF-8')
        ser.write(port4position)                        #Position of port 4 relative to absolute position at initiliziation
        time.sleep(t1)                                  #Wait for n seconds

def port_5():
        print("Moving to port 5")       

        port_5_pos ='AMA '+ str(port_p5)+'*EU\r\n'
        port5position = bytes(port_5_pos,'UTF-8')
        ser.write(port5position)                        #Position of port 5 relative to absolute position at initiliziation
        time.sleep(t1)                                  #Wait for n seconds

def port_6():
        print("Moving to port 6")       
        
        port_6_pos ='AMA '+ str(port_p6)+'\r\n'
        port6position = bytes(port_6_pos,'UTF-8')
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

#This section refers to external pump and lightsouce control

#def external_pump():
        #Place code here

#def lightsource():
        #place code here

#This section refers to Spectrometer scanning

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

        return samp_spec, samp_lambdas
    
def spectro_calcAbsorbace(dark_spec,ref_spec,samp_spec,samp_lambas):
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

        absorbances_unfiltered = np.log10((ref_spec - dark_spec) / (samp_spec - dark_spec))

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

        #plotting absorbance spectrum
        #plt.figure()
        #plt.plot(absorbances_final['wavelengths_filtered'],absorbances_final['absorbances_filtered'])
        #plt.ylabel('Absorbance Units')
        #plt.xlabel('Wavelength')
        #plt.xlim(600,1150)
        #plt.show()

        return abs_final

def blank_sample_run():
        port_2()
        system_flush()
        #NEED REFERENCE SCAN HERE
        ref_spec=spectro_refscan(spec)
        blank_sample()
        port_3()
        molybdate_reagent()
        port_5()
        ascorbic_acid_reagent()
        port_2()
        flow_cell()
        #ACQUIRE ABSORBANCE VALUE HERE
        samp_spec, samp_lambdas = spectro_samplescan(spec)[:]
        absorbance_blank=spectro+calcAbsorbance(dark_spec,ref_spec,samp_spec, samp_lambdas)    

def po4_standard_run():
        port_2()
        system_flush()
        #NEED REFERENCE SCAN HERE
        ref_spec=spectro_refscan(spec)
        port_6()
        po4_standard()
        port_3()
        molybdate_reagent()
        port_5()
        ascorbic_acid_reagent()
        port_2()
        flow_cell()
        #ACQUIRE ABSORBANCE VALUE HERE
        samp_spec, samp_lambdas = spectro_samplescan(spec)[:]
        absorbance_blank=spectro+calcAbsorbance(dark_spec,ref_spec,samp_spec, samp_lambdas)

def po4_sample_run():
        port_2()
        system_flush()
        #NEED REFERENCE SCAN HERE
        ref_spec=spectro_refscan(spec)
        # RUN AUXILLARY PUMP HERE FOR 60 secs
        port_4()
        po4_sample()
        port_3()
        molybdate_reagent()
        port_5()
        ascorbic_acid_reagent()
        port_2()
        flow_cell()
        #ACQUIRE ABSORBANCE VALUE HERE
        samp_spec, samp_lambdas = spectro_samplescan(spec)[:]
        absorbance_blank=spectro+calcAbsorbance(dark_spec,ref_spec,samp_spec, samp_lambdas)
#SPEC CODE

#Initialize Spec
from seabreeze.spectrometers import Spectrometer
spec = Spectrometer.from_first_available()
spec.integration_time_micros(38000) ##integration time in microseconds

#define monitoring and reference wavelengths to be used
monitoringlambda = 880
reflambda = 1050

#START OF CODE
#The system will run the blank sample sequence twice, then it will follow with the PO4 standard twice, then
#there will be one PO4 seawater sample run only once. The system will then post process to calculate the
#the PO4 concentration. The system will then sleep for ~40 mins., then run only the PO4 seawater sample again, followed by
#and additional sleep cycle. This will be repeated again, then calibration process will be restarted(Running the complete
#code from the beginning)

#(Maybe set up a for loop with sequences to follow specific sampling steps which will resest itself after 3 hours)
        # ACTIVATE INSTRUMENT
        #turn on analyzer
        #turn of light
        #get dark scan
        #turn lamp on
        #wait 3 minutes for lamp to warm up
#darkspec
#dark_spec=seafcn.darkscan(spec)

#RUN BLANK SAMPLE (This will be done twice)
#RUN PO4 STANDARD (This will be done twice)
#RUN PO4 SAMPLE (This will be done once)
#POST PROCESS HERE

        #NEED REFERENCE SCAN HERE
        #ref_spec=seafcn.referencescan(spec)
        #ACQUIRE ABSORBANCE VALUE HERE
        #samp_spec, samp_lambdas = seafcn.samplescan(spec)[:]
        #absorbance_blank=seafcn.absorbance(dark_spec,ref_spec,samp_spec, samp_lambdas)   
ser.close()

