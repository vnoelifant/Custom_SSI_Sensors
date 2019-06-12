# -*- coding: utf-8 -*-
"""
Estimate Relaxation from Band Powers

This example shows how to buffer, epoch, and transform EEG data from a single
electrode into values for each of the classic frequencies (e.g. alpha, beta, theta)
Furthermore, it shows how ratios of the band powers can be used to estimate
mental state for neurofeedback.

The neurofeedback protocols described here are inspired by
*Neurofeedback: A Comprehensive Review on System Design, Methodology and Clinical Applications* by Marzbani et. al

Adapted from https://github.com/NeuroTechX/bci-workshop
"""

import os
import sys
sys.path.append(os.environ.get('PYTHONPATH', ''))

import numpy as np  # Module that simplifies computations on matrices
import matplotlib.pyplot as plt  # Module used for plotting
from pylsl import StreamInlet, resolve_byprop  # Module to receive EEG data


""" EEG EXPERIMENTAL PARAMETERS """
# Modify these to change aspects of the signal processing

# Length of the EEG data buffer (in seconds)
# This buffer will hold last n seconds of data and be used for calculations
BUFFER_LENGTH = 5

# Length of the epochs used to compute the FFT (in seconds)
EPOCH_LENGTH = 1

# Amount of overlap between two consecutive epochs (in seconds)
OVERLAP_LENGTH = 0.8

# Amount to 'shift' the start of each next consecutive epoch
SHIFT_LENGTH = EPOCH_LENGTH - OVERLAP_LENGTH

# Index of the channel(s) (electrodes) to be used
# 0 = left ear, 1 = left forehead, 2 = right forehead, 3 = right ear
#INDEX_CHANNEL = [0]

# A very large time value (ca. 1 year); can be used in timeouts.
FOREVER = 32000000.0

""" 1. CONNECT TO EEG STREAM """

# Search for active LSL streams
print('Looking for an EEG stream...')
streams = resolve_byprop('type', 'EEG', timeout=2)
if len(streams) == 0:
    raise RuntimeError('Can\'t find EEG stream.')

# Set active EEG stream to inlet and apply time correction
print("Start acquiring data")
inlet = StreamInlet(streams[0], max_chunklen=12)
eeg_time_correction = inlet.time_correction()

# Get the stream info and description
info = inlet.info()
description = info.desc()
#print("EEG stream info: ",info)
#print("EEG stream description: ",description)

# number of EEG channels
chan_cnt = info.channel_count()
print("EEG channel count: ",chan_cnt)

# Get the sampling frequency
# This is an important value that represents how many EEG data points are
# collected in a second. This influences our frequency band calculation.
# for the Muse 2016, this should always be 256
fs = int(info.nominal_srate())
print("EEG fs: ",fs)

def getOptions(opts, vars):
    
    #opts['sr'] = fs
    #opts['dim'] = chan_cnt
    pass

# eeg channel(s) (electrodes) to be used
# ['TP9', 'AF7', 'AF8', 'TP10', 'Right AUX']
# 0 = left ear, 1 = left forehead, 2 = right forehead, 3 = right ear
def getChannelNames(opts, vars):
    
    return { 'eeg' : 'a brain wave signal with 5 electrodes' }


def initChannel(name, channel, types, opts, vars):

    if name == 'eeg':
        #print("eeg",name)
        channel.dim = chan_cnt # 5
        channel.type = types.FLOAT
        channel.sr = fs #256

    else:
        print('uh oh, unkown channel name')


def connect(opts, vars):
    pass

        
def read(name, sout, reset, board, opts, vars): 
    time = sout.time
    delta = 1.0 / sout.sr  

    """ ACQUIRE DATA """
    # Obtain EEG data from the LSL stream
    # channel(s) (electrodes) to be used are:  # ['TP9', 'AF7', 'AF8', 'TP10', 'Right AUX']
    # Following indeces are below per channel name:
    # 0 = left ear, 1 = left forehead, 2 = right forehead, 3 = right ear, 4 = right aux

 
    # method pull_chunk pulls a chunk of samples from the inlet
    # Returns a tuple (samples,timestamps) where samples is a list of samples 
    # (each itself a list of values), and timestamps is a list of time-stamps
    # (list of list of samples where each sample is a list of 5 channels)
    # eeg_chunk, timestamp = inlet.pull_chunk(timeout=1, max_samples=int(SHIFT_LENGTH * fs))
    
    # method pull_sample pulls a sample from the inlet and returns it
    # Returns a tuple (sample,timestamp) where
    # sample is a list of channel values
    # timestamp is the capture time of the sample on the remote 
    # machine, or (None,None) if no new sample was available. 
    eeg_sample, timestamp = inlet.pull_sample(timeout=FOREVER, sample=None)
    print("Number of samples:", sout.num)
    # length of eeg samples (each sample is a list of 5 channels)
    print("Number of Dimensions",sout.dim)
    for n in range(sout.num):
        for d in range(sout.dim):
            #sout[n,d] = eeg_chunk[n][d]
            sout[n,d] = eeg_sample[d]
            print("EEG Channel Number: ",d,"EEG Sample Number: ",n, "EEG Value: ",sout[n,d])
        time += delta

def disconnect(opts, vars):
    pass
