# About

This libary is developed for recognizing utility meter digits by using neural network classifier (see the image). The neural network is implemented in Pytorch and the details are available in the [code](meter_digits_recognizer/_net.py). 

The datset (from [here](https://github.com/jomjol/neural-network-digital-counter-readout) + self-made images) has 959 images that are classified into eleven categories: digits "0"-"9" and "10" for cases where digit is not recognizable.

![](example_output.png)

# Installation

1. Install PyTorch by following the official guidelines https://pytorch.org/get-started/locally/
2. Install from PyPI `pip install meter-digits-recognizer`

# Usage

Minimal example:

```python
import cv2
from meter_digits_recognizer import MeterDigitsRecognizer

# Read image, must be in BGR format (standard in OpenCV)
image = cv2.imread("images/0/1_hot_water_meter_20210212_065239.jpg")

# Run recognizer
dr = MeterDigitsRecognizer()
predictions, confidences = dr.run([image]) # Accepts list of images

# Print
print("Prediction %d (confidence %.1f %%)" % (predictions[0], confidences[0]))
```

Expected output:

```
Prediction 0 (confidence 100.0 %)
```

For additional examples see [example.ipynb](example.ipynb)

# Traing

To retrain the neural network follow the steps in the [train_neural_net.ipynb](train_neural_net.ipynb) notebook.

# Credits

* https://github.com/jomjol/neural-network-digital-counter-readout (dataset & inspiration) 
