import cv2
import matplotlib.pyplot as plt



def finalize(fig_or_ax):
    # get the handle of some figure axis 
    try:
        ax = fig_or_ax.gca()
    except AttributeError:
        if type(fig_or_ax) is tuple:
            ax = fig_or_ax[0].gca()
        else:
            ax = fig_or_ax
    # magic
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    ymin, ymax = ax.get_ylim()
    xmin, xmax = ax.get_xlim()
    ax.imshow(frame, zorder=-1000, extent=[xmin, xmax, ymin,ymax], aspect='auto')
    cap.release()
    cv2.destroyAllWindows()
