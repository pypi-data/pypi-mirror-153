__all__ = ["MeterDigitsRecognizer"]

import os
import cv2
import torch
import numpy as np
from meter_digits_recognizer._net import Net

PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))


class MeterDigitsRecognizer:

    def __init__(self):
        self.net = Net()
        state_dict = torch.load(os.path.join(PACKAGE_DIR, "model_weights.pt"), map_location="cpu")
        self.net.load_state_dict(state_dict)

    def run(self, digit_imgs):
        digits_batch = torch.cat([self.net.test_transform(cv2.resize(img,
            self.net.input_size, interpolation=cv2.INTER_LINEAR)).unsqueeze(0) for img in digit_imgs], 0)
        with torch.no_grad():
            outputs = self.net.forward(digits_batch) 
        all_confidences = torch.nn.functional.softmax(outputs, 1).numpy()
        predictions = np.argmax(all_confidences, axis=1)
        confidences = all_confidences[np.arange(len(predictions)), predictions]
        return predictions, confidences

if __name__ == "__main__":
    pass
