import numpy as np

Ts = 0.01 # Dimension: sec

def tustin_derivative(input, input_old, output_old, cutoff_freq):
	time_const = 1/(2 * np.pi * cutoff_freq)
	output = (2 * (input - input_old) - (Ts - 2 * time_const) * output_old) / (Ts + 2 * time_const)
	return output