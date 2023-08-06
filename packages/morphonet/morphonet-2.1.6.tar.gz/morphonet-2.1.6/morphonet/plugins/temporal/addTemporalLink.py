# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin


class AddTemporalLink(MorphoPlugin):
    """This plugin create a temporal link between objects

    Parameters
    ----------
    Objects: 
        It can be apply either on selected objects or on colored objects where temporal link will done by selection id

    """

    def __init__(self): #PLUGIN DEFINITION 
        MorphoPlugin.__init__(self) 
        self.set_name("Create Links")
        self.set_parent("Temporal Relation")

    def process(self,t,dataset,objects): #PLUGIN EXECUTION
        if not self.start(t,dataset,objects): 
            return None

        #List Objects by selections
        selections={}
        for cid in objects:
            o=dataset.get_object(cid)
            if o is not None:
                if o.s not in selections:
                    selections[o.s]=[]
                selections[o.s].append(o)
        if len(selections)>1:
            self.print_mn(" --> Found  "+str(len(selections))+ " selections ")
            dataset.backup()
        for s in selections:
            #Order objects by time
            times={}  #List all times
            for o in selections[s]:
                if o.t not in times:
                    times[o.t]=[]
                times[o.t].append(o)
            
            for t in sorted(times):
                if t+1 in times:
                    cellT=times[t]
                    cellTP=times[t+1]
                    for daughter in cellTP:
                        for mother in cellT:
                            dataset.add_mother(daughter,mother)
                            #dataset.add_link(daughter,mother)
                            self.print_mn(" ----> Link object "+str(daughter.id)+" at "+str(daughter.t)+" with "+str(mother.id)+ " at "+str(mother.t))

        self.restart()
