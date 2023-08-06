# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin
from skimage.morphology import extrema, binary_dilation
from skimage.filters import gaussian
from skimage.measure import label
import numpy as np
from ..functions import get_borders


class Minima_On_Mask(MorphoPlugin):
    """ This plugin create new seeds from a h min (or max) algorithm on the rawdata image
  If objects are selected, the function will be applied only on their mask
    If not, the function will be applied everywhere else there is no objects

    Parameters
    ----------
    Gaussian_Sigma : int, default :8
        sigma parameters from the gaussian algorithm (from skimage) applied on the rawdata in otder to perform the h minimum or maximum algorithm
    h_value : int, default :2
        the h value of h_minima or h_maxumum algorithm (see https://scikit-image.org/docs/stable/api/skimage.morphology.html )

    """

    def __init__(self):  # PLUGIN DEFINITION
        MorphoPlugin.__init__(self)
        self.set_parent("Create Seeds")
        self.set_name("Minima On Mask")
        self.add_inputfield("Gaussian_Sigma", default=8)
        self.add_dropdown("Method", ["H Minima", "Local Minima"])
        self.add_inputfield("h_value", default=2)

    def process(self, t, dataset, objects):  # PLUGIN EXECUTION
        if not self.start(t, dataset, objects, backup=False):
            return None

        s_sigma = int(self.get_inputfield("Gaussian_Sigma"))
        h_value = float(self.get_inputfield("h_value"))
        method=self.get_dropdown("Method")

        nbc = 0
        for t in dataset.get_times(objects):
            data = dataset.get_seg(t)
            rawdata = dataset.get_raw(t)
            if rawdata is None:
                break
            maxi = np.max(rawdata)

            for o in dataset.get_objects_at(objects, t):
                cellCoords = np.where(data == o.id)
                self.print_mn('     ----->>>  Look for object ' + str(o.get_name()) + " with " + str(
                    len(cellCoords[0])) + " voxels ")
                xmin, xmax, ymin, ymax, zmin, zmax = get_borders(data, cellCoords)

                if s_sigma > 0.0:  # Smoothing
                    self.print_mn("     ----->>>  Perform gaussian with sigma=" + str(s_sigma))
                    raw_mask = gaussian(rawdata[xmin:xmax + 1, ymin:ymax + 1, zmin:zmax + 1], sigma=s_sigma,preserve_range=True)
                else:
                    raw_mask = rawdata[xmin:xmax + 1, ymin:ymax + 1, zmin:zmax + 1]

                data_cell = data[xmin:xmax + 1, ymin:ymax + 1, zmin:zmax + 1]
                data_cell = data_cell != o.id  # Convert in Bool
                data_cell = binary_dilation(binary_dilation(data_cell))  # dilate to avoid seeds at the border
                raw_mask[data_cell] = maxi  # Create a Mask with high intensity

                if method=="H Minima":
                    local = extrema.h_minima(raw_mask, h_value)
                if method=="Local Minima":
                    local = extrema.local_minima(raw_mask)

                self.print_mn("     ----->>>  Perform labelisation")
                label_maxima, nbElts = label(local, return_num=True)
                if nbElts>100:
                    print(" ----> Found too much seeds : "+str(nbElts)+" Please, change parameters ")
                else:
                    for elt in range(1, nbElts + 1):
                        coord = np.where(label_maxima == elt)
                        coord = [coord[0][0] + xmin, coord[1][0] + ymin, coord[2][0] + zmin]
                        if data[coord[0], coord[1], coord[2]] == o.id:
                            dataset.add_seed(coord)
                            nbc += 1
                        else:
                            print(" ----> Seed out of mask at " + str(coord[0]) + "," + str(coord[1]) + "," + str(coord[2]))

        self.print_mn(" --> Found " + str(nbc) + " new seeds")
        self.restart()

