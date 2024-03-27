import matplotlib.pyplot as plt

class Data():
    def __init__(self) -> None:
        self.timestamps = []
        self.raw_values = [[] for _ in range(6)]
        self.processed_values = [[] for _ in range(6)]
        self.start_times = []
        self.timeouts = []
        self.labels = []
        self.label_dict = {   1: "Correct",
                              2: "Swinging",
                              3: "Very_Fast",
                              4: "Incomplete",
                              5: "No_Wrist_Rotation"  }
        self.frequency = 100

    def plot(self):
        self.equalize()
        fig, axs = plt.subplots(6, 1, sharex=True, figsize=(10, 10))

        labels = ['acc_x', 'acc_y', 'acc_z', 'gyro_x', 'gyro_y', 'gyro_z']
        colors = ['r', 'g', 'b', 'c', 'm', 'y']

        # Plot each data column
        for i in range(6):
            axs[i].plot(self.timestamps, self.processed_values[i], label=labels[i], color=colors[i])
            axs[i].legend(loc="upper right")

            # Highlight the x-axis at timestamps
            if i == 1 :
                for ts in self.start_times:
                    axs[i].axvline(x=ts, color='g', linestyle='--')
                for ts in self.timeouts:
                    axs[i].axvline(x=ts, color='r', linestyle='--')

        axs[-1].set_xlabel('Timestamp')

        plt.tight_layout()
        plt.show()

    def equalize(self):
        for i in range(6):
            if len(self.timestamps) != len(self.processed_values[i]):
                self.processed_values[i].pop()
            