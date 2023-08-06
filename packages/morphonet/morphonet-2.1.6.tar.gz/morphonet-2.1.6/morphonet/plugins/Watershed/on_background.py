# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin
import numpy as np
from ..functions import _centerInShape, get_seeds_in_image, watershed


class On_Background(MorphoPlugin):
    """ This plugin perform a watershed algorithm on the background of the image based on seeds pass in parameters

    Parameters
    ----------
    Gaussian_Sigma : int, default :2
        sigma parameters from the gaussian algorithm (from skimage) aplied on the rawdata
    Volume_Minimum: int, default : 1000
        minimum volume under wichi new object are created
    Inverse: Dropdown
        applied the watershed on inverted rawdata (for image on black or white background)
    Seeds: Coordinate List
        List of seeds added on the MorphoNet Window

    """

    def __init__(self):  # PLUGIN DEFINITION
        MorphoPlugin.__init__(self)
        self.set_name("On Background")
        self.add_inputfield("Volume Minimum", default=1000)
        self.add_inputfield("Box size", default=50)
        self.add_coordinates("Add a Seed")
        self.set_parent("Watershed")

    def process(self, t, dataset, objects):  # PLUGIN EXECUTION
        if not self.start(t, dataset, objects, objects_require=False):
            return None

        min_vol = int(self.get_inputfield("Volume Minimum"))
        box_size = int(self.get_inputfield("Box size"))

        data = dataset.get_seg(t)

        seeds = self.get_coordinates("Add a Seed")
        if len(seeds) == 0:
            print(" -> no seeds for watershed")
            return None
        print(" --> Found " + str(len(seeds)) + " seeds ")
        dataset.get_center(data)
        seeds = get_seeds_in_image(dataset, seeds)
        new_seed = []
        for seed in seeds:
            if _centerInShape(seed, data.shape):
                olid = data[seed[0], seed[1], seed[2]]
                if olid == dataset.background:
                    new_seed.append(seed)
                    self.print_mn(" ----> add seed " + str(seed))
                else:
                    self.print_mn(
                        " ----> remove this seed " + str(seed) + " which already correspond to cell " + str(olid))
            else:
                self.print_mn(" ----> this seed " + str(seed) + " is out of the image")

        if len(new_seed) == 0:
            self.restart()
            return None

        #new_seed = [] ;  new_seed.append([339, 531, 339])

        if box_size > 0:  # Perform on a specific Box arround the seeds
            seedsa = np.array(new_seed)
            box_coords = {}
            for i in range(3):
                mi = max(0, seedsa[:, i].min() - box_size)
                ma = min(data.shape[i], seedsa[:, i].max() + box_size)
                box_coords[i] = [mi, ma]

            # Crop the data
            ndata = data[box_coords[0][0]:box_coords[0][1], box_coords[1][0]:box_coords[1][1],
                    box_coords[2][0]:box_coords[2][1]]

            # Replace the seed in the box
            box_seed = []
            for s in new_seed:
                box_seed.append([s[0] - box_coords[0][0], s[1] - box_coords[1][0], s[2] - box_coords[2][0]])
            new_seed = box_seed
        else:
            ndata = data

        markers = np.zeros(ndata.shape, dtype=np.uint16)
        markers[0, :, :] = 1
        markers[:, 0, :] = 1
        markers[:, :, 0] = 1
        markers[ndata.shape[0] - 1, :, :] = 1
        markers[:, ndata.shape[1] - 1, :] = 1
        markers[:, :, ndata.shape[2] - 1] = 1

        newId = 2
        for seed in new_seed:  # For Each Seeds ...
            markers[seed[0], seed[1], seed[2]] = newId
            newId += 1

        # Create The Mask
        mask = np.ones(ndata.shape, dtype=np.bool)
        mask[ndata != dataset.background] = False

        self.print_mn(" --> Process watershed ")
        labelw = watershed(mask, markers=markers, mask=mask)

        cMax = data.max() + 1
        nbc = 0
        new_ids = np.unique(labelw)
        new_ids = new_ids[new_ids > 1]  # REMOVE THE BORDERS
        if len(new_ids) > 0:
            self.print_mn(" --> Combine new objects")
            cells_updated = []
            for new_id in new_ids:
                newIdCoord = np.where(labelw == new_id)
                if len(newIdCoord[0]) > min_vol:
                    if box_size > 0:
                        newIdCoord = (newIdCoord[0] + box_coords[0][0], newIdCoord[1] + box_coords[1][0],
                                      newIdCoord[2] + box_coords[2][0])
                    data[newIdCoord] = cMax + nbc
                    self.print_mn(
                        " ----> add object " + str(nbc + cMax) + ' with  ' + str(len(newIdCoord[0])) + " voxels")
                    cells_updated.append(cMax + nbc)
                    nbc += 1
                else:
                    self.print_mn(" ----> remove object with  " + str(len(newIdCoord[0])) + " voxels")
            if len(cells_updated) > 0:
                dataset.set_seg(t, data, cells_updated=cells_updated)
        self.print_mn(" --> Found  " + str(nbc) + " new labels")
        self.restart()




