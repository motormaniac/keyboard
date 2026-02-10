import pandas as pd
import matplotlib.pyplot as plt

filename = "layout_data/layout_data6.txt"
cutoff_index = 60 # cut off the first n generations

layout_df = pd.read_csv(filename, delimiter="\t")
layout_df = layout_df[cutoff_index:]
plt.plot(layout_df.index, layout_df["average fitness"], color="black")
plt.plot(layout_df.index, layout_df["top percent average fitness"], color="blue")
plt.plot(layout_df.index, layout_df["best fitness"], color="red")
plt.xlabel("Generations")
plt.ylabel("Fitness")
plt.grid(True, alpha=0.3)
plt.show()