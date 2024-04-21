import tensorflow as tf
from tensorflow.keras.layers import Conv2D, BatchNormalization, LeakyReLU, MaxPool2D, Flatten, Dense
from tensorflow.keras import Model
import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Conv2D, BatchNormalization, LeakyReLU, MaxPool2D, concatenate, UpSampling2D


def load_darknet_weights(model, weights_file):
    # Open the weights file
    with open(weights_file, 'rb') as f:
        # Skip the header (5 * 4 bytes) of the .weights file
        np.fromfile(f, dtype=np.int32, count=5)
        # Load the weights to the model layer by layer
        for layer in model.layers:
            if isinstance(layer, Conv2D):
                # Load weights for Conv2D layer
                load_conv_layer(layer, f)

def load_conv_layer(conv_layer, weights_file):
    # Load weights for the convolutional layer
    # Darknet stores weights in the format (out_channels, in_channels, height, width)
    # TensorFlow requires the format (height, width, in_channels, out_channels)
    # Transpose weights accordingly
    kernel_shape, bias_shape = [w.shape for w in conv_layer.get_weights()]
    kernel = np.fromfile(weights_file, dtype=np.float32, count=np.prod(kernel_shape))
    kernel = kernel.reshape(kernel_shape).transpose([2, 3, 1, 0])
    bias = np.fromfile(weights_file, dtype=np.float32, count=np.prod(bias_shape))
    conv_layer.set_weights([kernel, bias])

def build_yolo_model():
    # Define the YOLO architecture using TensorFlow Keras
    inputs = tf.keras.Input(shape=(416, 416, 3))
    x = Conv2D(32, (3, 3), strides=(2, 2), padding='same')(inputs)
    x = BatchNormalization()(x)
    x = LeakyReLU(alpha=0.1)(x)
    x = MaxPool2D(pool_size=(2, 2))(x)
    # Add more layers according to your YOLO architecture
    # ...

    outputs = Dense(1)(x)  # Example output layer, replace with your detection layer

    model = Model(inputs=inputs, outputs=outputs)
    return model

# Path to the Darknet .weights file
weights_file = 'yolo-obj_3000.weights'


def convolutional_layer(inputs, filters, size, stride, activation='leaky'):
    x = Conv2D(filters, size, strides=stride, padding='same')(inputs)
    x = BatchNormalization()(x)
    if activation == 'leaky':
        x = LeakyReLU(alpha=0.1)(x)
    return x

def yolo_convolutional_layer(inputs, filters, size, activation='linear'):
    x = Conv2D(filters, size, strides=1, padding='same')(inputs)
    if activation == 'linear':
        return x
    else:
        return LeakyReLU(alpha=0.1)(x)

def yolo_model(input_shape=(416, 416, 3), num_classes=3):
    inputs = tf.keras.Input(shape=input_shape)
    
    # Downsample path
    x = convolutional_layer(inputs, 32, 3, 2)
    x = convolutional_layer(x, 64, 3, 2)
    x = convolutional_layer(x, 64, 3, 1)
    route1 = x
    
    x = convolutional_layer(x, 32, 3, 1)
    x = convolutional_layer(x, 32, 3, 1)
    route2 = x
    
    x = concatenate([route2, route1])
    x = convolutional_layer(x, 64, 1, 1)
    route3 = x
    
    x = MaxPool2D(pool_size=(2, 2), strides=(2, 2))(x)
    x = convolutional_layer(x, 128, 3, 1)
    route4 = x
    
    x = convolutional_layer(x, 64, 3, 1)
    x = convolutional_layer(x, 64, 3, 1)
    route5 = x
    
    x = concatenate([route5, route4])
    x = convolutional_layer(x, 128, 1, 1)
    route6 = x
    
    x = MaxPool2D(pool_size=(2, 2), strides=(2, 2))(x)
    x = convolutional_layer(x, 256, 3, 1)
    route7 = x
    
    x = convolutional_layer(x, 128, 3, 1)
    x = convolutional_layer(x, 128, 3, 1)
    route8 = x
    
    x = concatenate([route8, route7])
    x = convolutional_layer(x, 256, 1, 1)
    route9 = x
    
    x = MaxPool2D(pool_size=(2, 2), strides=(2, 2))(x)
    x = convolutional_layer(x, 512, 3, 1)
    
    # YOLO head
    x = convolutional_layer(x, 256, 1, 1)
    x = convolutional_layer(x, 512, 3, 1)
    x = yolo_convolutional_layer(x, num_classes * 5, 1)
    
    # Upsample path
    x = convolutional_layer(route9, 128, 1, 1)
    x = UpSampling2D(size=(2, 2))(x)
    x = concatenate([x, route6])
    x = convolutional_layer(x, 256, 3, 1)
    x = yolo_convolutional_layer(x, num_classes * 5, 1)
    
    x = convolutional_layer(x, 128, 1, 1)
    x = UpSampling2D(size=(2, 2))(x)
    x = concatenate([x, route3])
    x = convolutional_layer(x, 256, 3, 1)
    x = yolo_convolutional_layer(x, num_classes * 5, 1)
    
    model = tf.keras.Model(inputs, x)
    
    return model

# Build the YOLO model
model = yolo_model()

# Print model summary
model.summary()


# Load Darknet weights into the model
load_darknet_weights(yolo_model, weights_file)

# Convert the YOLO model to TensorFlow Lite format
converter = tf.lite.TFLiteConverter.from_keras_model(yolo_model)
tflite_model = converter.convert()

# Save the TensorFlow Lite model to a file
with open('yolo_model.tflite', 'wb') as f:
    f.write(tflite_model)


