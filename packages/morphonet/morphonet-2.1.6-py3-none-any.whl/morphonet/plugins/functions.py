import numpy as np

def _centerInShape(c, s):
    if c[0] < 0 or c[1] < 0 or c[2] < 0 or c[0] >= s[0] or c[1] >= s[1] or c[2] >= s[2]:
        return False
    return True



def get_borders(data,cellCoords,border=4):
    xmin=max(0,cellCoords[0].min()-border)
    xmax=min(data.shape[0],cellCoords[0].max()+border)
    ymin=max(0,cellCoords[1].min()-border)
    ymax=min(data.shape[1],cellCoords[1].max()+border)
    zmin=max(0,cellCoords[2].min()-border)
    zmax=min(data.shape[2],cellCoords[2].max()+border)
    return xmin,xmax,ymin,ymax,zmin,zmax


def apply_new_label(data,xmin,ymin,zmin,labelw,minVol=0):
    import numpy as np
    labels=np.unique(labelw)
    labels=labels[labels!=0] #Remove Background
    if len(labels)==1:
        print(" ---> no new labels ")
        return data,[]
    #First We check of all coords have the required minimum of size
    #The biggest cell get the same label
    Labelsize={}
    Bigest=0
    BigestL=-1
    for l in labels:
        Labelsize[l]=len(np.where(labelw==l)[0])
        if Labelsize[l]>Bigest:
            Bigest=Labelsize[l]
            BigestL=l

    labels=labels[labels!=BigestL]
    newIds=[]
    lastID=int(data.max())+1
    for l in labels:
        new_coords=np.where(labelw==l)
        if len(new_coords[0])>=minVol:
            data[new_coords[0]+xmin,new_coords[1]+ymin,new_coords[2]+zmin]=lastID
            print('     ----->>>>>  Create a new object '+str(lastID)+ " with "+str(len(new_coords[0]))+ " voxels")
            newIds.append(lastID)
            lastID += 1
        else:
            print("     ----->>>>>  Do not create with "+str(len(new_coords[0]))+ " voxels")
    return data,newIds


def get_seeds_in_image(dataset,seeds):
    center = dataset.get_center()
    seeds=[np.int32(s + center) for s in seeds]
    return seeds

def get_barycenter(data,cell_id):
    coords = np.where(data == cell_id)
    return np.uint16([coords[0].mean(),coords[1].mean(),coords[2].mean()])

def get_seed_at(seeds,xmin,ymin,zmin):
    nseeds=[]
    for seed in seeds:
        nseed = [seed[0] - xmin, seed[1] - ymin, seed[2] - zmin]
        nseeds.append(nseed)
    return nseeds

def get_seeds_in_mask(seeds,mask):
    seeds_in_cell_mask=[]
    for seed in seeds:
        if seed[0] >= 0 and seed[1] >= 0 and seed[2] >= 0 and seed[0] < mask.shape[0] and seed[1] < mask.shape[1] and \
                seed[2] < mask.shape[2]:
            if mask[seed[0], seed[1], seed[2]]:
                seeds_in_cell_mask.append(seed)
    return seeds_in_cell_mask


#Local Redefinition of some tools
def watershed(data,markers=None,mask=None):
    from skimage.segmentation import watershed as sk_watershed
    return  sk_watershed(data, markers=markers, mask=mask)

def gaussian(data, sigma=2, preserve_range=False):
    from skimage.filters import gaussian as sk_gaussian
    return sk_gaussian(data,sigma=sigma,preserve_range=preserve_range)
