# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin

class DeleteSelectedObjects(MorphoPlugin):
    """ This plugin completly delete the opbjects from the segmented image
   
    Parameters
    ----------
    Objects: 
        It can be apply either on selected or colored objects
    """

    def __init__(self): #PLUGIN DEFINITION 
        MorphoPlugin.__init__(self) 
        self.set_name("Delete")
        self.set_parent("Remove objects")

    def process(self,t,dataset,objects): #PLUGIN EXECUTION
        if not self.start(t,dataset,objects):
            return None
        import numpy as np
        for t in dataset.get_times(objects):
            data = dataset.get_seg(t)
            cells_updated =[]
            for o in dataset.get_objects_at(objects, t):
                self.print_mn(" --> delete object "+str(o.id)+" at "+str(o.t))
                for m in o.mothers:
                    dataset.del_mother(o,m)
                for d in o.daughters:
                    dataset.del_daughter(o,d)
                dataset.remove_cell_from_infos(o.t,o.id)
                data[np.where(data==o.id)]=dataset.background
                cells_updated.append(o.id)
            if len(cells_updated)>0:
                dataset.set_seg(t,data,cells_updated=[0])
        self.restart()





