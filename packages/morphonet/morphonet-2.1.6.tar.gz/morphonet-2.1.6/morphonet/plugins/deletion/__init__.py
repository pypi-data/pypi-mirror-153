from .deleteSelectedObjects import *
from .fuseSelectedObjects import *
from .removeUnder import *


# -*- coding: latin-1 -*-
defaultPlugins=[]

from .fuseSelectedObjects import FuseSelectedObjects
defaultPlugins.append(FuseSelectedObjects())

from .deleteSelectedObjects import DeleteSelectedObjects
defaultPlugins.append(DeleteSelectedObjects())

from .removeUnder import RemoveUnder
defaultPlugins.append(RemoveUnder())
