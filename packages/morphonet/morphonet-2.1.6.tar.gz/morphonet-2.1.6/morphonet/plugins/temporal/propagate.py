# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin


class Propagate(MorphoPlugin):
    """This plugin propagate a name trough the full cell life

    Parameters
    ----------
    Objects: 
        It can be apply either on selected objects or on colored objects where temporal link will done by selection id

    """

    def __init__(self): #PLUGIN DEFINITION 
        MorphoPlugin.__init__(self) 
        self.set_name("Propagate")
        self.add_inputfield("Info",default="cell_name")
        self.set_parent("Temporal Relation")

    def process(self,t,dataset,objects): #PLUGIN EXECUTION
        if not self.start(t,dataset,objects): 
            return None

        info_name = self.get_inputfield("Info")
        if info_name=="":
            print(" Please fill the info name to propagate")
        else:
            info=dataset.get_info(info_name,create=False)
            if info is None:
                print(" The info named : "+info_name+" is unkown ... ")
            else:
                nb_propagated=0
                if len(objects)>0:
                    dataset.backup()
                for cid in objects:
                    o=dataset.get_object(cid)
                    if o is not None:
                        annotation=info.get(o)
                        if annotation is None:
                            print(" --> no corresponding annotation ")
                        else:
                            print(" --> found Annotation "+annotation)
                            while o.nb_daughters()==1: #Simple propagation method
                                #print(" Cell "+str(o.id)+" at "+str(o.t)+ " is annotated "+str(info.get(o)))
                                if info.get(o)!=annotation:
                                    info.set(o,annotation)
                                    nb_propagated+=1
                                o=o.daughters[0]
                            if info.get(o) != annotation: #The last one
                                info.set(o, annotation)
                                nb_propagated += 1
                print(" --> "+str(nb_propagated)+" info where propagated")
        self.restart() 
