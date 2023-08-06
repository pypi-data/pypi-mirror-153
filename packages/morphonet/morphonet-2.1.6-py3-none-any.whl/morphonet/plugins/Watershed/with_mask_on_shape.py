# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin
import numpy as np
from ..functions import get_borders, apply_new_label,get_seed_at,get_seeds_in_mask,get_seeds_in_image,watershed,get_barycenter
from morphonet.tools import imsave

class With_Mask_On_Shape(MorphoPlugin):
    """ This plugin perform a watershed algorithm on a segmented region with new seeds passed in parameters

    Parameters
    ----------
    Volume_Minimum: int, default : 1000
        minimum volume under wichi new object are created
    Seeds: Coordinate List
        List of seeds added on the MorphoNet Window

    """

    def __init__(self):  # PLUGIN DEFINITION
        MorphoPlugin.__init__(self)
        self.set_name("With Mask On Shape")
        self.add_inputfield("Volume_Minimum", default=1000)
        self.add_coordinates("Add a Seed")
        self.set_parent("Watershed")

    # Perform a watershed on a list of seed
    def _water_on_seed(self, dataset, t, data, seeds, objects):
        print(" -----> Perform watershed at " + str(t))
        cells_updated = []
        for o in dataset.get_objects_at(objects,t):
            cellCoords = np.where(data == o.id)
            self.print_mn('     ----->>>  Look in object ' + str(o.get_name()) + " with " + str(len(cellCoords[0])) + " voxels ")

            xmin, xmax, ymin, ymax, zmin, zmax = get_borders(data, cellCoords)
            cellShape = [1 + xmax - xmin, 1 + ymax - ymin, 1 + zmax - zmin]
            mask = np.zeros(cellShape, dtype=np.bool)
            mask[cellCoords[0] - xmin, cellCoords[1] - ymin, cellCoords[2] - zmin] = True
            # Keep only seeds in the mask
            nseeds=get_seed_at(seeds,xmin,ymin,zmin)
            #unused_seeds = [col for i, col in enumerate(seeds) if i not in nseeds]
            seeds_in_cell_mask = get_seeds_in_mask(nseeds,mask)
            if len(seeds_in_cell_mask) < 2: # If we have some seeds in this mask
                self.print_mn(" -----> " + str(len(seeds_in_cell_mask)) + "  is not enough  seeds in this mask")
            else:
                self.print_mn(" -----> Found " + str(len(seeds_in_cell_mask))  + " seeds in this mask")
                markers = np.zeros(mask.shape, dtype=np.uint16)
                newId = 1
                for seed in seeds_in_cell_mask:  # For Each Seeds ...
                    markers[seed[0] , seed[1], seed[2] ] = newId
                    newId+=1

                self.print_mn(" -----> Process watershed ")
                print(str(np.where(mask==True)))
                labelw = watershed(255-mask, markers=markers, mask=mask)
                imsave("markers_28_162.tiff",markers)
                coords_mask = np.where(mask==True)
                mask.dtype='uint8'
                mask[coords_mask] = 255
                imsave("mask_28_162.tiff",mask)
                imsave("255mask_28_162.tiff",255-mask)
                data, c_newIds = apply_new_label(data, xmin, ymin, zmin, labelw, minVol=self.min_vol)
                if len(c_newIds) > 0:
                    c_newIds.append(o.id)
                    cells_updated+=c_newIds

        if len(cells_updated) > 0:
            dataset.set_seg(t, data, cells_updated=cells_updated)
            #Recalculted New Seeds
            new_seeds=[]
            for c in cells_updated:
                new_seeds.append(get_barycenter(data,c))
            return new_seeds
        return []


    def _water_time(self, dataset, t, seeds, objects):
        data = dataset.get_seg(t)
        new_seeds = self._water_on_seed(dataset, t, data, seeds, objects)
        if len(new_seeds) > 0 and t + 1 in self.times:
            self._water_time(dataset, t + 1, new_seeds, objects)


    def process(self, t, dataset, objects):  # PLUGIN EXECUTION
        if not self.start(t, dataset, objects):
            return None
        self.min_vol = int(self.get_inputfield("Volume_Minimum"))
        seeds = self.get_coordinates("Add a Seed")
        if len(seeds) == 0:
            print(" -> no seeds for watershed")
            return None
        print(" --> Found "+str( len(seeds))+ " seeds ")
        seeds = get_seeds_in_image(dataset, seeds)

        self.times = dataset.get_times(objects)
        self._water_time(dataset, self.times[0], seeds, objects)
        self.restart()




