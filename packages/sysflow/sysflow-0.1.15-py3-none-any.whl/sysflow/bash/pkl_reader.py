import sys

from sysflow.utils.common_utils.file_utils import load


def main():
    pkl_file = sys.argv[1]
    assert pkl_file.endswith("pkl")
    pkl_data = load(pkl_file)
    print(pkl_data)


if __name__ == "__main__":
    # pkl test.pkl

    main()
