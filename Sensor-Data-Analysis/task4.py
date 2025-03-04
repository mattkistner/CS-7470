import parser_data
from plot_data import plot_data
from task2 import clean_data
from util import vector_magnitude
from util import moving_average
from task3 import count_steps
import matplotlib.pyplot as plt


def segment_climbing_walking(data_accelerometer, data_gyrosocope):
    '''
    While collecting data on stairs there were times when you were also walking rather than climbing
    It is important to remove the parts from the data where you were walking in between the flight of stairs
    Write your own algorithm to find segments in data which corresponds to climbing only

    This functions returns
    List of tuples (x,y,z) which corresponds to climbing only.
    i.e. remove data points from the original data which corresponds to walking
    '''
    
    # init
    climbing_data_accelerometer = []
    climbing_segments = []
    walking_segments = []
    segment_x_values = []
    climbing_data = []
    walking_data = []

    # thresholds
    threshold_min = -1.3
    threshold_max = 1.8
    check_length = 200 # check for check_length within threshold

    # processing vars
    walking = True
    threshold_counter = 0

    for i, value in enumerate(data_gyrosocope):
        if (threshold_min <= value <= threshold_max) and walking:  # Within threshold - walking
            walking_data.append((i, value)) # add current data point to walking_data

        elif (threshold_min <= value <= threshold_max) and not walking: # Within threshold - climbing
            climbing_data.append((i, value)) # add current data point to climbing_data

            # update threshold and check
            threshold_counter += 1
            if threshold_counter > check_length:  # wwitch to walking segment if threshold exceeded
                walking = True

                # add climbing data to segments
                if climbing_data:
                    climbing_segments.append(climbing_data)
                    segment_x_values.append(climbing_data[0][0])
                    climbing_data_accelerometer.extend([data_accelerometer[i] for i, _ in climbing_data])
                    climbing_data = []

        else:  # Outside threshold - climbing  
            climbing_data.append((i, value)) # add current data point to climbing_data
            threshold_counter = 0 # threshold reset

            if walking:
                # switch to climb if walking before
                walking = False

                # add walking data to segments
                if walking_data:
                    walking_segments.append(walking_data)
                    segment_x_values.append(walking_data[0][0])
                    walking_data = []

    # plot climbing and walking segments
    #plt.plot(data_accelerometer, label='Accelerometer Data')
    for segment in walking_segments:
        plt.plot([i for i, _ in segment], [data_gyrosocope[i] for i, _ in segment], 'k-')
        plt.plot([i for i, _ in segment], [data_accelerometer[i] for i, _ in segment], 'k-')
    for segment in climbing_segments:
        plt.plot([i for i, _ in segment], [data_gyrosocope[i] for i, _ in segment], 'r-')
        plt.plot([i for i, _ in segment], [data_accelerometer[i] for i, _ in segment], 'b-')
    for x in segment_x_values:
        plt.axvline(x=x, color='k', linestyle='--')  # Vertical lines to indicate segment changes
    
    # threshold lines
    plt.axhline(y=threshold_min, color='magenta', linestyle='--', label='Threshold Min')
    plt.axhline(y=threshold_max, color='magenta', linestyle='--', label='Threshold Max')

    plt.plot([], [], 'r-', label='climbing (accelerom.)')
    plt.plot([], [], 'k-', label='climbing (gyroscope)')
    plt.plot([], [], 'b-', label='walking')

    plt.legend(loc='upper right')
    plt.title('Segmented Climbing and Walking Data')
    plt.show()


    return climbing_data_accelerometer

def main():
    # loading dand processing initial data
    # init common vars
    timestamps = []
    window = 50
    start_time = 8.4
    end_time = 59

    plt.title('Pre-Segmented Stair Climb Data')

    # accelerometer (get filtered accelerometer magnitude)
        # get data
    file_name_accelerometer = "climb_steps_accelerometer.csv"
    data_accelerometer = parser_data.get_data(file_name_accelerometer)
        # process data
    cleaned_data_accelerometer = clean_data(data_accelerometer, start_time, end_time, "climb_steps_accelerometer_clean.csv")
    magnitude_data_accelerometer = vector_magnitude(cleaned_data_accelerometer)
    timestamps = [row[0] for row in cleaned_data_accelerometer]
    average_data_accelerometer = moving_average(magnitude_data_accelerometer, window)
        # print
    plt.plot(timestamps[:len(average_data_accelerometer)],average_data_accelerometer, label="Filtered Accelerometer Magnitude")


    # gyroscope (get filtered gyroscope z)
        # get data
    file_name_gyroscope = "climb_steps_gyroscope.csv"
    data_gyroscope = parser_data.get_data(file_name_gyroscope)
        # process data
    cleaned_data_gyroscope = clean_data(data_gyroscope, start_time, end_time, "climb_steps_gyroscope_clean.csv")
    magnitude_data_gyroscope = vector_magnitude(cleaned_data_gyroscope)
    timestamps = [row[0] for row in cleaned_data_gyroscope]
    average_data_gyroscope = moving_average(magnitude_data_gyroscope, window)
    average_z_gyrosocope = moving_average([row[3] for row in cleaned_data_gyroscope], window)
        # print
    plt.plot(timestamps[:len(average_z_gyrosocope)],average_z_gyrosocope, label="Filtered Gyroscope Z")


    # magnetometer (unused)
        # get data
    file_name_magnetometer = "climb_steps_magnetometer.csv"
    data_magnetometer = parser_data.get_data(file_name_magnetometer)
        # process data
    cleaned_data_magnetometer = clean_data(data_magnetometer, start_time, end_time, "climb_steps_magnetometer_clean.csv")
    magnitude_data_magnetometer = vector_magnitude(cleaned_data_magnetometer)
    timestamps = [row[0] for row in cleaned_data_magnetometer]
    average_data_magnetometer = moving_average(magnitude_data_magnetometer, window)


    # print pre-segmented data that will be used (using filtered accelerometer magnitude and filtered gyroscope z)
    plt.legend(loc='upper right')
    plt.show()

    # segmenting data
    segmented_accelerometer_data = segment_climbing_walking(average_data_accelerometer, average_z_gyrosocope)
        # print
    plt.title('Climbing Accelerometer Magnitude Data')
    plt.plot(segmented_accelerometer_data, label="magnitude")
    plt.legend(loc='upper right')
    plt.show()

    # calculate steps
    segmented_timestamps = [i for i in range(len(segmented_accelerometer_data))]
    number_of_steps = count_steps(segmented_accelerometer_data, 13, segmented_timestamps)
        # plot w steps
    plt.title('Accel. Magnitude Plot With Steps')
    plt.plot(segmented_timestamps,segmented_accelerometer_data, label="magnitude")
    plt.legend(loc='upper right')
    plt.show()
    print("Number of steps counted are :{0:d}".format(number_of_steps))


if __name__== "__main__":
  main()
 