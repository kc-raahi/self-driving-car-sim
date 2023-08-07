import random
import sys

from controllers import SimpleController, GenerationController
from pygamegui import PygameGui

random.seed(20)

if __name__ == "__main__":
    controller = GenerationController(100, 100, 10)
    gui = PygameGui(controller)
    while controller.running:
        controller.step()
        gui.update()

