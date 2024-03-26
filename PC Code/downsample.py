import os
import pickle
from data import Data

data_file = "03-23_0.pkl"

file_dir = os.getcwd() + r"\Data\Collected" + "\\" + data_file

with open(file_dir, 'rb') as file:
    data = pickle.load(file)

target_frequency = 50 # Hz
every_n_sample = int(100/target_frequency)

savepath = os.getcwd() + r"\Data\Downsampled"
entries = os.listdir(savepath)
file_count = sum([1 for entry in entries if os.path.isfile(os.path.join(savepath, entry)) and entry.endswith('.pkl')])

down_samp_data = Data()

for i, time in enumerate(data.timestamps):
    if (i % every_n_sample) or (time in data.start_times) or (time in data.timeouts):
        down_samp_data.timestamps.append(time)
        for j in range(6):
            down_samp_data.raw_values[j][i].append(data.raw_values[j][i])
        for j in range(6):
            down_samp_data.processed_values[j][i].append(data.processed_values[j][i])

down_samp_data.frequency = target_frequency
down_samp_data.start_times = data.start_times
down_samp_data.timeouts = data.timeouts
down_samp_data.labels = data.labels
down_samp_data.label_dict = data.label_dict

name = data_file.split('.pkl') + '_' + str(target_frequency) + 'Hz' + '_' + str(file_count)
filename = os.path.join(savepath, name) + ".pkl"
with open(filename, 'wb') as file:
    pickle.dump(down_samp_data, file)     