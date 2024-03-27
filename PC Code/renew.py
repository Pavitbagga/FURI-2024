import pickle
import os
from data import Data

filename = '03-26_1.pkl'
directory_old = os.getcwd() + r'/Data/Collected/' + filename

with open(directory_old, 'rb') as file:
    data = pickle.load(file)

renewed_data = Data()
renewed_data.timestamps = data.timestamps
renewed_data.raw_values = data.raw_values
renewed_data.processed_values = data.processed_values
renewed_data.start_times = data.start_times
renewed_data.timeouts = data.timeouts
renewed_data.labels = data.labels
renewed_data.label_dict = data.label_dict
renewed_data.frequency = data.frequency

directory_new = os.getcwd() + r"/Data/Renewed/" + filename
with open(directory_new, 'wb') as file:
    pickle.dump(renewed_data, file) 