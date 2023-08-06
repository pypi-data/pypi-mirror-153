from pathlib import Path
import cv2
import numpy as np
import wget


MODEL_FOLDER = Path(__file__).parent.parent / "model"
MODEL_FOLDER.mkdir(parents=True, exist_ok=True)


def check_exists_or_download(filename, url):
    path = MODEL_FOLDER / filename
    if not path.exists():
        print(f"{filename} not found, downloading...")
        wget.download(url, path.as_posix())
        print('\n')
    return path


PROTOTXT = check_exists_or_download(
    "colorization_deploy_v2.prototxt",
    r"https://raw.githubusercontent.com/PySimpleGUI/PySimpleGUI-Photo-Colorizer/master/model/colorization_deploy_v2.prototxt"
)
MODEL = check_exists_or_download(
    "colorization_release_v2.caffemodel",
    r"https://www.dropbox.com/s/dx0qvhhp5hbcx7z/colorization_release_v2.caffemodel?dl=1"
)
POINTS = check_exists_or_download(
    "pts_in_hull.npy",
    r"https://github.com/PySimpleGUI/PySimpleGUI-Photo-Colorizer/blob/master/model/pts_in_hull.npy?raw=true"
)


class Colorizer(object):
    def __init__(self):
        # load model from disk
        net = cv2.dnn.readNetFromCaffe(PROTOTXT.as_posix(), MODEL.as_posix())
        pts = np.load(POINTS)

        # add the cluster centers as 1x1 convolutions to the model
        class8 = net.getLayerId("class8_ab")
        conv8 = net.getLayerId("conv8_313_rh")
        pts = pts.transpose().reshape(2, 313, 1, 1)
        net.getLayer(class8).blobs = [pts.astype("float32")]
        net.getLayer(conv8).blobs = [np.full([1, 313], 2.606, dtype="float32")]
        self.net = net

    def __call__(self, filepath):
        file = Path(filepath)
        colorized = self.colorize_frame(cv2.imread(file.as_posix()))
        new_file = file.with_stem(f"{file.stem}_colored")
        cv2.imwrite(new_file.as_posix(), colorized)

    def convert_to_grayscale(self, frame):
        # Convert webcam frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Convert grayscale frame (single channel) to 3 channels
        gray_3_channels = np.zeros_like(frame)
        gray_3_channels[:, :, 0] = gray
        gray_3_channels[:, :, 1] = gray
        gray_3_channels[:, :, 2] = gray
        return gray_3_channels

    def colorize_frame(self, frame):
        scaled = frame.astype("float32") / 255.0
        lab = cv2.cvtColor(scaled, cv2.COLOR_BGR2LAB)

        # resize the Lab image to 224x224
        # (the dimensions the colorization network accepts)
        # split channels, extract the 'L' channel
        # and then perform mean centering
        resized = cv2.resize(lab, (224, 224))
        L = cv2.split(resized)[0]
        L -= 50

        # pass the L channel through the network
        # which will *predict* the 'a' and 'b' channel values
        self.net.setInput(cv2.dnn.blobFromImage(L))
        ab = self.net.forward()[0, :, :, :].transpose((1, 2, 0))

        # resize the predicted 'ab' volume
        # to the same dimensions as our input image
        ab = cv2.resize(ab, (frame.shape[1], frame.shape[0]))

        # grab the 'L' channel from the *original* input image
        # (not the resized one)
        # and concatenate the original 'L' channel
        # with the predicted 'ab' channels
        L = cv2.split(lab)[0]
        colorized = np.concatenate((L[:, :, np.newaxis], ab), axis=2)

        # convert the output image from the Lab color space to RGB,
        # then clip any values that fall outside the range [0, 1]
        colorized = cv2.cvtColor(colorized, cv2.COLOR_LAB2BGR)
        colorized = np.clip(colorized, 0, 1)

        # the current colorized image is represented
        # as a floating point data type in the range [0, 1]
        # -- let's convert to an unsigned 8-bit integer representation
        # in the range [0, 255]
        colorized = (255 * colorized).astype("uint8")
        return colorized
