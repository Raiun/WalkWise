import matplotlib.pyplot as plt
import requests
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import math

# URL of your web server
SERVER_URL = "http://192.168.4.1"

# Initialize the plot
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
ax.set_xlim([-1, 1])
ax.set_ylim([-1, 1])
ax.set_zlim([-1, 1])

# Initialize quiver arrows with dummy data
accel_arrow = ax.quiver(0, 0, 0, 0, 0, 0, length=1, color="blue", normalize=True)
gyro_arrow = ax.quiver(0, 0, 0, 0, 0, 0, length=1, color="red", normalize=True)


# Function to update the arrows with data from the server
def update_arrows(num, accel_arrow, gyro_arrow):
    # Clear the current arrows
    ax.cla()

    # Re-set the plot limits and labels after clearing
    ax.set_xlim([-1, 1])
    ax.set_ylim([-1, 1])
    ax.set_zlim([-1, 1])
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    # Make a GET request to your server
    response = requests.get(SERVER_URL)
    # Parse the response assuming a tab-delimited string of six values
    values = response.text.split("\t")
    # Make sure we have exactly 6 values (3 for accelerometer, 3 for gyroscope)
    if len(values) == 6:
        # try:
        # Convert string values to float
        accel_data = list(
            map(float, values[:3])
        )  # First three values for accelerometer
        gyro_data = list(map(float, values[3:]))  # Last three values for gyroscope

        # Update the accelerometer arrow
        # accel_arrow.remove()
        new_accel_arrow = ax.quiver(
            0, 0, 0, *accel_data, length=1, color="blue", normalize=True
        )

        # Update the gyroscope arrow
        # gyro_arrow.remove()
        length = (
            math.sqrt(gyro_data[0] ** 2 + gyro_data[1] ** 2 + gyro_data[2] ** 2) / 200
        )
        new_gyro_arrow = ax.quiver(
            0, 0, 0, *gyro_data, length=length, color="red", normalize=True
        )

        return new_accel_arrow, new_gyro_arrow
    # except ValueError:
    #     # Handle the case where conversion to float fails
    #     print("Error: Non-numeric data received.")
    #     return accel_arrow, gyro_arrow
    else:
        # Handle the case where the number of values is not 6
        print("Error: Incorrect number of values received.")
        return accel_arrow, gyro_arrow


# Create an animation that updates the arrows
ani = FuncAnimation(
    fig, update_arrows, fargs=(accel_arrow, gyro_arrow), interval=10, blit=False
)

# Display the plot
plt.show()
