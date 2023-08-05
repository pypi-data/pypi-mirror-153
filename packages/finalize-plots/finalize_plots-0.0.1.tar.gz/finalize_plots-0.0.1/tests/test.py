import sys,os
moduleroot = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
moduleroot = os.path.dirname(moduleroot)
sys.path.append(moduleroot)
from finalize_plots import finalize
import matplotlib.pyplot as plt


fig = plt.figure()
plt.plot([1,2,3,4,5,6,7],[2,3,5,8,6,5,6], ls='-', lw=5, color='royalblue')

finalize(fig)
plt.show()
