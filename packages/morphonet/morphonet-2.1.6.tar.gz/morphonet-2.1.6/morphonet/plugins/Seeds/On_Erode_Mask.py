# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin
from ..functions import  get_borders, apply_new_label

class On_Erode_Mask(MorphoPlugin):
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
        self.set_name("On Erode Mask")
        self.add_inputfield("Iteration", default=2)
        self.add_inputfield("Volume_Minimum", default=1000)

    def process(self, t, dataset, objects):  # PLUGIN EXECUTION
        if not self.start(t, dataset, objects,backup=False):
            return None

        from skimage.morphology import binary_erosion
        from skimage.measure import label

        iteration = int(self.get_inputfield("Iteration"))
        min_vol = int(self.get_inputfield("Volume_Minimum"))
        import numpy as np
        nbc = 0
        for t in dataset.get_times(objects):
            data = dataset.get_seg(t)
            for o in dataset.get_objects_at(objects, t):
                cellCoords = np.where(data == o.id)
                self.print_mn('     ----->>>  Look for object ' + str(o.get_name()) + " with " + str(len(cellCoords[0])) + " voxels ")
                xmin, xmax, ymin, ymax, zmin, zmax = get_borders(data, cellCoords)
                cellShape = [1 + xmax - xmin, 1 + ymax - ymin, 1 + zmax - zmin]
                omask = np.zeros(cellShape, dtype=np.bool)
                omask[cellCoords[0] - xmin, cellCoords[1] - ymin, cellCoords[2] - zmin] = True
                mask = np.copy(omask)
                for n in range(iteration):
                    mask = binary_erosion(mask)
                splitted = label(mask)
                new_objects = np.unique(splitted)
                new_objects = new_objects[new_objects != 0]
                nbc = 0
                if len(new_objects)>=2:
                    for no in new_objects:
                        coords = np.where(splitted == no)
                        if len(coords[0]) <= min_vol:
                            self.print_mn("     ----->>>  found a small cell with  only " + str(len(coords[0])) + " voxels")
                        else:
                            self.print_mn("     ----->>>  add a cell with " + str(len(coords[0])) + " voxels")
                            cc = np.uint16([coords[0].mean(), coords[1].mean(), coords[2].mean()])
                            dataset.add_seed(cc)
                            nbc += 1
                if nbc <= 2:
                    self.print_mn(" ----->  not splittable with this erosion iteration value " + str(iteration))

        self.print_mn(" --> Found " + str(nbc) + " new seeds")
        self.restart()

