from matplottikz import matplottikz as tikzplot
import numpy as np 


y1 = np.random.normal(loc = 0, scale = 1, size = 1000)
y2 = np.random.normal(loc = 0, scale = 1, size = 1000)

tikz_plt = tikzplot()
tikz_plt.figure("matplottikz_boxplot_example")
tikz_plt.xlabel("y-axis")

tikz_plt.boxplot_direction("y")
tikz_plt.boxplot(1, y1, label="y1")

tikz_plt.write_tikz()