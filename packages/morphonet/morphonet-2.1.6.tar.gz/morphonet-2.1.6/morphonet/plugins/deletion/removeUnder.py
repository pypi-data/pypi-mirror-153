# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin
import numpy as np

class RemoveUnder(MorphoPlugin):
    """ This plugin remove opbjects under a certain volume in the segmented image
  
    Parameters
    ----------
    Voxel Size: int, default 20
        The volume under which objecs as to be remove
    """

    def __init__(self): #PLUGIN DEFINITION 
        MorphoPlugin.__init__(self) 
        self.set_name("Remove Under")
        self.add_inputfield("Voxel Size",default=50)
        self.add_dropdown("Time points",["Current time","All times"])
        self.set_parent("Remove objects")
       

    def process(self,t,dataset,objects): #PLUGIN EXECUTION
        if not self.start(t,dataset,objects,objects_require=False):
            return None


        voxel_size=float(self.get_inputfield("Voxel Size"))
        if str(self.get_dropdown("Time points")) == "All times":
            cell_volume = dataset.get_info("cell_volume", info_type="float")
            for i in range(self.dataset.begin,self.dataset.end+1):
                #print("looking for delete in time : "+str(i))
                data=dataset.get_seg(i)
                sorted_info = sorted(cell_volume.data.items(), key=lambda x: x[1][0].value)
                cell_updated=[]
                for cell in sorted_info:
                    if cell[1][0].value <voxel_size:
                        if dataset.begin <= cell[0].t <= dataset.end:
                            dataset.backup(i)
                            coords = np.where(data == cell[0].id)
                            self.print_mn("     ----->>>  delete object " + str(cell[0].id) + " at " + str(cell[0].t) + " with " + str(cell[1][0].value) + " voxels")
                            data[coords] = dataset.background
                            for m in cell[0].mothers:
                                dataset.del_mother(cell[0],m)
                            for d in cell[0].daughters:
                                dataset.del_daughter(cell[0],d)
                            dataset.remove_cell_from_infos(cell[0].t,cell[0].id)
                            cell_updated.append(cell[0].id)

                    else :
                        break
                if len(cell_updated)>0:
                    dataset.set_seg(i, data, cells_updated=cell_updated)
        else :
            data=dataset.get_seg(t)
            dataset._set_volume(data,t)  #We Recompute All Volumes to avoid small cells issues
            cell_volume = dataset.get_info("cell_volume", info_type="float")
            sorted_info = sorted(cell_volume.data.items(), key=lambda x: x[1][0].value)
            cell_updated=[]
            for cell in sorted_info:
                if cell[1][0].value < voxel_size:
                    if cell[0].t == t:
                        dataset.backup(t)
                        self.print_mn("     ----->>>  delete object " + str(cell[0].id) + " at " + str(cell[0].t) + " with " + str(cell[1][0].value) + " voxels")
                        data[np.where(data == cell[0].id)] = dataset.background
                        for m in cell[0].mothers:
                            dataset.del_mother(cell[0],m)
                        for d in cell[0].daughters:
                            dataset.del_daughter(cell[0],d)
                        dataset.remove_cell_from_infos(cell[0].t,cell[0].id)
                        cell_updated.append(cell[0].id)

                else:
                    break
            if len(cell_updated) > 0:
                dataset.set_seg(t, data, cells_updated=cell_updated)

        self.restart()
         




