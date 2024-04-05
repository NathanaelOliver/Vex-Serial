import cv2

# LOAD MODEL FROM FILE
#will be our model not downloaded from online
#model = 

# Open the video capture
cap = cv2.VideoCapture('path/to/video.mp4')

while True:
    # Read a frame from the video
    ret, frame = cap.read()
    if not ret:
        break #die if we dont have video

    # preproccess the frame
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
    model.setInput(blob)

    # Forward pass through the model to get the detections
    detections = model.forward()

    #Class names from either a file or just write them here
    class_names = {"tri_ball","goalpost","wall"}
    # Process the detections
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:
            class_id = int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * [frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]]
            (x1, y1, x2, y2) = box.astype("int")

            # Draw a bounding box and label
            label = f"{class_names[class_id]}: {confidence * 100:.2f}%"
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (36, 255, 12), 2)

    # Display frame
    cv2.imshow("Object Detection", frame)


# Release the video capture and close all windows
cap.release()
cv2.destroyAllWindows()