import glob
import os
from PIL import Image

if __name__ == "__main__":
    frames = []
    frames5 = []
    frames10 = []
    imgs = glob.glob("*.png")[200:500]
    i = 0
    for img in imgs:
        frame = Image.open(img)
        frames.append(frame)
        if i % 5 == 0:
            frames5.append(frame)
        if i % 10 == 0:
            frames10.append(frame)

    frames[0].save("animated.gif", format='GIF', append_images=frames[1:], save_all=True, duration=300, loop=0)
    frames5[0].save("animated2.gif", format='GIF', append_images=frames5[1:], save_all=True, duration=60, loop=0)
    frames10[0].save("animated3.gif", format='GIF', append_images=frames10[1:], save_all=True, duration=30, loop=0)
    os.startfile("animated3.gif")
