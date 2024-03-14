from matplottikz.tikz_file_writer import tikz_writer
from matplottikz.utils import empty_plot_dict, matplotlib_markers, TAB, TAB2, TAB3

class matplottikz:
    def __init__(self):
        self.clear()
    
    def clear(self):
        self.current_plot = None
        self.plots = []
        self.figures_names = []
    
    def print_current_figures(self):
        for i, names in enumerate(self.figures_names):
            print(f"Figure {i+1}: {names}")
    
    def grid(self, show=True, style="dashed"):
        self.show_grid = show
        if show:
            self.current_plot["grid"] = "both"
            self.current_plot["grid_style"] = style
        else:
            self.current_plot["grid"] = "false"
            self.current_plot["grid_style"] = style
    
    def legend(self, name=None, columns=1, anchor="center", pos="north west", column_sep=2, font_size=7):
        if name is not None:
            print(f"NOTE:Legend will not appear in figure have to call separately to show up in document.")
        self.current_plot["legend_name"] = name
        self.current_plot["legend_columns"] = columns
        self.current_plot["legend_pos"] = pos
        self.current_plot["legend_style"]["anchor"] = anchor
        self.current_plot["legend_style"]["column_sep"] = column_sep
        self.current_plot["legend_style"]["font_size"] = font_size
    
    def axis(self, tick_label_size=7, label_size=9):
        self.current_plot["tick_label_size"] = tick_label_size
        self.current_plot["label_size"] = label_size
    
    def ymode(self, mode):
        assert mode in ["log", "linear"], "mode must be either 'log' or 'linear'"
        self.current_plot["y_axis_mode"] = mode

    def xlabel(self, label, offset=0.8):
        self.current_plot["x_label"] = label
        self.current_plot["x_label_offset"] = offset
    
    def ylabel(self, label, offset=-0.75):
        self.current_plot["y_label"] = label
        self.current_plot["y_label_offset"] = offset
    
    def figure(self, filename, width=0.9, height=0.65, scale=1):
        
        if filename in self.figures_names:
            index = self.figures_names.index(filename)
            self.current_plot = self.plot[index]

        else:
            self.figures_names.append(filename)
            self.plots.append(empty_plot_dict.copy())
            self.current_plot = self.plots[-1]

        self.current_plot["filename"] = filename
        self.current_plot["width"] = width
        self.current_plot["height"] = height
        self.current_plot["scale"] = scale

    def scatter(self, x, y, color=None, marker_size=3, label=None):
        if self.current_plot is None:
            raise ValueError("No figure is defined. Please define a figure first")

        if label is None:
            label = f"scatter_{len(self.current_plot['plots'])}"
        
        self.current_plot["plots"][label] = {}
        self.current_plot["plots"][label]["x"] = x
        self.current_plot["plots"][label]["y"] = y
        self.current_plot["plots"][label]["line_type"] = "scatter"
        self.current_plot["plots"][label]["color"] = color
        self.current_plot["plots"][label]["marker"] = marker_o
        self.current_plot["plots"][label]["marker_size"] = marker_size
    
    def plot(self, x, y, marker=None, color=None, marker_size=3, label=None):
        if self.current_plot is None:
            raise ValueError("No figure is defined. Please define a figure first")

        if label is None:
            label = f"plot_{len(self.current_plot['plots'])}"
        
        self.current_plot["plots"][label] = {}
        self.current_plot["plots"][label]["x"] = x
        self.current_plot["plots"][label]["y"] = y
        self.current_plot["plots"][label]["line_type"] = "line"
        self.current_plot["plots"][label]["color"] = color
        self.current_plot["plots"][label]["marker"] = marker
        self.current_plot["plots"][label]["marker_size"] = marker_size

    def write_tikz(self, dir="", show_latex_cmd=True):
        for i, plot in enumerate(self.plots):
            if len(plot["plots"]) == 0:
                continue
            
            # clip the color palette size to between 3 and 8
            color_palette_size = max(3, min(8, len(plot["plots"])))

            filename = plot["filename"]
            writer = tikz_writer(dir + filename)
            writer.write_color_palette(color_palette_size)

            writer.start_file()
            writer.write(TAB + r"\pgfplotsset{")
            writer.write(TAB2 + r"label style = {font=\fontsize{" + str(self.current_plot["label_size"]) + "pt}{7.2}\selectfont},")
            writer.write(TAB2 + r"tick label style = {font=\fontsize{" + str(self.current_plot["tick_label_size"]) + "pt}{7.2}\selectfont}")
            writer.write(TAB + r"}")
            writer.write(TAB + r"\begin{axis}[")
            writer.write(TAB2 + r"scale = " + str(plot["scale"]) + ",")
            writer.write(TAB2 + r"ymode=" + plot["y_axis_mode"] + ",")
            if plot["x_label"] is not None:
                writer.write(TAB2 + r"xlabel={" + plot["x_label"] + r"}, xlabel style={yshift=" + str(plot["x_label_offset"]) + r"em},")
            if plot["y_label"] is not None:
                writer.write(TAB2 + r"ylabel={" + plot["y_label"] + r"}, ylabel style={yshift=" + str(plot["y_label_offset"]) + r"em},")
            if plot["grid"] is not None:
                writer.write(TAB2 + r"grid=" + plot["grid"] + r",")
            writer.write(TAB2 + r"ymajorgrids=true,")
            writer.write(TAB2 + r"xmajorgrids=true,")
            writer.write(TAB2 + r"grid style=" + plot["grid_style"] + r",")
            writer.write(TAB2 + r"width=" + str(plot["width"]) + r"\columnwidth,")
            writer.write(TAB2 + r"height=" + str(plot["height"]) + r"\columnwidth,")
            writer.write(TAB2 + r"legend style={")
            if plot["legend_name"] is not None:
                writer.write(TAB3 + r"anchor=" + plot["legend_style"]["anchor"] + r",")
                writer.write(TAB3 + r"cells={anchor=west},")
            writer.write(TAB3 + r"column sep= " + str(plot["legend_style"]["column_sep"]) + r"mm,")
            writer.write(TAB3 + r"thick,")
            writer.write(TAB3 + r"font=\fontsize{" + str(plot["legend_style"]["font_size"]) + "pt}{7.2}\selectfont,")
            writer.write(TAB2 + r"},")
            if plot["legend_name"] is not None:
                writer.write(TAB2 + r"legend to name=" + plot["legend_name"] + r",")
            writer.write(TAB2 + r"legend columns=" + str(plot["legend_columns"]) + r",")
            if plot["legend_pos"] is not None:
                writer.write(TAB2 + r"legend pos=" + plot["legend_pos"] + r",")
            writer.write(TAB + r"]")
            writer.write("")

            color_index = 1
            for label, data in plot["plots"].items():
                x = data["x"]
                y = data["y"]
                
                color = data["color"]
                marker = data["marker"]
                marker_size = data["marker_size"]
                line_style = data["line_type"]
                add_plot_params = ""

                if color is None:
                    color = "matplottikz-color" + str(color_index)
                    color_index += 1
                    if color_index > color_palette_size:
                        color_index = 1

                if line_style == "scatter":
                    add_plot_params += r"only marks"
                
                if add_plot_params != "":
                    add_plot_params += r", color=" + color
                else:
                    add_plot_params += r"color=" + color
                
                if marker is not None:
                    add_plot_params += r", thick, mark=" + marker
                
                add_plot_params += r", mark size=" + str(marker_size)

                writer.write(TAB2 + r"% " + "-" * 25)
                writer.write(TAB2 + r"% Plot for: " + label)
                writer.write(TAB2 + r"% " + "-" * 25)
                writer.write(TAB2 + r"\addplot[" + add_plot_params + r"]")
                writer.write(TAB2 + r"table{")
                for i in range(len(x)):
                    writer.write(TAB3 + str(x[i]) + " " + str(y[i]))
                writer.write(TAB2 + r"};")
                writer.write(TAB2 + r"\addlegendentry{" + label + r"}")
                writer.write("")

            writer.write(TAB + r"\end{axis}")
            writer.end_file()
            writer.write_import_latex_cmd(filename, plot["legend_name"])
            writer.save()
            if show_latex_cmd:
                print(f"")
                print("To include the figure in your latex document, use the following commands:")
                self.print_latex_figure_cmd(filename, plot["legend_name"])
    
    def print_latex_figure_cmd(self, filename, legend_name):
        print(f"\\begin{{figure}}[!htb]")
        print(f"    \\centering")
        print(f"    % Uncomment one of the following")
        print(f"    %\\includegraphics[width=0.9\\columnwidth]{{figures/{filename}}}")
        print(f"    %\\includestandalone[width=0.9\\columnwidth]{{figures/{filename}}}")
        if legend_name:
            print(f"    \\hspace{{25pt}}\\ref{{{legend_name}}}")
        print(f"    \\caption{{Write caption here.}}")
        print(f"    \\label{{fig:{filename}}}")
        print(f"\\end{{figure}}")

    def preview(self, show=True, save_fig=""):
        for i, plot in enumerate(self.plots):
            plt.figure()
            plt.title(plot["filename"] + " Preview")
            plt.yscale(plot["y_axis_mode"])
            plt.grid(visible=plot["grid"] == "both", linestyle=plot["grid_style"])
            plt.xlabel(plot["x_label"])
            plt.ylabel(plot["y_label"])

            for label, data in plot["plots"].items():
                x = data["x"]
                y = data["y"]
                marker = data["marker"]
                line_style = data["line_type"]
                if line_style == "scatter":
                    plt.scatter(x, y, label=label, marker=matplotlib_markers[marker])
                else:
                    plt.plot(x, y, label=label, marker=matplotlib_markers[marker])
            plt.legend()
            
            if save_fig != "":
                plt.savefig(save_fig + plot["filename"] + ".png")
            
            if show:
                plt.show()
            else:
                plt.close()
                