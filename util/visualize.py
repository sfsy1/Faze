import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from mpl_toolkits.mplot3d import Axes3D

"""plots head in 3D"""

def plot_head(head):
    """
    input: [x, y, z] of head
    output: np.array image of 3D plot of everything 
    """
    # flip axes. actual axis order: x, z, y
    head[0], head[1] = -head[0], -head[1]
    fig = plt.figure(figsize=(12,9))
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    ax = Axes3D(fig)#fig.gca(projection='3d')
    ax.view_init(elev=20, azim=-60)
    ax.set_xlim3d(-50,50); ax.set_ylim3d(100,0); ax.set_zlim3d(-80,50)
    ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
    
    # camera (origin) and screen
    ax.scatter([0],[0],[0], marker='X', s=200, c='k')
    ax.text(0, 0, 5, "Camera",color='k',fontsize=16)
    
    # plot head
    ax.scatter([head[0]],[head[2]],[head[1]], c='cornflowerblue', s=1000)
    ax.plot([head[0],-50],[head[2],head[2]],[head[1],head[1]], 'o--', c='cornflowerblue', alpha=0.3, linewidth=2, markersize=12)
    ax.plot([head[0],head[0]],[head[2],0],[head[1],head[1]], 'o--',c='cornflowerblue', alpha=0.3, linewidth=2, markersize=12)
    ax.plot([head[0],head[0]],[head[2],head[2]],[head[1],-80],'o--', c='cornflowerblue', alpha=0.3, linewidth=2, markersize=12)

    plt.close(fig)  
    b, (w,h) = fig.canvas.print_to_buffer()
    img_plot = np.frombuffer(b, dtype=np.uint8)
    img_plot = np.resize(img_plot, (h,w,4))[:,:,(2,1,0)] #bgr to rgb
    return img_plot