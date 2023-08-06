# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin

class DelTemporalLink(MorphoPlugin):
    """This plugin delete any temporal links between objects

    Parameters
    ----------
    Objects: 
        It can be apply either on selected or colored objects
    """
    def __init__(self): #PLUGIN DEFINITION 
        MorphoPlugin.__init__(self) 
        self.set_name("Delete Links")
        self.set_parent("Temporal Relation")

    def process(self,t,dataset,objects): #PLUGIN EXECUTION
        if not self.start(t,dataset,objects):
            return None
        if len(objects)>0:
            dataset.backup()
        for cid in objects:
            o=dataset.get_object(cid)
            if o is not None:
                for m in o.mothers:
                    dataset.del_mother(o,m)
                for d in o.daughters:
                    dataset.del_daughter(o,d)
                self.print_mn(" ----> remove link for object "+str(o.id)+" at "+str(o.t))
        self.restart()
