## CV lesson 10 homework
We are going to use and compare two different trackers CSRT vs MIL, and compare the results.
Test in difficult conditions when objects move in a turn and their appearance changes quickly.

### Results
**MIL** - Not very robust, can lose track when object easily changes in size and shape.  
**CSRT** - was much better but with default parameters also lost object in the last 2 frames.

### Tuning
**MIL** - did not support tuning its parameters.

**CSRT** - some tuning of `filter_lr` parameter made it possible to track the object for all 10 frames.  
If `filter_lr` is high (~0.23 compared to default 0.02 )
- The model quickly adapts to the new quick changed view, the tracker holds the object.
- This is risky when we have occlusion, and tracker may follow wrong object.
- But in this case, camera captures a top-down perspective of the racetrack, and the likelihood of object occlusion is minimal.
"""
