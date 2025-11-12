### Contactless Computer Interaction (based on gaze direction tracking)

### Equipment:

A standard laptop with a built-in webcam.

### Goal (MVP):

Detect the user’s gaze direction and identify one cell out of a 10×10 grid on the screen.

### Project Plan:

1. Collect ground truth data using MediaPipe (FaceMesh + Iris) while the user looks at predefined points on the screen.
2. Prepare and save the dataset for model training and validation.
3. Design and train a CNN-based gaze estimation model to predict gaze direction.
4. (option, not realized) Develop a prototype application that tracks gaze direction on the laptop screen divided into a 10×10 grid in real time.
