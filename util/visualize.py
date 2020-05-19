import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import Circle, PathPatch, Rectangle
from matplotlib.text import TextPath
from matplotlib.transforms import Affine2D
import mpl_toolkits.mplot3d.art3d as art3d

def text3d(ax, xyz, s, zdir="z", size=None, angle=0, usetex=False, **kwargs):
    '''
    Plots the string 's' on the axes 'ax', with position 'xyz', size 'size',
    and rotation angle 'angle'.  'zdir' gives the axis which is to be treated
    as the third dimension.  usetex is a boolean indicating whether the string
    should be interpreted as latex or not.  Any additional keyword arguments
    are passed on to transform_path.

    Note: zdir affects the interpretation of xyz.
    '''
    x, y, z = xyz
    if zdir == "y":
        xy1, z1 = (x, z), y
    elif zdir == "x":
        xy1, z1 = (y, z), x
    else:
        xy1, z1 = (x, y), z

    text_path = TextPath((0, 0), s, size=size, usetex=usetex)
    trans = Affine2D().rotate(angle).translate(xy1[0], xy1[1])

    p1 = PathPatch(trans.transform_path(text_path), **kwargs)
    ax.add_patch(p1)
    art3d.pathpatch_2d_to_3d(p1, z=z1, zdir=zdir)


"""plots head,gaze,screen,camera in 3D"""
def plot_all(head, gazes):
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
    ax.set_xlim3d(-60,60); ax.set_ylim3d(120,0); ax.set_zlim3d(-80,40)
#     ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
    
    # check gaze & plot gaze, projected onto z = 0 frame (i.e. the screen)
    gaze_color = ['orange','green']
    
    for i in range(2):
        look = 0
        scale = abs(head[2].copy()/gazes[i,2])
        g = gazes[i,:].copy()*scale + head
        if abs(g[0]) <= 30 and g[1] <= 0 and g[1] >= -40:
            look = 1
        
        ax.plot([g[0],head[0]], [0,head[2]], [g[1],head[1]],'o--', c=gaze_color[look], alpha=0.4, linewidth=5, markersize=16)
    
    # camera (origin)
    ax.scatter([0],[0],[0], marker='x', s=128, c='k')
    ax.text(0, 0, 5, "Camera",color='k',fontsize=16)
    
    # screen
    p = Rectangle((-30, -40), 60,40, color='gray',alpha=0.3)
    ax.add_patch(p)
    art3d.pathpatch_2d_to_3d(p, z=0, zdir="y")
    text3d(ax, (-25, 0, -20), "Screen", zdir="y", size=15, ec="none", fc="k", alpha=0.1)
    
    # plot head
    ax.scatter([head[0]],[head[2]],[head[1]], c='cornflowerblue', s=1200)
    ax.plot([head[0],-60],[head[2],head[2]],[head[1],head[1]], 'o--', c='cornflowerblue', alpha=0.4, linewidth=2, markersize=8)
    ax.plot([head[0],head[0]],[head[2],0],[head[1],head[1]], 'o--',c='cornflowerblue', alpha=0.4, linewidth=2, markersize=8)
    ax.plot([head[0],head[0]],[head[2],head[2]],[head[1],-80],'o--', c='cornflowerblue', alpha=0.4, linewidth=2, markersize=8)
    
    plt.close(fig)  
    b, (w,h) = fig.canvas.print_to_buffer()
    img_plot = np.frombuffer(b, dtype=np.uint8)
    img_plot = np.resize(img_plot, (h,w,4))[:,:,(2,1,0)] #bgr to rgb
    return img_plot

def plot_emotions(emotion_history):
    emo = np.array(emotion_history)+1

    fig = plt.figure(figsize=(12,4))
    plt.stackplot(np.arange(len(emo)), [emo,2-emo], colors=['mediumturquoise','lightcoral'], alpha=0.6)
    plt.plot(emo, c='#555555')
    plt.text(0,2.03,'sad',fontsize=12)
    plt.text(0,-0.13,'happy',fontsize=12)

    # size = ((np.arange(len(emo))**2)*64/len(emo)**2)[-20:]
    # plt.scatter(np.arange(len(emo))[-20:], emo[-20:],s=size, c='#444444')
    plt.xlim(0,60)
    plt.ylim(0,2)
    plt.xticks([])
    plt.yticks([])

    plt.close(fig)  
    b, (w,h) = fig.canvas.print_to_buffer()
    img_plot = np.frombuffer(b, dtype=np.uint8)
    img_plot = np.resize(img_plot, (h,w,4))[:,:,(2,1,0)] #rgb to bgr
    return img_plot


# """plots head,screen,camera in 3D"""
# def plot_head(head):
#     """
#     input: [x, y, z] of head
#     output: np.array image of 3D plot of everything 
#     """
#     # flip axes. actual axis order: x, z, y
#     head[0], head[1] = -head[0], -head[1]
#     fig = plt.figure(figsize=(12,9))
#     fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
#     ax = Axes3D(fig)#fig.gca(projection='3d')
#     ax.view_init(elev=20, azim=-60)
#     ax.set_xlim3d(-50,50); ax.set_ylim3d(100,0); ax.set_zlim3d(-80,50)
#     ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
    
#     # camera (origin) and screen
#     ax.scatter([0],[0],[0], marker='X', s=200, c='k')
#     ax.text(0, 0, 5, "Camera",color='k',fontsize=16)
    
#     # plot head
#     ax.scatter([head[0]],[head[2]],[head[1]], c='cornflowerblue', s=1000)
#     ax.plot([head[0],-50],[head[2],head[2]],[head[1],head[1]], 'o--', c='cornflowerblue', alpha=0.3, linewidth=2, markersize=12)
#     ax.plot([head[0],head[0]],[head[2],0],[head[1],head[1]], 'o--',c='cornflowerblue', alpha=0.3, linewidth=2, markersize=12)
#     ax.plot([head[0],head[0]],[head[2],head[2]],[head[1],-80],'o--', c='cornflowerblue', alpha=0.3, linewidth=2, markersize=12)

#     plt.close(fig)  
#     b, (w,h) = fig.canvas.print_to_buffer()
#     img_plot = np.frombuffer(b, dtype=np.uint8)
#     img_plot = np.resize(img_plot, (h,w,4))[:,:,(2,1,0)] #bgr to rgb
#     return img_plot