import cv2

# LOAD MODEL FROM FILE
#will be our model not downloaded from online
#model = 
# Load the pre-trained YOLO model
net = cv2.dnn.readNet('yolov3.weights', 'yolov3.cfg')

# Open the video capture
cap = cv2.VideoCapture('path/to/video.mp4')

while True:
    # Read a frame from the video
    ret, frame = cap.read()
    if not ret:
        break #die if we dont have video

    # preproccess the frame
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
    net.setInput(blob)

# Run the forward pass to get the output layer
    output_layers = net.getUnconnectedOutLayersNames()
    layer_outputs = net.forward(output_layers)

     boxes, confidences, class_ids = [], [], []
     
    for output in layer_outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
            #If confident there is a triball, create the bounding box from detection 
                center_x, center_y, w, h = detection[0:4] * np.array([width, height, width, height])
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, int(w), int(h)])
                confidences.append(float(confidence))#save confidence
                class_ids.append(class_id)#add a label

    # Draw the bounding boxes and labels, create labels from class_id
    for i in range(len(boxes)):
        box = boxes[i]
        x, y, w, h = box
        label = str(classes[class_ids[i]])
        confidence = confidences[i]
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(img, f"{label} ({confidence:.2f})", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.imshow("Object Detection", frame)
    #Exit program
    cap.release()
    cv2.destroyAllWindows()