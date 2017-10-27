"""
Preprocessing pipeline
10/27/l7
Convert data from XML format -> dataframe
"""
import pandas as pd
import numpy as np
from bs4 import *

"""Load data"""
filename = 'sample_data.txt'
data = open(filename,'r')
soup = BeautifulSoup(data,'lxml')

"""Pre-process label for each example"""
#Create dictionary to assign encoded integer to each class.
classes = ['LFT','TooBig','NoRead','ValidDim','MultiRead','Irreg','TooSmall','Gap']
class_dict = {classes[i]:i for i in range(len(classes))}

#Extract and encode contents of condition field only for conditions listed in the `classes` list
conditions = [[class_dict[c] for c in obj.condition.contents[0].split(',') if c in classes]\
              for obj in soup.find_all('objectdata')]
##Perform one-hot-encoding
#Initialize matrix
conditions_encoded = np.zeros([len(conditions),len(classes)])
#Encode position in matrix for place of class
for c in range(len(conditions)):
    conditions_encoded[c,conditions[c]] = 1
#Store in dataframe
label_df = pd.DataFrame(conditions_encoded,columns=classes).astype(int)

"""Extract relevant information from each field for all objects"""
cols = ['date', 'time', 'height', 'width', 'length', 'volume', 'weight', 'angle', 'velocity', 'velocity_units',
        'belt_velocity', \
        'belt_velocity_units']
# Initialize dictionary for storing extracted data
data = {}
for obj in soup.find_all('objectdata'):
    # Time stamp
    [date, time] = obj.timestamp.contents[0].split('T')
    data
    # Gap information
    gap = float(obj.oga.value.contents[0])
    # Item volume
    vol_keys = ['ohe', 'owi', 'ole']
    [height, width, length] = [float(obj.volumetric.size.attrs[key]) for key in vol_keys]
    vol = height * width * length
    vol_units = obj.volumetric.size.attrs['unit']
    # Item angle
    angle = int(obj.volumetric.oa.value.contents[0])
    # Item Velocity
    vel = int(obj.volumetric.otve.value.contents[0])
    vel_units = obj.volumetric.otve.attrs['unit']
    # Item weight
    weight = float(obj.scaledata.value.contents[0])  # In lbs
    # Conveyor belt velocity
    belt_vel = float(obj.sorterstate.speed.value.contents[0])
    belt_vel_units = obj.sorterstate.speed.attrs['unit']

    # Add data to dictionary
    d = [date, time, height, width, length, vol, weight, angle, vel, vel_units, belt_vel, belt_vel_units]
    for k, v in zip(cols, d):
        # Initialize each entry with an empty list and then append new value
        data[k] = data.get(k, []) + [v]
# Construct dataframe
df = pd.DataFrame(data)
# Add labels
df = df.join(label_df)
# Save as csv
# df.to_csv('sampledata.csv', index=False)