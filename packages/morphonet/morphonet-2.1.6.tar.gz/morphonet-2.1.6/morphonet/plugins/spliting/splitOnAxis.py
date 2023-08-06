# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin



class SplitOnAxis(MorphoPlugin):
    """ This plugin split objects in two on a given axis

    Parameters
    ----------
    Objects: 
        It can be apply either on selected or colored objects
    Axis : Dropdown
        It can be X,Y or Z axis

    """
    def __init__(self): #PLUGIN DEFINITION 
        MorphoPlugin.__init__(self) 
        self.set_name("Split On Axis")
        self.add_dropdown("Axis",["X","Y","Z"])
        self.set_parent("Split objects")

    def process(self,t,dataset,objects): #PLUGIN EXECUTION
        if not self.start(t,dataset,objects):
            return None

        import numpy as np
        which=self.get_dropdown("Axis")
        xyz=-1
        if which=="X":
            xyz=0
        elif which=="Y":
            xyz=1
        elif which=="Z":
            xyz=2
        if xyz==-1:
            self.print_mn('ERROR' + which+ " unknown ....")
        else:
            for t in dataset.get_times(objects):
                data = dataset.get_seg(t)
                cells_updated = []
                for o in dataset.get_objects_at(objects, t):
                    self.print_mn('     ----->>>  Split Object '+str(o.get_name())+ " in "+str(which))
                    coords=np.where(data==o.id)
                    xyzList=np.unique(coords[xyz])
                    xyzList.sort()
                    lastID=int(data.max())
                    lastID=lastID+1
                    w=np.where(coords[xyz]>int(xyzList.mean()))
                    new_coords=(coords[0][w],coords[1][w],coords[2][w])
                    data[new_coords]=lastID
                    self.print_mn('     ----->>>>>  Create a new ID '+str(lastID)+ " with "+str(len(new_coords[0]))+ " pixels")
                    cells_updated.append(o.id)
                    cells_updated.append(lastID)
                if len(cells_updated)>0:
                    dataset.set_seg(t,data,cells_updated=cells_updated)

        self.restart()
