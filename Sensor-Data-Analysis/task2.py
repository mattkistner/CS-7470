import parser_data
from plot_data import plot_data
import csv


def clean_data(data, start, end, new_file_name):

    # clean data (copy within range)
    cleaned_data = []
    for sample in data:
        if start <= sample[0] <= end:
            cleaned_data.append(sample)

    # save to clean file
    file_name_clean = "data/" + new_file_name
    with open(file_name_clean, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Time (s)', 'Acceleration x (m/s^2)', 'Acceleration y (m/s^2)', 'Acceleration z (m/s^2)']) 
        writer.writerows(cleaned_data)

    return cleaned_data


def main():
    # ws1
    file_name_1 = "walking_steps_1.csv"
    data_1 = parser_data.get_data(file_name_1)
    cleaned_data_1 = clean_data(data_1, 0.5, 56, "walking_steps_1_clean.csv")
    plot_data(cleaned_data_1)

    # ws2
    file_name_2 = "walking_steps_2.csv"
    data_2 = parser_data.get_data(file_name_2)
    cleaned_data_2 = clean_data(data_2, 1.35, 54.50, "walking_steps_2_clean.csv")
    plot_data(cleaned_data_2)


if __name__== "__main__":
  main()

 