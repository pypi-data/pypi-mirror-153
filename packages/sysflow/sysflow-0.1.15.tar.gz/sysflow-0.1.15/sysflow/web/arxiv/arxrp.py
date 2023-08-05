import pyperclip
import re
import argparse


def parse_args():
    desc = "replace the macro for an arxiv paper"
    parser = argparse.ArgumentParser(description=desc)
    arg_lists = []

    def add_argument_group(name):
        arg = parser.add_argument_group(name)
        arg_lists.append(arg)
        return arg

    # latex path
    arx_arg = add_argument_group("latex")
    arx_arg.add_argument("path", type=str, help="the path of the latex")
    args = parser.parse_args()

    return args


def to_raw(string):
    # some hard code
    return (
        string.replace("\\", "\\\\")
        .replace("\\\\g<", "\\g<")
        .replace("?!\\\\w", "?!\w")
    )


def translate(text, conversion_dict, before=None):
    """
    Translate words from a text using a conversion dictionary

    Arguments:
        text: the text to be translated
        conversion_dict: the conversion dictionary
        before: a function to transform the input
        (by default it will do nothing)
    """
    # if empty:
    if not text:
        return text
    # preliminary transformation:
    if before:
        t = before(text)
    else:
        t = text
    for key, value in conversion_dict.items():
        t = re.sub(key, value, t)

    return t


def latex_replace(input_file):
    assert input_file.endswith(".tex")
    output_file = input_file.replace(".tex", "_replace.tex")

    with open(input_file, "r") as f:
        input_lines = f.readlines()

    start_trans = False

    replace_dict = {}
    output_lines = []
    for line in input_lines:

        # case I:
        # \DeclareMathOperator{\Ker}{Ker}
        # ====>
        # \newcommand{\Ker}{\operatorname{Ker}}
        if line.startswith("\\DeclareMathOperator"):
            line = re.sub(
                r"\\DeclareMathOperator\**{(.*)}{(.*)}",
                r"\\newcommand{\g<1>}{\operatorname{\g<2>}}",
                line,
            )

        # case II:
        # A = '\def\hh{\hat{h}}'
        # re.sub(r'\\def(.*?){(.*)}',r'\\newcommand{\g<1>}{\g<2>}', A)
        if line.startswith("\\def"):
            line = re.sub(r"\\def(.*?){(.*)}", r"\\newcommand{\g<1>}{\g<2>}", line)

        if (
            line.startswith("\\newcommand")
            or line.startswith("\\renewcommand")
            or line.startswith("\\providecommand")
        ):
            keyword = re.findall("((new|renew|provide)command)", line)
            keyword = keyword[0][0]

            if len(re.findall(r"\[(\d)\]", line)) != 0:
                num_params = int(re.findall(r"\[(\d)\]", line)[0])
            else:
                num_params = 0

            if num_params:
                # example
                # \newcommand{\ip}[1] {\langle #1 \rangle }
                # r'\\ip{(.*)}': r'\\langle \g<1> \\rangle'

                try: 
                    line_map = re.findall(
                        r"\\{}".format(keyword) + r"\**{(.*?)}\s*\[\d\]\s*{(.*)}", line
                    )[0]
                except: 
                    line_map = re.findall(
                        r"\\{}".format(keyword) + r"\**(.*?)\s*\[\d\]\s*{(.*)}", line
                    )[0]

                assert len(line_map) == 2
                key, value = line_map

                key = key + "{(.*?)}" * num_params

                for i in range(num_params):
                    i += 1
                    value = value.replace("#{}".format(i), "\g<{}>".format(i))

                # example (nested newcommand)
                # \newcommand{\cA}{\mathcal{A}}
                # \newcommand{\das}{\Delta_{\cA}^{\cS}}

                value = translate(value, replace_dict)
                replace_dict[to_raw(key)] = to_raw(value)

            else:
                # example
                # \newcommand{\minimize}{\mathop{\textrm{minimize}}}
                # line_map = re.findall(r'\\newcommand{(.*?)}{(.*)}', line)[0]

                # star: for \renewcommand*{\thepa}{\alph{pa}}
                try: 
                    line_map = re.findall(
                        r"\\{}".format(keyword) + r"\**{(.*?)}{(.*)}", line
                    )[0]
                except: 
                    line_map = re.findall(
                        r"\\{}".format(keyword) + r"\**(.*?){(.*)}", line
                    )[0]

                assert len(line_map) == 2

                key, value = line_map
                # avoid
                # \newcommand{\be}{\mathbf{e}}
                # changes \begin
                # look ahead negative
                key = key + "(?![a-z])"
                value = translate(value, replace_dict)

                # extra space
                value = " " + value

                replace_dict[to_raw(key)] = to_raw(value)

        else:
            if start_trans:
                if len(line.strip()):
                    line = translate(line, replace_dict)

            output_lines.append(line)

        if r"\begin{document}" in line:
            start_trans = True

            print("Replace mapping: ")
            for a, b in replace_dict.items():
                print(a, ":", b)

    with open(output_file, "w") as f:
        f.write("".join(output_lines))


def main():
    global args
    args = parse_args()

    latex_replace(args.path)


if __name__ == "__main__":
    # usage:
    # 1. flap the latex: flap my/project/main.tex my/output
    # 2. replace the latex

    # testing 
    import urllib.request
    import os 

    print('Download paper')
    url = 'https://arxiv.org/e-print/2007.02151'
    fname = '2007.02151.tar.gz'
    urllib.request.urlretrieve(url, fname)

    print('Unzip the files')
    import tarfile

    tar = tarfile.open(fname, "r:gz")
    tar.extractall(path='latexreplace')
    tar.close()

    print('Replace macro')
    print()
    texfile = 'latexreplace/draft.tex' 

    latex_replace(texfile)

