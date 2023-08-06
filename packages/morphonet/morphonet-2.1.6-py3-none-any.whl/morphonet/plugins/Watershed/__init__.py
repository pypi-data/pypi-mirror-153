# -*- coding: latin-1 -*-
defaultPlugins=[]

from .on_raw import On_Raw
defaultPlugins.append(On_Raw())

from .on_background import On_Background
defaultPlugins.append(On_Background())

from .with_mask_on_raw import With_Mask_On_Raw
defaultPlugins.append(With_Mask_On_Raw())

from .with_mask_on_shape import With_Mask_On_Shape
defaultPlugins.append(With_Mask_On_Shape())

