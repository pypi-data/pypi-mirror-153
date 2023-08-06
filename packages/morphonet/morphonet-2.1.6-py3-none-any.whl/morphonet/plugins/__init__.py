# -*- coding: latin-1 -*-
from .MorphoPlugin import MorphoPlugin
__all__ = [
    'MorphoPlugin'
]

#from functions import  get_borders

defaultPlugins=[]

from .Seeds import defaultPlugins as DP
defaultPlugins+=DP

from .Watershed import defaultPlugins as DP
defaultPlugins+=DP

from .deletion import defaultPlugins as DP
defaultPlugins+=DP

from .spliting import defaultPlugins as DP
defaultPlugins+=DP

from .temporal import defaultPlugins as DP
defaultPlugins+=DP
