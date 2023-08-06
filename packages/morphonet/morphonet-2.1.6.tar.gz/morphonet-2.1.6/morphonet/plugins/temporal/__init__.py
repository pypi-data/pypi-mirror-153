# -*- coding: latin-1 -*-
defaultPlugins=[]

from .addTemporalLink import AddTemporalLink
defaultPlugins.append(AddTemporalLink())

from .delTemporalLink import DelTemporalLink
defaultPlugins.append(DelTemporalLink())


from .propagate import Propagate
defaultPlugins.append(Propagate())