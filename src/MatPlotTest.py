import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

fig = plt.figure(num=None, figsize=(5, 5))
plt.title("Tic Tac Toe")
#plt.axis('off')
plt.plot([0, 2, 4, 6], [0, 0, 0, 0], 'b-')
plt.plot([0, 2, 4, 6], [2, 2, 2, 2], 'b-')
plt.plot([0, 2, 4, 6], [4, 4, 4, 4], 'b-')
plt.plot([0, 2, 4, 6], [6, 6, 6, 6], 'b-')

plt.plot([0, 0, 0, 0], [0, 2, 4, 6], 'b-')
plt.plot([2, 2, 2, 2], [0, 2, 4, 6], 'b-')
plt.plot([4, 4, 4, 4], [0, 2, 4, 6], 'b-')
plt.plot([6, 6, 6, 6], [0, 2, 4, 6], 'b-')

plt.text(3, 3, "X", fontsize=25, horizontalalignment='center', verticalalignment='center', color='g', fontweight='bold')
plt.text(5, 1, "O", fontsize=25, horizontalalignment='center', verticalalignment='center', color='r', fontweight='bold')

plt.xlabel("Turn :X (QTPlayer)")
plt.tight_layout()
plt.show()
