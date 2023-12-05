import collect_imu_data as imu
import model_inference as inference
from model_inference import Gait1DCNN  # needed so Gait1DCNN symbol can be resolved
import torch
# import torch.nn as nn
# import torch.nn.functional as F
import asyncio
import os
import numpy as np

arduinoName = "Nate's Nano"
newData = "new_data.txt"
collectionTime = 10

async def main():
    await imu.collect_data(arduinoName,newData,collectionTime)
    
    model = torch.load("1D_CNN_model.pth")
    # label_dict = {"hersh": 0, "nate": 1, "ryan": 2}
    name_dict = {0: "hersh", 1: "nate", 2: "ryan"}
    model.eval()  # Set the model to evaluation mode
    
    sample = np.loadtxt(
            newData, delimiter=","
        ) 
    prediction = inference.predict(model, sample)
    predictedName = name_dict[prediction]
    print(predictedName)
    os.remove(newData) # clear file for each iteration

if __name__ == "__main__":
    asyncio.run(main())