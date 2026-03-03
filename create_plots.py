import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("data/fitness_output.csv")

x = df.iloc[:, 0]
y1 = df.iloc[:, 1]
y2 = df.iloc[:, 2]
y3 = df.iloc[:, 3] * 1/300
y4 = df.iloc[:, 4]

plt.figure()
plt.plot(x, y1, label="Average")
plt.plot(x, y2, label="Best")
#plt.plot(x, y3, label="Num Success")

plt.title("Fitness change through generations")
plt.xlabel("Generation")
plt.ylabel("Fitness")
plt.legend()
plt.savefig('plots/fitness_plot.png')

plt.figure()
plt.plot(x, y4, label="Average circuit length")

plt.title("Mean circuit size through generations")
plt.xlabel("Generation")
plt.ylabel("Average circuit size")
plt.legend()
plt.savefig('plots/circuit_len_plot.png')





"""
xpoints = np.array([1,2,6,8])
ypoints = np.array([3, 8, 1, 10])

plt.plot(xpoints, ypoints)
plt.savefig('test.png')
"""