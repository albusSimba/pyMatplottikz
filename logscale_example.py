from matplottikz import matplottikz
from matplottikz import marker_square

x = [i for i in range(-10, 31, 5)]
y = [   
            2.5239E-01,
            1.4308E-01,
            6.1988E-02,
            1.7012E-02,
            4.4750E-03,
            1.1375E-03,
            3.6250E-04,
            9.0625E-05,
            3.1250E-05,
        ]
tikz_plt = matplottikz()
tikz_plt.figure("matplottikz_logscale_example")
tikz_plt.xlabel("y-axis")
tikz_plt.ylabel("x-axis")
tikz_plt.grid()
tikz_plt.ymode("log")
# tikz_plt.legend(name="legend:matplottikz_logscale_example", columns=1, pos="north west")
tikz_plt.plot(x, y, marker_square, label="plot1")
# tikz_plt.preview()
tikz_plt.write_tikz()