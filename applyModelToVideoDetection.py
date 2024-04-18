import cv2
import tensorflow as tf
import numpy as np
 
# Load the pre-trained YOLO model
#net = cv2.dnn.readNet('yolov3.weights', 'yolov3.cfg')

# Open the video capture
cap = cv2.VideoCapture('path/to/video.mp4')
    
model = tf.keras.models.load_model('/path/to/model')

while True:
    # Read a frame from the video
    ret, frame = cap.read()
    if not ret:
        break #die if we dont have video

    # Resize and normalize the frame to match the input shape of the model
    resized_frame = cv2.resize(frame, (640, 480))   
    resized_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
    resized_frame = np.expand_dims(resized_frame, axis=0) / 255.0  

    predictions = model.predict(resized_frame)

    # Print 0 or 1 
    print(round(predictions[0]))

# Clean up: Release video capture and c
       
    #Exit program
    cap.release()
    cv2.destroyAllWindows()