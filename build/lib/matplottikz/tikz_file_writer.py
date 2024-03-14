from matplottikz.utils import matplottikz_palette

class tikz_writer:
    def __init__(self, filename):
        self.filename = filename + ".tex"
        self.text = ""
        self.write(r"% " + "-" * 50)
        self.write(r"% This file was generated using matplottikz")
        self.write(r"% " + "-" * 50)
        self.write(r"\documentclass[crop,tikz]{standalone}")
        self.write(r"\usepackage{tikz}")
        self.write(r"\usepackage{pgfplots}")
        self.write(r"")

    def write_color_palette(self, n):
        self.write(r"% " + "-" * 50)
        self.write(r"% Matplottikz color palette generated using,")
        self.write(r"%     https://www.learnui.design/tools/data-color-picker.html#palette")
        self.write(r"% " + "-" * 50)
        for color in matplottikz_palette[n]:
            self.write(color)
        self.write(r"% " + "-" * 50)
        self.write(r"")

    def start_file(self):
        self.write(r"% " + "-" * 50)
        self.write(r"% Start of the document")
        self.write(r"% " + "-" * 50)

        self.write(r"\begin{document}")
        self.write(r"\begin{tikzpicture}")
    
    def end_file(self):
        self.write(r"\end{tikzpicture}")
        self.write(r"\end{document}")
        self.write(r"% " + "-" * 50)
        self.write(r"% End of the document")
        self.write(r"% " + "-" * 50)

    def write(self, text, end="\n", prefix=""):
        self.text += prefix + text + end

    def write_import_latex_cmd(self, filename, legend_name):
        self.write(r"")
        self.write("% To include the figure in your latex document, use the following commands:")
        self.write(r"")
        self.write(f"% \\begin{{figure}}[!htb]")
        self.write(f"%     \\centering")
        self.write(f"%     % Uncomment one of the following")
        self.write(f"%     %\\includegraphics[width=0.9\\columnwidth]{{figures/{filename}}}")
        self.write(f"%     %\\includestandalone[width=0.9\\columnwidth]{{figures/{filename}}}")
        if legend_name:
            self.write(f"%     \\hspace{{25pt}}\\ref{{{legend_name}}}")
        self.write(f"%     \\caption{{Write caption here.}}")
        self.write(f"%     \\label{{fig:{filename}}}")
        self.write(f"% \\end{{figure}}")


    def save(self):
        print(f"FILE_IO:Saving to {self.filename}")
        with open(self.filename, "w+") as f:
            f.write(self.text)
        self.text = ""
