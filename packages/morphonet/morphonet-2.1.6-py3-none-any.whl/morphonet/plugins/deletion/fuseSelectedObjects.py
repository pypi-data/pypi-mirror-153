# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin

class FuseSelectedObjects(MorphoPlugin):
    """ This plugin fuse opbjects in the segmented image
   
    Parameters
    ----------
    Objects: 
        It can be apply either on selected objects or on colored objects where fusion will done by selection id
    """

    def __init__(self): #PLUGIN DEFINITION 
        MorphoPlugin.__init__(self) 
        self.set_name("Fuse")
        self.set_parent("Remove objects")

    def process(self,t,dataset,objects): #PLUGIN EXECUTION
        if not self.start(t,dataset,objects):
            return None
        import numpy as np

        for t in dataset.get_times(objects):
            tofuse={}
            for o in dataset.get_objects_at(objects,t):
                if o.s not in tofuse:
                    tofuse[o.s]=[]
                tofuse[o.s].append(o.id)
            data=dataset.get_seg(t)
            cells_updated=[]
            for s in tofuse:
                if len(tofuse[s])>1 : #More than one object to fuse..
                    minFuse=np.array(tofuse[s]).min()
                    cells_updated.append(minFuse)
                    self.print_mn(" --> fuse objects "+str(tofuse[s])+" at "+str(t) + " into object id="+str(minFuse))
                    for tof in tofuse[s]:
                        if tof!=minFuse:
                            dataset.backup()
                            cells_updated.append(tof)
                            data[np.where(data==tof)]=minFuse
                            cell = dataset.get_object(t, minFuse)
                            cell_to_fuse = dataset.get_object(t, tof)
                            for m in cell_to_fuse.mothers:
                                print("-----> add mother "+str(m.id) + " to "+str(cell.id))
                                dataset.add_mother(cell,m)
                                dataset.del_mother(cell_to_fuse,m)

                            for d in cell_to_fuse.daughters:
                                print("-----> add daughter " + str(d.id)+ " to "+str(cell.id))
                                dataset.add_daughter(cell,d)
                                dataset.del_daughter(cell_to_fuse,d)
                            dataset.remove_cell_from_infos(cell_to_fuse.t,cell_to_fuse.id)
                            #TODO retirer completemnet la cellule cell_to_fuse de toutes les properties (info)


            if len(cells_updated)>0:
                dataset.set_seg(t,data,cells_updated=cells_updated)
        self.restart()



