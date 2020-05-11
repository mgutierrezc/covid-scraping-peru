import numpy as np
import pandas

data = np.load('matrizProba2020.npy')
np.savetxt("matrix_prob.csv", data, delimiter=",")