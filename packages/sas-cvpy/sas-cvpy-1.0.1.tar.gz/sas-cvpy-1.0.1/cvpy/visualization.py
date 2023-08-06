#!/usr/bin/env python
# encoding: utf-8
#
# Copyright SAS Institute
#
#  Licensed under the Apache License, Version 2.0 (the License);
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

''' Visualization tools '''

import sys
stdout = sys.stdout
stderr = sys.stderr

import struct
import numpy as np
from mayavi import mlab
import pandas as pd
import matplotlib.pylab as plt
from cvpy.image import *

sys.stdout = stdout
sys.stderr = stderr

def __mapping(val):

    '''
    "A simple mapping from int to int.

    Parameters
    ----------
    val : :class:`int`
        Specifies value to be mapped.

    Returns
    -------
    :class:`int`

    '''    
    
    if (val == 0):
        return 2
    elif (val == 2):
        return 0
    else:
        return val

def display_image_slice(images, dims, ress, fmts, poss, oris, scas, perm, image_index, slice_index, rf, imin=-100, imax=400, additive=0):

    '''
    Display an image slice in 3D.

    Parameters
    ----------
    images : :class:`str`
        Specifies the images.
    dims : :class:`pandas.Series`
        Specifies the dimensions of the image.
    ress : :class:`pandas.Series`
        Specifies the resolutions of the image.
    fmts : :class:`pandas.Series`
        Specifies the image formats.
    poss : :class:`pandas.Series`
        Specifies the positions of the image.
    oris : :class:`pandas.Series`
        Specifies the image format orientations of the image.
    scas : :class:`pandas.Series`
        Specifies the scaling of the image.
    perm : :class:`pandas.Series`
        Specifies the permissions of the image.
    image_index : :class:`pandas.Series`
        Specifies the image index.
    slice_index : :class:`tuple`
        Specifies the slice_index.
    imin : :class:`int`
        Specifies the input minimum.
    imax : :class:`int`
        Specifies the input maximum.
    additive : :class:`int`
        Specifies the additive.

    '''

    image = get_image_array(images, dims, ress, fmts, image_index)
    geo_perm = np.zeros(3, dtype=np.int)
    for i in range(3):
        geo_perm[__mapping(i)] = __mapping(perm[i])
    image = np.transpose(image, perm)
    image = image[slice_index, :, :] + additive
    nr, nc = image.shape[:2]
    dimension = int(dims[image_index])
    pos = np.array(struct.unpack('=%sd' % dimension, poss[image_index]))
    sca = np.array(struct.unpack('=%sd' % dimension, scas[image_index][0:8 * dimension]))
    ori = np.array(struct.unpack('=%sd' % (dimension*dimension), oris[image_index][0:8 * dimension * dimension]))
    xx, yy = np.meshgrid(np.linspace(0, nc, nc), np.linspace(0, nr, nr))
    zz = np.zeros((nr, nc))
    lc = np.vstack((np.reshape(xx, (1, nc*nr)), np.reshape(yy, (1, nc*nr)), np.reshape(zz, (1, nc*nr))))
    ori = np.reshape(ori, (3, 3))
    ori = ori[:, geo_perm]
    sca = sca[geo_perm]
    pos = pos + slice_index * sca[2] * ori[:, 2]
    pos = np.reshape(pos, (3, 1))
    sca = np.diag(sca)
    gc = np.matmul(ori, np.matmul(sca, lc))
    gc = gc + np.matmul(pos, np.ones((1, nc*nr)))
    mlab.mesh(np.reshape(gc[0, :], (nr, nc)), np.reshape(gc[1, :], (nr, nc)), np.reshape(gc[2, :], (nr, nc)),
              scalars = image, colormap='gray', vmin=imin, vmax=imax)
    if (rf):
        for i in range(3):
            clr=((i == 0) * 1, (i == 1) * 1, (i == 2) * 1)
            mlab.quiver3d(pos[0], pos[1], pos[2], ori[0, i], ori[1, i], ori[2, i],
                          line_width=5, scale_factor=50*sca[i, i], color=clr, mode='arrow')

def display_3D_image_slices_from_array(array, hold=False, slice_index_x=0, slice_index_y=0, slice_index_z=0):

    '''
    Display 3D image slices in 3D.

    Parameters
    ----------
    array : :class:`numpy.ndarray`
        Specifies the array to be displayed.
    hold : :class:`bool`
        When set to True, the display is held.
    
    '''

    sf = mlab.pipeline.scalar_field(array)
    mlab.pipeline.image_plane_widget(sf, plane_orientation="x_axes", slice_index=slice_index_x, colormap="gray")
    mlab.pipeline.image_plane_widget(sf, plane_orientation="y_axes", slice_index=slice_index_y, colormap="gray")
    mlab.pipeline.image_plane_widget(sf, plane_orientation="z_axes", slice_index=slice_index_z, colormap="gray")
    if (not hold):
        mlab.show()

def display_3D_image_slices(self, image, hold=False, slice_index_x=0, slice_index_y=0, slice_index_z=0):

    '''
    Display 3D image slices in 3D.

    Parameters
    ----------
    self : :class:`swat.CAS <swat.cas.connection.CAS>`
        Specifies the SWAT connection.
    image : :class:`str`
        Specifies the image to be displayed.
    hold : :class:`bool`
        When set to True, the display is held.
    slice_index_x : :class:`int`
        Specifies the slice index to be displayed on the x axis.
    slice_index_y : :class:`int`
        Specifies the slice index to be displayed on the y axis.
    slice_index_z : :class:`int`
        Specifies the slice index to be displayed on the z axis.

    '''

    rows=self.fetch(table=image, sastypes=False)['Fetch']
    dimensions = rows["_dimension_"]
    formats = rows["_channelType_"]
    binaries = rows["_image_"]
    resolutions = rows["_resolution_"]
    image_array = get_image_array( binaries, dimensions, resolutions, formats, 0)
    display_3D_image_slices_from_array(image_array, hold=False, slice_index_x=0, slice_index_y=0, slice_index_z=0)

def display_3D_surface(surfaces, vdata, fdata, hold=False, color=(1, 0, 0), op=1):

    '''
    Display the surfaces of an image.

    Parameters
    ----------
    surfaces : :class:`swat.SASDataFrame <swat.dataframe.SASDataFrame>`
        Specifies the surfaces to be displayed.
    vdata : :class:`swat.SASDataFrame <swat.dataframe.SASDataFrame>`
        Specifies the fetched vertices.
    fdata : :class:`swat.SASDataFrame <swat.dataframe.SASDataFrame>`
        Specifies the fetched faces.
    hold : :class:`bool`
        When set to True, the display is held.
    color : :class:`tuple`
        Specifies color of the surface.
    op : :class:`float`
        Specifies the opacity of the surface.

    '''

    sid = surfaces.iloc[0]['Surface Identifier']
    fetchv = vdata.query('_surfaceId_='+str(sid)).sort_values('_id_').to_frame()
    fetchf = fdata.query('_surfaceId_='+str(sid)).to_frame()
    sx = fetchv.loc[:, ["_x_"]]
    sy = fetchv.loc[:, ["_y_"]]
    sz = fetchv.loc[:, ["_z_"]]
    sflist = fetchf.loc[:, ["_v1_", "_v2_", "_v3_"]]
    mlab.triangular_mesh(sx, sy, sz, sflist, color=color, opacity=op)
    if (not hold):
        mlab.show()
