# -*- coding: latin-1 -*-
defaultPlugins=[]

from .Distance_On_Mask import Distance_On_Mask
defaultPlugins.append(Distance_On_Mask())

from .Minima_On_Mask import Minima_On_Mask
defaultPlugins.append(Minima_On_Mask())

from .Minima_On_Background import Minima_On_Background
defaultPlugins.append(Minima_On_Background())

from .Long_Axis import Long_Axis
defaultPlugins.append(Long_Axis())

from .On_Erode_Mask import On_Erode_Mask
defaultPlugins.append(On_Erode_Mask())