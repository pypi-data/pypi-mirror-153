import PIL
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as transforms

__all__ = ["Net"]


class Net(nn.Module):
    test_transform = transforms.Compose([
        transforms.ToTensor()
    ]) 

    if hasattr(transforms, "InterpolationMode"):
        interp_kwargs = dict(interpolation=transforms.InterpolationMode.BILINEAR)
    else:
        interp_kwargs = dict(resample=PIL.Image.BILINEAR)
    train_transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.ColorJitter(brightness=0.1),
        transforms.RandomAffine(5.0,  translate=(0.1, 0.1), scale=(1.0, 1.2),
            ),
    ])

    def __init__(self):
        nn.Module.__init__(self)
        self.n_filters1 = 64
        self.n_filters2 = 64
        self.n_filters3 = 128
        self.n_filters4 = 128
        self.n_fc1 = 256
        self.n_fc2 = 128
        self.n_fc_input = 5 * 2 * self.n_filters4
        self.input_size = (20, 32)
      
        self.batchnorm = nn.BatchNorm2d(3)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv1 = nn.Conv2d(3, self.n_filters1, 3, padding=0)
        self.conv2 = nn.Conv2d(self.n_filters1, self.n_filters2, 3, padding=0)
        self.conv3 = nn.Conv2d(self.n_filters2, self.n_filters3, 3, padding=0)
        self.conv4 = nn.Conv2d(self.n_filters3, self.n_filters4, 3, padding=0)
        self.fc1 = nn.Linear(self.n_fc_input, self.n_fc1)
        self.fc2 = nn.Linear(self.n_fc1, self.n_fc2)
        self.fc3 = nn.Linear(self.n_fc2, 11)

    def forward(self, x):
        x = self.batchnorm(x)
        
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = self.pool(x)
        
        x = F.relu(self.conv3(x))
        x = F.relu(self.conv4(x))
        x = self.pool(x)
        
        x = x.view(-1, self.n_fc_input)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x
