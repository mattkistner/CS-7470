from plot_data import plot_data

import parser_data
# numpy imported to check if the student has numpy
import numpy

data = parser_data.get_data("walking_steps_1.csv")
plot_data(data)

data = parser_data.get_data("walking_steps_2.csv")
plot_data(data)
