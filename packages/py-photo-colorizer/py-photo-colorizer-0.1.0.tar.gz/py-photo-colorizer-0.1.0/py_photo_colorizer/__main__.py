from sys import argv
from py_photo_colorizer.colorizer import Colorizer


def main(filenames):
    colorizer = Colorizer()
    for filename in filenames:
        colorizer(filename)


if __name__ == "__main__":
    main(argv[1:])
