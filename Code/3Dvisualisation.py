from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from example import packed_items

def plot_cuboid(origin, width, length, height, rotation):
    # get the coordinates of the vertices
    x,y,z = origin
    dx = width 
    dy = length
    dz = height

    if rotation == 0:
        w = dx
        l = dy
        h = dz
    elif rotation == 1:
        w = dz
        l = dx
        h = dy
    elif rotation == 2:
        w = dz
        l = dy
        h = dx
    elif rotation == 3:
        w = dy
        l = dz
        h = dx
    elif rotation == 4:
        w = dy
        l = dx
        h = dz
    elif rotation == 5:
        w = dx
        l = dz
        h = dy
    
    vertices = np.array([[x, y, z],
                         [x + w, y, z],
                         [x + w, y + l, z],
                         [x, y + l, z],
                         [x, y, z + h],
                         [x + w, y, z + h],
                         [x + w, y + l, z + h],
                         [x, y + l, z + h]])
    # get the indices of the vertices for each face
    faces = np.array([[0, 1, 2, 3],
                      [4, 5, 6, 7],
                      [0, 1, 5, 4],
                      [1, 2, 6, 5],
                      [2, 3, 7, 6],
                      [3, 0, 4, 7]])
    # create a Poly3DCollection object with the face coordinates
    cuboid = Poly3DCollection(vertices[faces] ,edgecolors='k', facecolors='y', linewidths=1, alpha=0.5)
    return cuboid

# create a figure and a 3D axes
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

packed_data = packed_items[['Container_id','Width','Length','Height','Position','Rotation','Console_Width','Console_Length','Console_Height']]

container_data = packed_data[packed_data['Container_id'] == '-5140415174795267898']

prefix = 'cuboid_'
var_num = 0

l = []

for _,row in container_data.iterrows():
    origin = row['Position']
    width = row['Width']
    length = row['Length']
    height = row['Height']
    rotation = row['Rotation']
    globals()[prefix + str(var_num)] = plot_cuboid(origin,width,length,height,rotation)
    l.append(ax.add_collection3d(globals()[prefix + str(var_num)]))
    var_num = var_num + 1


# plot a yellow cuboid with origin (1 ,2 ,3) and size (4 ,5 ,6)
# cuboid = plot_cuboid([0,0,0], 159, 108, 152, 0)
# cuboid1 = plot_cuboid([0,108.0,0],140,115,115,0)
# cuboid2 = plot_cuboid([0,0,152.0],160,100,120,0)
# cuboid3 = plot_cuboid([0,108.0,115.0],138,115,120,0)
# cuboid4 = plot_cuboid([140.0,108.0,0],185,80,120,3) 
# cuboid5 = plot_cuboid([140.0,108.0,185.0],153,88,88,1)
# cuboid6 = plot_cuboid([0,223.0,0],140,86,128,0)
# cuboid7 = plot_cuboid([0,223.0,128.0],135,87,128,0)
# cuboid8 = plot_cuboid([0,335.0,212.0],128,86,113,1)
# cuboid9 = plot_cuboid([140.0,228.0,0],130,82,90,2)
# cuboid10 = plot_cuboid([159.0,0,0],90,72,72,1)
# öl = [ax.add_collection3d(cuboid),ax.add_collection3d(cuboid1),ax.add_collection3d(cuboid2),ax.add_collection3d(cuboid3),
#       ax.add_collection3d(cuboid4),ax.add_collection3d(cuboid5),ax.add_collection3d(cuboid6),ax.add_collection3d(cuboid7),
#       ax.add_collection3d(cuboid8),ax.add_collection3d(cuboid9),ax.add_collection3d(cuboid10)]

# set the axes limits and labels
ax.set_xlim(0 ,container_data['Console_Width'].mean())
ax.set_ylim(0 ,container_data['Console_Length'].mean())
ax.set_zlim(0 ,container_data['Console_Height'].mean())
ax.set_xlabel('Width')
ax.set_ylabel('Length')
ax.set_zlabel('Height')

# show the plot
plt.show()