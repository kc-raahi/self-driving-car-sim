from refactor.controllers import SimpleController
from refactor.pygamegui import PygameGui

if __name__ == "__main__":
    controller = SimpleController()
    gui = PygameGui(controller)
    while controller.running:
        controller.step()
        gui.update()

