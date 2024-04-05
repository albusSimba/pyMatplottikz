import numpy as np

TAB = " " * 4
TAB2 = " " * 8
TAB3 = " " * 12
TAB4 = " " * 16

marker_square = "square"
marker_pentagon = "pentagon"
marker_triangle = "triangle"
marker_o = "o"
marker_star = "Mercedes star"
marker_star_flipped = "Mercedes star flipped"
marker_diamond = "diamond"
marker_asterisk = "asterisk"
marker_star = "star"
marker_x = "x"
marker_plus = "+"
marker_o_plus = "oplus"
marker_minus = "−"
marker_line = "|"
marker_otimes = "otimes"

matplotlib_markers = {
    "square": "s",
    "pentagon": "p",
    "triangle": "^",
    "o": "o",
    "Mercedes star": "1",
    "Mercedes star flipped": "x",
    "diamond": "D",
    "asterisk": "*",
}
def boxplot_process_data(data):
    q1 = np.percentile(data, 0.25)
    q3 = np.percentile(data, 0.75)
    med = np.median(data)

    # finding the iqr region
    iqr = q3-q1
    
    # finding upper and lower whiskers
    upper_bound = q3+(1.5*iqr)
    lower_bound = q1-(1.5*iqr)

    # finding the outliers
    outliers = data[(data >= upper_bound) | (data <= lower_bound)]

    return q1, q3, med, upper_bound, lower_bound, outliers

def empty_plot_dict():
    return {
        "filename": None,
        "color": None,
        "shape": None,
        "height": 0.65,
        "width": 0.9,
        "boxplot_draw_direction": None,
        "tick_label_size": 7,
        "label_size": 9,
        
        "x_max": None,
        "x_min": None,
        "x_label": None,
        "x_ticks": None,
        "x_ticks_distance": None,
        "x_ticks_labels": None,
        "x_ticks_label_style": None,
        "x_label_offset": 0.8,
        "minor x tick num": None,
        
        "y_label": None,
        "y_ticks": None,
        "y_ticks_distance": None,
        "y_ticks_labels_style": None,
        "y_ticks_labels": None,
        "y_label_offset": -0.75,
        "y_max": None,
        "y_min": None,
        "y_axis_mode": "linear",
        
        "grid": None,
        "grid_style": "dashed",
        
        "legend_name": None,
        "legend_columns": 1,
        "legend_pos": None,
        "legend_style": {"anchor": "center",
                        "column_sep":2,
                        "font_size":7},
        
        "plots": {},
    }

matplottikz_palette = {
        3: [ 
            r"\definecolor{matplottikz-color1}{HTML}{003f5c}",
            r"\definecolor{matplottikz-color2}{HTML}{bc5090}",
            r"\definecolor{matplottikz-color3}{HTML}{ffa600}",
            ],
        4: [
            r"\definecolor{matplottikz-color1}{HTML}{003f5c}",
            r"\definecolor{matplottikz-color2}{HTML}{7a5195}",
            r"\definecolor{matplottikz-color3}{HTML}{ef5675}",
            r"\definecolor{matplottikz-color4}{HTML}{ffa600}",
            ],
        5: [
            r"\definecolor{matplottikz-color1}{HTML}{003f5c}",
            r"\definecolor{matplottikz-color2}{HTML}{58508d}",
            r"\definecolor{matplottikz-color3}{HTML}{bc5090}",
            r"\definecolor{matplottikz-color4}{HTML}{ff6361}",
            r"\definecolor{matplottikz-color5}{HTML}{ffa600}",
            ],
        6: [
            r"\definecolor{matplottikz-color1}{HTML}{003f5c}",
            r"\definecolor{matplottikz-color2}{HTML}{444e86}",
            r"\definecolor{matplottikz-color3}{HTML}{955196}",
            r"\definecolor{matplottikz-color4}{HTML}{dd5182}",
            r"\definecolor{matplottikz-color5}{HTML}{ff6e54}",
            r"\definecolor{matplottikz-color6}{HTML}{ffa600}",
            ],
        7: [
            r"\definecolor{matplottikz-color1}{HTML}{003f5c}",
            r"\definecolor{matplottikz-color2}{HTML}{374c80}",
            r"\definecolor{matplottikz-color3}{HTML}{7a5195}",
            r"\definecolor{matplottikz-color4}{HTML}{bc5090}",
            r"\definecolor{matplottikz-color5}{HTML}{ef5675}",
            r"\definecolor{matplottikz-color6}{HTML}{ff764a}",
            r"\definecolor{matplottikz-color7}{HTML}{ffa600}",
            ],
        8: [
            r"\definecolor{matplottikz-color1}{HTML}{003f5c}",
            r"\definecolor{matplottikz-color2}{HTML}{2f4b7c}",
            r"\definecolor{matplottikz-color3}{HTML}{665191}",
            r"\definecolor{matplottikz-color4}{HTML}{a05195}",
            r"\definecolor{matplottikz-color5}{HTML}{d45087}",
            r"\definecolor{matplottikz-color6}{HTML}{f95d6a}",
            r"\definecolor{matplottikz-color7}{HTML}{ff7c43}",
            r"\definecolor{matplottikz-color8}{HTML}{ffa600}",
            ]
        }
