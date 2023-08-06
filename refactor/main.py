import random

from refactor.controllers import SimpleController, GenerationController
from refactor.pygamegui import PygameGui

random.seed(20)

if __name__ == "__main__":
    controller = GenerationController(100, 2, 10)
    gui = PygameGui(controller)
    while controller.running:
        controller.step()
        gui.update()

