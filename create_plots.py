import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("data/fitness_output.csv")

x = df.iloc[:, 0]
y1 = df.iloc[:, 1]
y2 = df.iloc[:, 2]
y3 = df.iloc[:, 3] * 1/300
y4 = df.iloc[:, 4]
med = df.iloc[:, 5]
p10 = df.iloc[:, 6]
p90 = df.iloc[:, 7]

# average and best circuits
plt.figure()
plt.plot(x, y1, label="Average")
plt.plot(x, y2, label="Best")
#plt.plot(x, y3, label="Num Success")

plt.title("Fitness change through generations")
plt.xlabel("Generation")
plt.ylabel("Fitness")
plt.legend()
plt.savefig('plots/fitness_plot.png')

# average circuit length
plt.figure()
plt.plot(x, y4, label="Average circuit length")
plt.plot(x, med, label="Median circuit length")

plt.fill_between(x, p10, p90, alpha=0.3, label="10-90 percentile")

plt.title("Mean circuit size through generations")
plt.xlabel("Generation")
plt.ylabel("Average circuit size")
plt.legend()
plt.savefig('plots/circuit_len_plot.png')




####################################################
#      BOX PLOT GP VS RANDOM SEARCH CREATION       # - NOT NEEDED RN
####################################################
"""
df = pd.read_csv("data/all_genome_fitnesses.csv")
col_name = df.columns[0]
data = pd.to_numeric(df[col_name], errors='coerce').dropna().values

df = pd.read_csv("data/rand_genome_fitnesses.csv")
col_name = df.columns[0]
data_rand = pd.to_numeric(df[col_name], errors='coerce').dropna().values

data_to_plot = [data,data_rand]

plt.figure()
plt.figure(figsize=(12, 6))  # width x height; increase height for taller boxes

plt.boxplot(data_to_plot, vert=False, labels=['Genetic Program', 'Random Search'], patch_artist=False)

plt.title("Distribution of fitnesses")
plt.xlabel("Fitness Value")
plt.savefig('plots/gp_fitness_boxplot.png')
"""
