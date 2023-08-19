import random
import argparse

from controllers import SimpleController, GenerationController
from pygamegui import PygameGui

random.seed(30)

# args: generations, drivers, traffic, which nn is in use, traffic config
if __name__ == "__main__":
    """
    Instantiates the "universe" in which the highway exists. Updates the universe and the GUI frame by frame until 
    the universe ends (program goes through the specified # of generations or the 'q' key is pressed).
    """

    parser = argparse.ArgumentParser(prog="python main.py")
    parser.add_argument('-g', '--generations', type=int, help="Number of generations the program goes through")
    parser.add_argument('-d', '--drivers', type=int, help="Number of cars navigating through the traffic")
    parser.add_argument('-n', '--nn', type=str, help="File name of neural network to use (.pickle)")
    parser.add_argument('-p', '--traffic_pattern', type=str, help="File name of traffic pattern to use (.pickle)")

    args = parser.parse_args()

    g = args.generations if args.generations is not None else 100
    d = args.drivers if args.drivers is not None else 100
    p = args.traffic_pattern if args.traffic_pattern is not None else "savedata/cascade_up_traffic.pickle"
    n = args.nn if args.nn is not None else ""

    controller = GenerationController(g, d, p, n)
    gui = PygameGui(controller)
    while controller.running:
        controller.step()
        gui.update()
