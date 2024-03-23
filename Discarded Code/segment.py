import pickle
import os
import matplotlib.pyplot as plt

class Segment():
    def __init__(self) -> None:
        self.values = [[] for _ in range(6)]
        self.timestamps = []
        self.savepath = os.getcwd() + r"\Data\Segments" # (CHANGE THIS)

    def values_update(self, values):
        for i in range(6):
            self.values[i] = values[i]
    
    def values_clear(self):
        self.values = [[] for _ in range(6)]

    def filesave(self, label):
        entries = os.listdir(self.savepath)
        file_count = sum([1 for entry in entries if os.path.isfile(os.path.join(self.savepath, entry)) and entry.endswith('.pkl')])
        name = label + str(file_count) + '.pkl'
        filename = os.path.join(self.savepath, name)
        with open(filename, 'wb') as file:
            pickle.dump(self, file)

    def from_data(self, directory):

        with open(directory, 'rb') as file:
            data = pickle.load(file)

        segment_record = False
        segment = [[] for _ in range(6)]

        label_iterator = 0

        for i, time in enumerate(data.timestamps):
            if time in data.start_times:
                segment_record = True
                if len(segment[0]) != 0:
                    self.values_update(segment)
                    self.filesave(data.label_dict[data.labels[label_iterator]])
                    print(label_iterator)
                    label_iterator += 1
                    self.values_clear()

            elif time in data.timeouts:
                segment_record = False
                if len(segment[0]) != 0:
                    self.values_update(segment)
                    self.filesave(data.label_dict[data.labels[label_iterator]])
                    print(label_iterator)
                    # label_iterator += 1
                    self.values_clear()

            if segment_record:
                for i in range(6):
                    segment[i].append(data.processed_values[i])
                self.timestamps.append(time)

    def plot(self):
        fig, axs = plt.subplots(6, 1, sharex=True, figsize=(10, 10))

        axs[0].set_ylabel('acc_x')
        axs[1].set_ylabel('acc_y')
        axs[2].set_ylabel('acc_z')
        axs[3].set_ylabel('gyro_x')
        axs[4].set_ylabel('gyro_y')
        axs[5].set_ylabel('gyro_z')

        # Plot each data column
        for i in range(1, 7):
            axs[i-1].plot(self.timestamps, self.values[i-1], label=f'data{i}')
            axs[i-1].legend(loc="upper right")

        axs[-1].set_xlabel('Timestamp')

        plt.tight_layout()
        plt.show()
