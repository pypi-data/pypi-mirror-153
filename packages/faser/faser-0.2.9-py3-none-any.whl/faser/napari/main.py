from faser.napari.gui import generate_psf_gui, convolve_image_gui, make_effective_gui
from skimage import data
import napari
import numpy as np
import argparse
from scipy.sparse import random


def main(**kwargs):
    viewer = napari.Viewer()
    viewer.window.add_dock_widget(generate_psf_gui, area="right", name="Faser")
    viewer.window.add_dock_widget(convolve_image_gui, area="right", name="Convov")
    viewer.window.add_dock_widget(make_effective_gui, area="right", name="Convov")

    x = np.random.randint(0, 400, size=(100))
    y = np.random.randint(0, 400, size=(100))
    z = np.random.randint(0, 20, size=(100))

    M = np.zeros((400, 400, 20))
    for p in zip(x, y, z):
        M[p] = 1

    viewer.add_image(M, name="Space")
    napari.run()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    main()
