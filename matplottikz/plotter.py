from matplottikz.tikz_file_writer import tikz_writer
from matplottikz.utils import empty_plot_dict, matplotlib_markers, TAB, TAB2, TAB3, boxplot_process_data
import matplotlib.pyplot as plt

class matplottikz:
    def __init__(self):
        self.clear()
    
    def clear(self):
        self.idx = None
        self.plots = []
        self.figures_names = []
    
    def print_current_figures(self):
        for i, names in enumerate(self.figures_names):
            print(f"Figure {i+1}: {names}")
    
    def grid(self, show=True, style="dashed"):
        self.show_grid = show
        if show:
            self.plots[self.idx]["grid"] = "both"
            self.plots[self.idx]["grid_style"] = style
        else:
            self.plots[self.idx]["grid"] = "false"
            self.plots[self.idx]["grid_style"] = style
    
    def xgrid_ticks(self, num):
        self.plots[self.idx]["minor x tick num"] = num
    
    def legend(self, name=None, columns=1, anchor="center", pos="north west", column_sep=2, font_size=7):
        if name is not None:
            print(f"NOTE:Legend will not appear in figure have to call separately to show up in document.")
        self.plots[self.idx]["legend_name"] = name
        self.plots[self.idx]["legend_columns"] = columns
        self.plots[self.idx]["legend_pos"] = pos
        self.plots[self.idx]["legend_style"]["anchor"] = anchor
        self.plots[self.idx]["legend_style"]["column_sep"] = column_sep
        self.plots[self.idx]["legend_style"]["font_size"] = font_size
    
    def axis(self, tick_label_size=7, label_size=9):
        self.plots[self.idx]["tick_label_size"] = tick_label_size
        self.plots[self.idx]["label_size"] = label_size
    
    def ymode(self, mode):
        assert mode in ["log", "linear"], "mode must be either 'log' or 'linear'"
        self.plots[self.idx]["y_axis_mode"] = mode

    def xlabel(self, label, offset=0.8):
        self.plots[self.idx]["x_label"] = label
        self.plots[self.idx]["x_label_offset"] = offset
    
    def xlabel_style(self, align="center", font="small", rotation=0):
        self.plots[self.idx]["xlabel_style"] = {
            "label_align": align,
            "font": font,
            "rotation": rotation
        }

    def xlim(self, min, max):
        self.plots[self.idx]["x_min"] = min
        self.plots[self.idx]["x_max"] = max
    
    def ylim(self, min, max):
        self.plots[self.idx]["y_min"] = min
        self.plots[self.idx]["y_max"] = max
    
    def ylabel(self, label, offset=-0.75):
        self.plots[self.idx]["y_label"] = label
        self.plots[self.idx]["y_label_offset"] = offset
    
    def ylabel_style(self, align="center", font="small", rotation=0):
        self.plots[self.idx]["ylabel_style"] = {
            "label_align": align,
            "font": font,
            "rotation": rotation
        }
        
    def xticks(self, ticks=None, distance=None, labels=None):
        if ticks is not None:
            ticks = [str(tick) for tick in ticks]
            ticks = "{" + ", ".join(ticks) + "}"
            self.plots[self.idx]["x_ticks"] = ticks
        if distance is not None:
            self.plots[self.idx]["x_ticks_distance"] = distance
        if labels is not None:
            labels = [str(label) for label in labels]
            labels = "{" + ", ".join(labels) + "}"
            self.plots[self.idx]["x_ticks_labels"] = labels
    
    def yticks(self, ticks=None, distance=None, labels=None):
        if ticks is not None:
            ticks = [str(tick) for tick in ticks]
            ticks = "{" + ", ".join(ticks) + "}"
            self.plots[self.idx]["y_ticks"] = ticks
        if distance is not None:
            self.plots[self.idx]["y_ticks_distance"] = distance
        if labels is not None:
            labels = [str(label) for label in labels]
            labels = "{" + ", ".join(labels) + "}"
            self.plots[self.idx]["y_ticks_labels"] = labels
    
    def figure(self, filename, width=0.9, height=0.65, scale=1):
        
        if filename in self.figures_names:
            self.idx = self.figures_names.index(filename)
        else:
            self.figures_names.append(filename)
            self.plots.append(empty_plot_dict())
            self.idx = len(self.plots) - 1

        self.plots[self.idx]["filename"] = filename
        self.plots[self.idx]["width"] = width
        self.plots[self.idx]["height"] = height
        self.plots[self.idx]["scale"] = scale

    def boxplot(self, x, y, color="black", fill_color="white", fill_opacity=0.2, marker="*", marker_color="white", marker_size=1, label=None):
        if self.idx is None:
            raise ValueError("No figure is defined. Please define a figure first")

        if self.plots[self.idx]["boxplot_draw_direction"] is None:
            raise ValueError("Please define the boxplot direction first using boxplot_direction method")

        if label is None:
            label = str(x)

        self.plots[self.idx]["plots"][label] = {
            "x": x,
            "y": y,
            "line_type": "boxplot",
            "color": color,
            "fill_color": fill_color,
            "fill_opacity": fill_opacity,
            "marker": marker,
            "marker_color": marker_color,
            "marker_size": marker_size
        }

    def boxplot_direction(self, direction="y"):
        self.plots[self.idx]["boxplot_draw_direction"] = direction
        
    def scatter(self, x, y, marker=None, color=None, marker_size=3, label=None):
        self.plot(x, y, marker, color, marker_size, label, "only marks")
    
    def line(self, x, y, marker=None, color=None, marker_size=3, label=None):
        self.plot(x, y, marker, color, marker_size, label, "sharp plot")

    def plot(self, x, y, marker=None, color=None, marker_size=3, label=None, line_type="smooth"):
        if self.idx is None:
            raise ValueError("No figure is defined. Please define a figure first")

        if label is None:
            label = f"plot_"+ str(len(self.plots[self.idx]["plots"]))
        
        self.plots[self.idx]["plots"][label] = {
            "x": x,
            "y": y,
            "line_type": line_type,
            "color": color,
            "marker": marker,
            "marker_size": marker_size
        }
        
    def write_tikz(self, dir="", show_latex_cmd=True):
        for i, plot in enumerate(self.plots):
            if len(plot["plots"]) == 0:
                continue
            
            # clip the color palette size to between 3 and 8
            color_palette_size = max(3, min(8, len(plot["plots"])))

            filename = plot["filename"]
            writer = tikz_writer(dir + filename)
            writer.write_color_palette(color_palette_size)
            writer.write(r"\usepgfplotslibrary{statistics}")

            writer.start_file()
            writer.write(TAB + r"\pgfplotsset{")
            writer.write(TAB2 + r"label style = {font=\fontsize{" + str(plot["label_size"]) + "pt}{7.2}\selectfont},")
            writer.write(TAB2 + r"tick label style = {font=\fontsize{" + str(plot["tick_label_size"]) + "pt}{7.2}\selectfont}")
            writer.write(TAB + r"}")
            writer.write(TAB + r"\begin{axis}[")
            writer.write(TAB2 + r"scale = " + str(plot["scale"]) + ",")
            writer.write(TAB2 + r"ymode=" + plot["y_axis_mode"] + ",")

            if plot["boxplot_draw_direction"] is not None:
                writer.write(TAB2 + r"boxplot/draw direction=" + plot["boxplot_draw_direction"] + r",")
            if plot["minor x tick num"] is not None:
                writer.write(TAB2 + r"minor x tick num=" + str(plot["minor x tick num"]) + r",")

            if plot["x_min"] is not None:
                writer.write(TAB2 + r"xmin=" + str(plot["x_min"]) + ",")
            if plot["x_max"] is not None:
                writer.write(TAB2 + r"xmax=" + str(plot["x_max"]) + ",")
            if plot["x_ticks_distance"] is not None:
                writer.write(TAB2 + r"xtick distance=" + str(plot["x_ticks_distance"]) + ",")
            if plot["x_ticks_labels"] is not None:
                writer.write(TAB2 + "")
            if plot["x_label"] is not None:
                writer.write(TAB2 + r"xlabel={" + plot["x_label"] + r"}, xlabel style={yshift=" + str(plot["x_label_offset"]) + r"em},")
            if plot["x_ticks"] is not None:
                writer.write(TAB2 + r"xtick=" + plot["x_ticks"] + ",")
            if plot["x_ticks_labels"] is not None:
                writer.write(TAB2 + r"xticklabels=" + plot["x_ticks_labels"] + ",")
            if plot["x_ticks_label_style"] is not None:
                writer.write(TAB2 + r"xticklabel style={")
                writer.write(TAB3 + r"align=" + plot["x_ticks_label_style"]["align"] + r",")
                writer.write(TAB3 + r"font=\fontsize{" + str(plot["x_ticks_label_style"]["font_size"]) + "pt}{7.2}\selectfont,")
                writer.write(TAB3 + r"rotate=" + str(plot["x_ticks_label_style"]["rotation"]) + r",")
                writer.write(TAB2 + r"},")

            if plot["y_min"] is not None:
                writer.write(TAB2 + r"ymin=" + str(plot["y_min"]) + ",")
            if plot["y_max"] is not None:
                writer.write(TAB2 + r"ymax=" + str(plot["y_max"]) + ",")
            if plot["y_ticks_distance"] is not None:
                writer.write(TAB2 + r"ytick distance=" + str(plot["y_ticks_distance"]) + ",")
            if plot["y_label"] is not None:
                writer.write(TAB2 + r"ylabel={" + plot["y_label"] + r"}, ylabel style={yshift=" + str(plot["y_label_offset"]) + r"em},")
            if plot["y_ticks"] is not None:
                writer.write(TAB2 + r"ytick=" + plot["y_ticks"] + ",")
            if plot["y_ticks_labels"] is not None:
                writer.write(TAB2 + r"yticklabels=" + plot["y_ticks_labels"] + ",")
            if plot["y_ticks_labels_style"] is not None:
                writer.write(TAB2 + r"yticklabel style={")
                writer.write(TAB3 + r"align=" + plot["y_ticks_labels_style"]["align"] + r",")
                writer.write(TAB3 + r"font=\fontsize{" + str(plot["y_ticks_labels_style"]["font_size"]) + "pt}{7.2}\selectfont,")
                writer.write(TAB3 + r"rotate=" + str(plot["y_ticks_labels_style"]["rotation"]) + r",")
                writer.write(TAB2 + r"},")


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

                add_plot_params += line_style
                
                if add_plot_params != "":
                    add_plot_params += r", color=" + color
                else:
                    add_plot_params += r"color=" + color
                
                if line_style == "boxplot":
                    add_plot_params += r", fill=" + str(data["fill_color"])
                    add_plot_params += r", fill opacity=" + str(data["fill_opacity"])
                    add_plot_params += r", mark=" + str(data["marker"])
                    add_plot_params += r", mark options={scale=" + str(data["marker_size"]) + ", fill=" + str(data["marker_color"]) + "}"
                else:
                    if marker is not None:
                        add_plot_params += r", thick, mark=" + marker
                    
                    add_plot_params += r", mark size=" + str(marker_size)

                writer.write(TAB2 + r"% " + "-" * 25)
                writer.write(TAB2 + r"% Plot for: " + label)
                writer.write(TAB2 + r"% " + "-" * 25)
                writer.write(TAB2 + r"\addplot[" + add_plot_params + r"]")
                if line_style == "boxplot":
                    writer.write(TAB2 + r"table[row sep=\\,y index=0] {")
                    writer.write(TAB3 + r"data\\")
                    for i in range(len(y)):
                       writer.write(TAB3 + str(y[i]) + r"\\")
                else:
                    writer.write(TAB2 + r"table{")
                    for i in range(len(y)):
                        writer.write(TAB3 + str(x[i]) + " " + str(y[i]))

                writer.write(TAB2 + r"};")

                if line_style != "boxplot":
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
                