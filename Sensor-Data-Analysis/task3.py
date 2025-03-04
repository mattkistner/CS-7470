from plot_data import plot_data
import parser_data

# added imports
from util import vector_magnitude
from util import moving_average
import matplotlib.pyplot as plt

def count_steps(data, threshold, timestamps):
    #plot_data(data)
    num_steps = 0
    peak = False
    
    for i in range(len(data) - 1):
        if data[i] > threshold and data[i] > data[i - 1] and data[i] > data[i + 1]:
            # above threshold and local maximum
            if not peak:
                # not already within a step
                num_steps += 1
                peak = True
                    # dot at local maximum
                plt.plot(timestamps[i], data[i], 'ro')
            
        elif data[i] < threshold:
            # under threshold
            peak = False

    # threshold line
    plt.axhline(y=threshold, color='r', linestyle='--', label='Threshold')


    return num_steps



def main():
    # loading data
    file_name_1 = "walking_steps_1_clean.csv"  # Change to your file name
    data_1 = parser_data.get_data(file_name_1)
    file_name_2 = "walking_steps_2_clean.csv"  # Change to your file name
    data_2 = parser_data.get_data(file_name_2)

    # timestamp
    timestamps_1 = [row[0] for row in data_1]
    timestamps_2 = [row[0] for row in data_2]


    # magnitudes
        # ws1
    magnitude_data_1 = vector_magnitude(data_1)
    plt.title('Magnitude Plot')
    plt.plot(timestamps_1,magnitude_data_1, label="magnitude")
    plt.legend(loc='upper right')
    plt.show()

        # ws2
    magnitude_data_2 = vector_magnitude(data_2)
    plt.title('Magnitude Plot')
    plt.plot(timestamps_2,magnitude_data_2, label="magnitude")
    plt.legend(loc='upper right')
    plt.show()

    # moving averages
    window = 20

        # ws1
    average_data_1 = moving_average(magnitude_data_1, window)
    plt.title('Low Pass Filtered Magnitude Plot')
    plt.plot(timestamps_1[:len(average_data_1)],average_data_1, label="magnitude")
    plt.legend(loc='upper right')
    plt.show()

        # ws2
    average_data_2 = moving_average(magnitude_data_2, window)
    plt.title('Low Pass Filtered Magnitude Plot')
    plt.plot(timestamps_2[:len(average_data_2)],average_data_2, label="magnitude")
    plt.legend(loc='upper right')
    plt.show()

    # step counts
    print(average_data_1)
        # ws1
    plt.title('Magnitude Plot With Steps')
    plt.plot(timestamps_1[:len(average_data_1)],average_data_1, label="magnitude")
    plt.legend(loc='upper right')
    number_of_steps_1 = count_steps(average_data_1, 10, timestamps_1)
    print ("Number of steps in trial 1 counted are :{0:d}".format(number_of_steps_1))
    plt.show()
    
    plt.title('Magnitude Plot With Steps')
    plt.plot(timestamps_2[:len(average_data_2)],average_data_2, label="magnitude")
    plt.legend(loc='upper right')
    number_of_steps_2 = count_steps(average_data_2, 12, timestamps_2)
    print ("Number of steps in trial 2 counted are :{0:d}".format(number_of_steps_2))
    plt.show()

if __name__== "__main__":
  main()

 