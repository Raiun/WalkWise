import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

class Gait1DCNN(nn.Module):
    def __init__(self, num_classes=3):
        super(Gait1DCNN, self).__init__()
        # Input shape: [batch_size, 6, 500]
        self.conv1 = nn.Conv1d(
            in_channels=6, out_channels=64, kernel_size=3, stride=1, padding=1
        )
        self.pool = nn.MaxPool1d(kernel_size=2, stride=2, padding=0)
        self.conv2 = nn.Conv1d(64, 128, kernel_size=3, stride=1, padding=1)

        # Calculate the size of the features after the convolution and pooling layers
        # Assuming input length is 500 and you apply pooling twice
        conv_output_size = 500 // 2 // 2
        self.fc1 = nn.Linear(128 * conv_output_size, 128)
        self.fc2 = nn.Linear(128, num_classes)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        # Flatten the output for the dense layer
        x = x.view(x.size(0), -1)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x
    

def preprocess_data(sample, crop_size, noise_level):
    # Normalize the sample
    sample_mean = sample.mean(axis=0)
    sample_std = sample.std(axis=0)
    sample = (sample - sample_mean) / sample_std

    # Random cropping
    if sample.shape[0] > crop_size:
        start = np.random.randint(0, sample.shape[0] - crop_size)
        sample = sample[start : start + crop_size, :]
    else:
        # If the sample is shorter than crop_size, you might want to pad it or handle it differently
        pass

    # Adding noise
    noise = np.random.normal(0, noise_level, sample.shape)
    sample = sample + noise

    # Reshape and convert to PyTorch tensor
    sample_tensor = torch.from_numpy(sample).float().transpose(0, 1).unsqueeze(0)
    return sample_tensor


def predict(model, sample):
    # Define preprocessing parameters
    crop_size = 500  # Example crop size, adjust to your needs
    noise_level = 0.01  # Example noise level
    
    with torch.no_grad():  # Ensure gradients are not computed in inference mode
        preprocessed_sample = preprocess_data(sample, crop_size, noise_level)
        outputs = model(preprocessed_sample)
        _, predicted = torch.max(outputs, 1)
        return predicted.item()  # or return outputs for probabilistic interpretation