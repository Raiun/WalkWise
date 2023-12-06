import collect_imu_data as imu
import model_inference as inference
from model_inference import Gait1DCNN  # needed so Gait1DCNN symbol can be resolved
import torch
import asyncio
import os
import numpy as np
import unlock

arduinoName = "Nate's Nano"
newData = "nate_data_10.txt"
collectionTime = 7

async def main():
    await imu.collect_data(arduinoName,newData,collectionTime)
    
    model = torch.load("1D_CNN_model.pth")
    name_dict = {0: "Hersh Gupta", 1: "Nate Webster", 2: "Ryan Man"}
    model.eval()  # Set the model to evaluation mode
    sample = np.loadtxt(
            newData, delimiter=","
        ) 
    prediction = inference.predict(model, sample)
    predictedName = name_dict[prediction]
    print(predictedName)

    #os.system("python3 unlock.py " + predictedName) # call unlock.py

    #os.remove(newData) # clear file for each iteration

if __name__ == "__main__":
    asyncio.run(main())