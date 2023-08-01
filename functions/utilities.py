import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
import seaborn as sns
import umap.umap_ as umap

def get_umap(dataBlock):
    embedding=umap.UMAP(n_neighbors=8,min_dist=0.3,metric='euclidean', 
                   random_state=34).fit_transform(dataBlock)
    
    plt.figure(figsize=(11,8))
    sns_plot=''
    sns_plot=sns.scatterplot(x=embedding[:,0],y=embedding[:,1],
                   legend="full",
                   palette="tab10",
                   s=20)
    return(embedding, sns_plot)

def get_ranges(df, col, num_cat=4):
    PCmax=df[col].max()
    PCmin=df[col].min()
    PCrng = np.linspace(PCmin,PCmax,num_cat+1)
    categ=list()
    for v in df[col].to_list():
        for i,r in enumerate(PCrng[1:]):
            if v<r:
                col=i+1
                break
            else:
                continue
        categ.append(col)
    if 'Categ' in df:
        df['Categ']=categ
    else:        
        df.insert(0,'Categ',categ)
    return(df)

def get_ranges2(df, col):
    PCmax=df[col].max()
    PCmin=df[col].min()
    crit_val=df[col].quantile([0.90]).values
    categ=list()
    for v in df[col].to_list():
        if v<crit_val:
            categ.append("Low")
        else:
            categ.append("High")
    if 'Categ' in df:
        df['Categ']=categ
    else:        
        df.insert(0,'Categ',categ)
    return(df)

def adjust_box_widths(g, fac):
    """
    Adjust the withs of a seaborn-generated boxplot.
    """

    # iterating through Axes instances
    for ax in g.axes:

        # iterating through axes artists:
        for c in ax.get_children():

            # searching for PathPatches
            if isinstance(c, PathPatch):
                # getting current width of box:
                p = c.get_path()
                verts = p.vertices
                verts_sub = verts[:-1]
                xmin = np.min(verts_sub[:, 0])
                xmax = np.max(verts_sub[:, 0])
                xmid = 0.5*(xmin+xmax)
                xhalf = 0.5*(xmax - xmin)

                # setting new width of box
                xmin_new = xmid-fac*xhalf
                xmax_new = xmid+fac*xhalf
                verts_sub[verts_sub[:, 0] == xmin, 0] = xmin_new
                verts_sub[verts_sub[:, 0] == xmax, 0] = xmax_new

                # setting new width of median line
                for l in ax.lines:
                    if np.all(l.get_xdata() == [xmin, xmax]):
                        l.set_xdata([xmin_new, xmax_new])