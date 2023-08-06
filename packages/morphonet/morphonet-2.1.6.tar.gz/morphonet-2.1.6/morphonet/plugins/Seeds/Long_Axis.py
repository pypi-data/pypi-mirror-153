# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin


class Long_Axis(MorphoPlugin):
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
        self.set_name("Long Axis")
        self.add_inputfield("factor", default=8)

    def process(self, t, dataset, objects):  # PLUGIN EXECUTION
        if not self.start(t, dataset, objects,backup=False):
            return None

        factor = int(self.get_inputfield("factor"))
        import numpy as np
        from scipy.spatial.distance import cdist
        nbc = 0
        for t in dataset.get_times(objects):
            data = dataset.get_seg(t)
            data=data[::factor,::factor,::factor]
            for o in dataset.get_objects_at(objects, t):
                coords = np.where(data == o.id)  # Take the 2 farest points
                self.print_mn('     ----->>>  Look for object ' + str(o.get_name()) + " with " + str(factor*len(coords[0])) + " voxels ")
                vT = np.zeros([len(coords[0]), len(coords)])
                for s in range(len(coords)):
                    vT[:, s] = coords[s]

                dist = cdist(vT, vT)
                maxi = dist.max()
                coords_maxi = np.where(dist == maxi)
                #print(maxi)
                if len(coords_maxi[0]) >= 2:
                    ipt1 = coords_maxi[0][0]
                    ipt2 = coords_maxi[0][1]
                    pt1 = np.array([coords[0][ipt1], coords[1][ipt1], coords[2][ipt1]])*factor
                    pt2 = np.array([coords[0][ipt2], coords[1][ipt2], coords[2][ipt2]])*factor
                    v = pt2 - pt1
                    #print(v)
                    seed1 = np.int32(pt1 + v * 1.0 / 3.0)
                    seed2 = np.int32(pt1 + v * 2.0 / 3.0)
                    for seed in [seed1,seed2]:
                        dataset.add_seed(seed)
                        nbc += 1

        self.print_mn(" --> Found " + str(nbc) + " new seeds")
        self.restart()

