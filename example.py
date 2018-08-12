from random import randrange

from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(10, 10))


def update(i):
    # im_normed = np.random.random((64, 64))
    im_normed = np.zeros((10, 10))
    im_normed[randrange(0, 10), randrange(0, 10)] = 1
    ax.imshow(im_normed,cmap='Greys')


anim = FuncAnimation(fig, update, frames=np.arange(0, 1), interval=100)
# anim.save('colour_rotation.gif', dpi=80, writer='imagemagick')
plt.show()