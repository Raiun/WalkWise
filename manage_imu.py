import collect_imu_data as imu
import model_inference as inference
from model_inference import Gait1DCNN  # needed so Gait1DCNN symbol can be resolved
import torch
import asyncio
import os
import numpy as np
import subprocess

arduinoName = "Nate's Nano"
newData = "data/nate_26.txt"
collectionTime = 7

async def main():
    await imu.collect_data(arduinoName,newData,collectionTime)
    
    model_hersh = torch.load("1D_CNN_model_hersh.pth")
    model_ryan = torch.load("1D_CNN_model_ryan.pth")
    model_nate = torch.load("1D_CNN_model_nate.pth")
    name_dict = {0: "Hersh Gupta", 1: "Nate Webster", 2: "Ryan Man"}
    model_hersh.eval()  # Set the model to evaluation mode
    model_ryan.eval()  # Set the model to evaluation mode
    model_nate.eval()  # Set the model to evaluation mode
    sample = np.loadtxt(
            newData, delimiter=","
        ) 
    prediction_hersh, output_hersh = inference.predict(model_hersh, sample)
    prediction_nate, output_nate = inference.predict(model_nate, sample)
    prediction_ryan, output_ryan = inference.predict(model_ryan, sample)
    predictedName = None
    print("output_hersh: " + str(output_hersh))
    print("output_nate: " + str(output_nate))
    print("output_ryan: " + str(output_ryan))
    output_list = [output_hersh[0][1], output_nate[0][1], output_ryan[0][1]]
    if max(output_list) < 3:
        predictedName = "Unrecognized"
    else:
        match (prediction_hersh, prediction_nate, prediction_ryan):
            case (0, 0, 0):
                predictedName = "Unrecognized"
            case (0, 1, 0):
                predictedName = "Nate Webster"
            case (0, 0, 1):
                predictedName = "Ryan Man"
            case (0, 1, 1):
                if output_nate[0][1] > output_ryan[0][1]:
                    predictedName = "Nate Webster"
                else:
                    predictedName = "Ryan Man"
            case (1, 0, 0):
                predictedName = "Hersh Gupta"
            case (1, 0, 1):
                if output_hersh[0][1] > output_ryan[0][1]:
                    predictedName = "Hersh Gupta"
                else:
                    predictedName = "Ryan Man"
            case (1, 1, 0):
                if output_hersh[0][1] > output_nate[0][1]:
                    predictedName = "Hersh Gupta"
                else:
                    predictedName = "Nate Webster"
            case (1, 1, 1):
                max_index = max(output_list)
                index = output_list.index(max_index)
                if index == 0:
                    predictedName = "Hersh Gupta"
                elif index == 1:
                    predictedName = "Nate Webster"
                else:
                    predictedName = "Ryan Man"



    print(predictedName)
    #predictedName = "Nate Webster"
    subprocess.run(["python3", "unlock.py", f"{predictedName}"]) # call unlock.py

    #os.remove(newData) # clear file for each iteration

if __name__ == "__main__":
    asyncio.run(main())