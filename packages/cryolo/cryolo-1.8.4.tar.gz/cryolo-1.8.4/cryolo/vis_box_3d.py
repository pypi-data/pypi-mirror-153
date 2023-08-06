from mpl_toolkits.mplot3d import Axes3D
import cryolo.CoordsIO as CoordsIO
import matplotlib.pyplot as plt
import numpy

pth = "/home/twagner/Projects/Tomography/results/202009_cryolo_predict3d/more_ribosomes_michael/out_t25/CBOX_UNTRACED/d01t25_b8_lp60.cbox"
pth = "/home/twagner/Projects/Tomography/results/202009_cryolo_predict3d/pranav/out_picking_tf15_tw/CBOX_UNTRACED/dlp_fid10_049_rec.cbox"

boxes = CoordsIO.read_cbox_boxfile(pth)

xcoords = [box.x for box in boxes if box.c>0.3]
ycoords = [box.y for box in boxes if box.c>0.3]
zcoords = [box.z for box in boxes if box.c>0.3]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(xcoords,ycoords,zcoords)
plt.show()