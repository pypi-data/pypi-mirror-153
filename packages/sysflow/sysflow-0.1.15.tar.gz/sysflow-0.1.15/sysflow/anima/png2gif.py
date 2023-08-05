import argparse
import os
import re

from PIL import Image


def parse_args():
    desc = "convert the png's to gif"
    parser = argparse.ArgumentParser(description=desc)
    arg_lists = []

    def add_argument_group(name):
        arg = parser.add_argument_group(name)
        arg_lists.append(arg)
        return arg

    # animation arg
    anima_arg = add_argument_group("animation")

    anima_arg.add_argument("--input", "-i", type=str, help="input file")
    anima_arg.add_argument("--output", "-o", type=str, help="output file")

    args = parser.parse_args()

    return args


def png2gif(in_folder, out_file):
    """convert the figures in the in_folder folder to out_file in the gif format

    Args:
        in_folder (str): figure folder, the figures are in the format abc0001.png, abc0002.png, ....
        out_file (str): output file name
    """

    in_files = os.listdir(in_folder)
    in_png = filter(lambda x: x.endswith(".png"), in_files)
    in_png = map(lambda x: os.path.join(in_folder, x), in_png)
    in_png = sorted(in_png, key=lambda a: int(re.findall("\d+", a)[-1]))

    images = []
    for n, a in enumerate(in_png):
        exec("a" + str(n) + ' = Image.open("' + '{}")'.format(a))
        images.append(eval("a" + str(n)))

    images[0].save(
        out_file if out_file else "out.gif",
        save_all=True,
        append_images=images[1:],
        duration=50,
        loop=0,
    )


def main():
    global args
    args = parse_args()

    png2gif(args.input, args.output)


if __name__ == "__main__":
    main()
