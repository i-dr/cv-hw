#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CV lesson 10 homework
We are going to use and compare two different trackers CSRT vs MIL, and compare the results.
Test in difficult conditions when objects move in a turn and their appearance changes quickly.

Result:
MIL - Not very robust, can lose track when object easily changes in size and shape.
CSRT - was much better but with default parameters also lost object in the last 2 frames.

Tuning:
MIL - did not support tuning its parameters.
CSRT - some tuning of filter_lr parameter made it possible to track the object for all 10 frames.
If filter_lr is high (~0.23 compared to default 0.02 ):
- The model quickly adapts to the new quick changed view, the tracker holds the object.
- This is risky when we have occlusion, and tracker may follow wrong object.
- But in this case, camera captures a top-down perspective of the racetrack, and the likelihood of object occlusion is minimal.
"""

import os
import cv2
import matplotlib
matplotlib.use('TkAgg') # backend adaptation for PyCharm IDE (disable inline mode)
from matplotlib import pyplot as plt


# Load the dataset
# to reduce diskspace dataset is already prepared in order to have every 10th frame from 25fps video
# in dataset we have 10 frames that corresponds about 3.60 sec of videostream
folder = 'data/input'
frames = os.listdir(folder)

# Sort (alphabetically) to ensure temporal consecutiveness
frames.sort()

start_frame = '2025-10-03_17-41-31.png'
frame_count = 10


def detected_object_bbox():
    # Let's assume the detector has detected an object
    x1, y1 = 523, 251
    x2, y2 = 578, 292
        
    width = x2 - x1
    height = y2 - y1
    return x1, y1, width, height

# Set up tracker
tracker_types = ['MIL','CSRT', 'CSRT_tuned']

def setup_tracker(tracker_type):    
    if tracker_type == 'MIL':
        tracker = cv2.TrackerMIL_create()
        path_out = 'data/output/MIL'
    
    if tracker_type == "CSRT":
        tracker = cv2.TrackerCSRT_create()
        path_out = 'data/output/CSRT'
    
    if tracker_type == "CSRT_tuned":
        params = cv2.TrackerCSRT_Params()
        params.filter_lr = 0.23               # default 0.02     
        tracker = cv2.TrackerCSRT_create(params)
        path_out = 'data/output/CSRT_tuned'
    return path_out, tracker

# Use trackers, generate output for comparing
for tracker_type in tracker_types:
     # Generate tracking template
    idx = frames.index(start_frame)
    img = cv2.imread(os.path.join(folder, frames[idx]))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Initialize tracker
    path_out, tracker = setup_tracker(tracker_type)
    bbox = detected_object_bbox()
    ok = tracker.init(img, bbox)    

    # Show tracker_type title
    plt.imshow(img)
    plt.text(20, 500, tracker_type, fontsize=36, fontweight='bold', color='red')
    plt.show(block=False), plt.draw()    
    plt.waitforbuttonpress(2)
    plt.clf()

    # Run the tracker for frame_count 
    for ii in range(idx, idx + frame_count):
        img = cv2.imread(os.path.join(folder, frames[ii]))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)    
        ok, bbox = tracker.update(img)
        print(ok, bbox)
    
        # Print the bounding box on the image
        x1, y1 = bbox[0], bbox[1]
        width, height = bbox[2], bbox[3]
        cv2.rectangle(img, (x1, y1), (x1+width, y1+height), (0, 255, 0), 2)
        
        # Show the tracker working
        plt.imshow(img)
        plt.show(block=False), plt.draw()    
        if ii == frame_count - 1 :
            plt.waitforbuttonpress(2.0)
        else:
            plt.waitforbuttonpress(0.5) 
        plt.clf()
    
        # Save each frame to folder dedicated to tracker
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        fname = 'frame_' + str(ii).zfill(2) + '.jpg'
        print('Save: ', os.path.join(path_out, fname))
        if not cv2.imwrite(os.path.join(path_out, fname), img):
            print('Image save failed')

    # destroy tracker for init() the same tracker with new parameters
    del tracker
    






