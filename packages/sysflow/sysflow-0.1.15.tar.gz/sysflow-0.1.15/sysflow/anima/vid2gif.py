# https://github.com/wookayin/video2gif
# http://blog.pkh.me/p/21-high-quality-gif-with-ffmpeg.html#usage

r"""
video2gif: Convert a video file into a GIF.
The GIF should be (reasonably) compressed and high-quality.
Usage:
    $ video2gif foo.mp4
    $ video2gif foo.mp4 foo.gif --scale 640
"""

import argparse
import os.path
import re
import shlex
import subprocess as sp
import sys
import tempfile


def run(cmd: str):
    sys.stderr.write(cmd)
    sys.stderr.write("\n")
    sys.stderr.flush()
    return sp.call(cmd, shell=True)


def convert(inputfile, outputfile=None, *, fps=24, scale=None):
    if not os.path.exists(inputfile):
        sys.stderr.write("File does not exist: " + inputfile + "\n")
        return 1
    if not outputfile:
        outputfile = os.path.splitext(inputfile)[0] + ".gif"

    fd, tmpfile = tempfile.mkstemp(suffix=".png", prefix="video2gif-palette")
    os.close(fd)

    try:
        palette = tmpfile
        filters = f"fps={fps}"
        if scale:
            # e.g. 50% -> iw:50, ih:50
            match = re.search(r"^(\d+\.?\d*)%$", scale)
            if match:
                percent = float(match.group(1)) / 100.0
                scale = "iw*{percent:.2f}:ih*{percent:.2f}".format(percent=percent)

            filters += ",scale={scale}:-1:flags=lanczos".format(scale=scale)

        ctx = dict(
            inputfile=shlex.quote(inputfile),
            outputfile=shlex.quote(outputfile),
            filters=filters,
            palette=palette,
        )

        cmd = 'ffmpeg -v warning -i {inputfile} -vf "{filters},palettegen" -y {palette}'.format(
            **ctx
        )
        if run(cmd) != 0:
            return 1
        cmd = 'ffmpeg -v warning -i {inputfile} -i {palette} -lavfi "{filters} [x]; [x][1:v] paletteuse" -y {outputfile}'.format(
            **ctx
        )
        if run(cmd) != 0:
            return 1

    finally:
        try:
            os.remove(tmpfile)
        except OSError:
            pass

    return 0


def parse_args():
    desc = "convert the mp4 to gif"
    parser = argparse.ArgumentParser(description=desc)
    arg_lists = []

    def add_argument_group(name):
        arg = parser.add_argument_group(name)
        arg_lists.append(arg)
        return arg

    # animation arg
    anima_arg = add_argument_group("animation")

    anima_arg.add_argument("--inputfile", "-i", type=str, help="input file")
    anima_arg.add_argument("--outputfile", "-o", type=str, help="output file")
    anima_arg.add_argument(
        "--scale",
        default=None,
        type=str,
        help="Output scale. e.g. 640, 640:360, -1:480, iw*2:ih, 50%%",
    )
    anima_arg.add_argument("--fps", default=24, type=int, help="FPS (defaults 24)")

    args = parser.parse_args()

    return args


def main():
    global args
    args = parse_args()

    convert(**vars(args))


if __name__ == "__main__":
    main()
