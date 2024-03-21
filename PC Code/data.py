import matplotlib.pyplot as plt

class Data_Structure():
    def __init__(self) -> None:
        self.timestamps = []
        self.raw_values = [[] for _ in range(6)]
        self.processed_values = [[] for _ in range(6)]
        self.start_times = []
        self.timeouts = []
        self.order_of_labels = []

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
            axs[i-1].plot(self.timestamps, self.processed_values[i-1], label=f'data{i}')
            axs[i-1].legend(loc="upper right")

            # Highlight the x-axis at timestamps
            if i == 2 :
                for ts in self.start_times:
                    axs[i-1].axvline(x=ts, color='g', linestyle='--')
                for ts in self.timeouts:
                    axs[i-1].axvline(x=ts, color='r', linestyle='--')

        axs[-1].set_xlabel('Timestamp')

        plt.tight_layout()
        plt.show()

'''
Label:
1) Correct: 0
2) Swinging: 1
3) Very Fast: 2
4) Incomplete: 3
'''