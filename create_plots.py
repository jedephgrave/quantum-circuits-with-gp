import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def main_plots():
    df = pd.read_csv("saved_data/4/fitness_output.csv")

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
    plt.savefig('plots/fitness_plot.png', dpi=600)

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



def fitness_dist():
    
    df = pd.read_csv("saved_data/1/all_genome_fitnesses.csv")
    col_name = df.columns[0]
    data = pd.to_numeric(df[col_name], errors='coerce').dropna().values

    df = pd.read_csv("saved_data/1/rand_genome_fitnesses.csv")
    col_name = df.columns[0]
    data_rand = pd.to_numeric(df[col_name], errors='coerce').dropna().values

    data_to_plot = [data,data_rand]

    plt.figure(figsize=(10, 6))  # width x height; increase height for taller boxes

    plt.boxplot(data_to_plot, vert=False, labels=['Genetic Program', 'Random Search'], patch_artist=False, widths=0.5, medianprops=dict(color='blue', linewidth=1))
    plt.ylim(0.5, 2.5)
    plt.title("Distribution of fitnesses")
    plt.xlabel("Fitness Value")
    plt.savefig('plots/gp_fitness_boxplot2.png', dpi=600)
    
def length_compare():
    df_parsimony = pd.read_csv("saved_data/2/fitness_output_parsimony.csv")
    df_normal = pd.read_csv("saved_data/2/fitness_output_no_parsimony.csv")

    gens = df_parsimony.iloc[:,0]

    mean_parsimony = df_parsimony.iloc[:,4]
    mean_normal = df_normal.iloc[:,4]
    
    med_parsimony = df_parsimony.iloc[:,5]
    med_normal = df_normal.iloc[:,5]
    
    p10_parsimony = df_parsimony.iloc[:,6]
    p10_normal = df_normal.iloc[:,6]
    
    p90_parsimony = df_parsimony.iloc[:,7]
    p90_normal = df_normal.iloc[:,7]
    
    plt.figure(figsize=(9,5))
    plt.plot(gens, med_parsimony, label="With Parismony (median, 10th-90th percentile)")
    plt.plot(gens, med_normal, label="Without Parsimony (median, 10th-90th percentile)")
    
    plt.fill_between(gens, p10_parsimony, p90_parsimony, alpha=0.3)
    plt.fill_between(gens, p10_normal, p90_normal, alpha=0.3)
    
    
    plt.title("Circuit size through generations")
    plt.xlabel("Generation")
    plt.ylabel("Circuit size")
    plt.legend()
    plt.savefig('plots/length_comparison.png', dpi=600)
    
if __name__=="__main__":
    main_plots()