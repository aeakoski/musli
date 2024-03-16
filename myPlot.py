import os
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

# Directory containing the data files
# data_directory = "data_batch_1"
data_directory = "data_single_r_1"

# Get a list of all files in the directory
file_list = os.listdir(data_directory)

# Initialize a plot
plt.figure(figsize=(10, 6))

# Plot data from each file
for file_name in file_list:
    if file_name.endswith('.txt'):  # Filter out only text files
        file_path = os.path.join(data_directory, file_name)
        with open(file_path, 'r') as file:
            lines = file.readlines()
            data = []
            ignore = 0
            for line in lines:
                parsed_line = float(line.strip())
                if line:  # Skip empty lines
                    try:   
                        data.append(parsed_line)
                    except ValueError:
                        pass  # Skip unreadable rows
            smoothed_data = savgol_filter(data, 51, 3)  # Apply smoothing
            if "russin" in file_name.lower():
                if "single" in file_name.lower():
                    color = "black"
                elif "batch" in file_name.lower():
                    color = "brown"
            elif "musli" in file_name.lower():
                if "single" in file_name.lower():
                    color = "red"
                elif "batch" in file_name.lower():
                    color = "orange"
            #color = 'black' if 'russin' in file_name.lower() else 'blue'
            plt.plot(smoothed_data, label=file_name+ " smooth")#, color=color)
            plt.plot(data, label=file_name)#, color=color)

# Add labels and legend
plt.xlabel('Sample Index')
plt.ylabel('Sensor Value')
plt.title('Overlaying Line Graph of Sensor Data')
plt.legend()

# Add grid
plt.grid(True)

# Show plot
plt.tight_layout()

# Enable zooming

plt.show()
