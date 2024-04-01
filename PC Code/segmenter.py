import os
import pickle
from data import Data

data_file = "03-26_3.pkl"

file_dir = os.path.join(os.getcwd() + r"\Data\Collected" , data_file)

with open(file_dir, 'rb') as file:
    data = pickle.load(file)

data.equalize()

start_idx = []
end_idx = []

for i, time in enumerate(data.timestamps):
    if time in data.timeouts:
        end_idx.append(i)
    elif time in data.start_times:
        if len(end_idx) < len(start_idx):
            start_idx.append(i)
            end_idx.append(i)
        else:
            start_idx.append(i)

if len(end_idx) < len(start_idx):
    end_idx.append(data.timestamps[-1])

for i in range(len(start_idx)):
    label_str = data.label_dict[data.labels[i]]
    savepath = os.getcwd() + r"\Data\Segments\\" + label_str
    entries = os.listdir(savepath)
    file_count = sum([1 for entry in entries if os.path.isfile(os.path.join(savepath, entry)) and entry.endswith('.pkl')])
    segment_number = file_count

    segment_name = label_str + str(file_count)
    start = start_idx[i]
    end = end_idx[i]+1
    segment = Data()
    segment.timestamps = data.timestamps[start:end]
    for j in range(6):
        segment.processed_values[j] = data.processed_values[j][start:end]
    file_count += 1

    filename = os.path.join(savepath, segment_name) + ".pkl"
    with open(filename, 'wb') as file:
        pickle.dump(segment, file)     