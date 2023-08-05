from faser.napari.gui import generate_psf_gui

import napari
import numpy as np
import argparse


def main(**kwargs):
    viewer = napari.Viewer()
    viewer.window.add_dock_widget(generate_psf_gui, area="right", name="Faser")
    napari.run()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    main()
