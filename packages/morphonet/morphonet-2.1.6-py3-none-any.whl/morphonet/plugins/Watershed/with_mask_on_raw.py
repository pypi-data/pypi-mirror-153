# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin
import numpy as np
from ..functions import  get_borders, apply_new_label,get_seed_at,get_seeds_in_mask,get_seeds_in_image,watershed,gaussian,get_barycenter

class With_Mask_On_Raw(MorphoPlugin):
    """ This plugin perform a watershed algorithm on a segmented region with new seeds passed in parameters

    Parameters
    ----------
    Gaussian_Sigma : int, default :2
        sigma parameters from the gaussian algorithm (from skimage) aplied on the rawdata
    Volume_Minimum: int, default : 1000
        minimum volume under wichi new object are created
    Seeds: Coordinate List
        List of seeds added on the MorphoNet Window

    """

    def __init__(self):  # PLUGIN DEFINITION
        MorphoPlugin.__init__(self)
        self.set_name("With Mask On Raw")
        self.add_inputfield("Gaussian_Sigma", default=2)
        self.add_inputfield("Volume_Minimum", default=1000)
        self.add_coordinates("Add a Seed")
        self.set_parent("Watershed")

    # Perform a watershed on a list of seed
    def _water_on_seed(self, dataset, t, data, seeds, objects, rawdata):
        print(" ----> perform watershed at " + str(t))
        cells_updated = []
        for o in dataset.get_objects_at(objects,t):
            cellCoords = np.where(data == o.id)
            self.print_mn('     ----->>>  Look in object ' + str(o.get_name()) + " with " + str(len(cellCoords[0])) + " voxels ")

            xmin, xmax, ymin, ymax, zmin, zmax = get_borders(data, cellCoords)
            cellShape = [1 + xmax - xmin, 1 + ymax - ymin, 1 + zmax - zmin]
            mask = np.zeros(cellShape, dtype=np.bool)
            mask[cellCoords[0] - xmin, cellCoords[1] - ymin, cellCoords[2] - zmin] = True

            # Keep only seeds in the mask

            nseeds = get_seed_at(seeds, xmin, ymin, zmin)
            #next_seeds = [col for i, col in enumerate(seeds) if i not in nseeds]
            seeds_in_cell_mask = get_seeds_in_mask(nseeds, mask)
            if len(seeds_in_cell_mask) < 2:  # If we have some seeds in this mask
                self.print_mn(" -----> " + str(len(seeds_in_cell_mask)) + "  is not enough  seeds in this mask")
            else:
                self.print_mn(" -----> Found " + str(len(seeds_in_cell_mask)) + " seeds in this mask")
                markers = np.zeros(mask.shape, dtype=np.uint16)
                newId = 1
                for seed in seeds_in_cell_mask:  # For Each Seeds ...
                    markers[seed[0], seed[1], seed[2]] = newId
                    newId += 1

                seed_preimage = rawdata[xmin:xmax + 1, ymin:ymax + 1, zmin:zmax + 1]
                if self.s_sigma > 0.0:
                    self.print_mn(" --> Perform gaussian with sigma=" + str(self.s_sigma) + " at " + str(t))
                    seed_preimage = gaussian(seed_preimage, sigma=self.s_sigma, preserve_range=True)

                self.print_mn(" --> Process watershed ")
                labelw = watershed(seed_preimage, markers=markers, mask=mask)

                data, c_newIds = apply_new_label(data, xmin, ymin, zmin, labelw, minVol=self.min_vol)
                if len(c_newIds) > 0:
                    c_newIds.append(o.id)
                    cells_updated += c_newIds

        if len(cells_updated) > 0:
            dataset.set_seg(t, data, cells_updated=cells_updated)
            #Recalculted New Seedsss
            new_seeds=[]
            for c in cells_updated:
                new_seeds.append(get_barycenter(data,c))
            return new_seeds
        return []

    def _water_time(self, dataset, t, seeds, objects):
        data = dataset.get_seg(t)
        rawdata = dataset.get_raw(t)
        if rawdata is None:
            return

        new_seeds = self._water_on_seed(dataset, t, data, seeds, objects, rawdata)
        if len(new_seeds) > 0 and t+1 in self.times:
            self._water_time(dataset, t + 1, new_seeds, objects)


    def process(self, t, dataset, objects):  # PLUGIN EXECUTION
        if not self.start(t, dataset, objects):
            return None
        self.s_sigma = int(self.get_inputfield("Gaussian_Sigma"))
        self.min_vol = int(self.get_inputfield("Volume_Minimum"))
        seeds = self.get_coordinates("Add a Seed")
        if len(seeds) == 0:
            print(" -> no seeds for watershed")
            self.restart()
            return None
        print(" --> Found " + str(len(seeds)) + " seeds ")
        seeds=get_seeds_in_image(dataset,seeds)

        self.times=dataset.get_times(objects)
        self._water_time(dataset, self.times[0], seeds, objects)
        self.restart()




