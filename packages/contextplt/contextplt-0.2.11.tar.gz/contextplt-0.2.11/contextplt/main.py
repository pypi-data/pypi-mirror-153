from dataclasses import dataclass, field
from typing import Union, Optional, List, Dict, Tuple, Any, ClassVar
import copy

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.dates as mdates

@dataclass(repr=True)
class Single():
    """Create one figure. Adjust figure with arguments. 

    Args:
        figsize : Figure size.
        dpi : dpi.
        xlim : x limit.
        ylim : y limit.
        show : If False, plot is not displayed.
        xticklabels_show : If False, y tick labels are hidden.
        yticklabels_show : If False, y tick labels are hidden.
        xtick_show : If False, tick labels and ticks are hidden.
        ytick_show : If False, tick labels and ticks are hidden.
        hide_spines : Hide outlines of axes. Takes "right","top","bottom","left" or these list.
            Also takes "all" to hide outlines and ticks of plot.

    Examples: 
        Basic usage. 

        >>> import contextplt as cplt
        >>> x = [1,2,3]
        >>> y = [1,2,3]
        >>> with cplt.Single() as p:
        >>>     p.ax.plot(x,y)

        With parameter version.

        >>> with cplt.Single(xlim=[0,5], ylim=[0,5], xlabel="xlabel", ylabel="ylabel",
        ...         title="title", figsize=(6,6), dpi=150) as p:
        >>>     p.ax.plot(x,y)

        Can use variadic keyword arguments to share the same keyword arguments. 

        >>> kargs = dict(xlim=[0,5], ylim=[0,5], xlabel="xlabel", ylabel="ylabel",
        ...         title="title", figsize=(6,6), dpi=150)
        >>> with cplt.Single(**kargs) as p:
        >>>     p.ax.plot(x,y)
    """
    figsize : Tuple[float, float] =(5,3)
    dpi : int =150
    xlim : Optional[List[float]] = None
    ylim : Optional[List[float]] = None 
    xlabel : Optional[str] = None 
    ylabel : Optional[str] = None
    xlabelfontsize : Optional[float] = None
    ylabelfontsize : Optional[float] = None
    xtickfontsize : Optional[float] = None
    ytickfontsize : Optional[float] = None
    title : Optional[str] =None
    titlefontsize : Optional[float] = None
    tight : bool =True
    xrotation : Optional[int] = None
    yrotation : Optional[int] = None 
    xscale : Optional[str] = None
    yscale : Optional[str] = None
    show : bool = True
    xticklabels_show : bool = True
    yticklabels_show : bool = True
    xticks_show : bool = True
    yticks_show : bool = True
    hide_spines : Optional[Union[List[str]]] = None
    save_path : Optional[str] = None
    savefig_kargs : dict = field(default_factory=dict)

    def __post_init__(self): 
        """Set various parameters. 

        Attributes:
            ax : axis. 
            save_path (str) : path to save.
            title (str) : title.
            tight (bool) : tight_layout or not.
        """
        self.fig = plt.figure(figsize=self.figsize,dpi=self.dpi)
        self.ax = self.fig.add_subplot(111)


    def __enter__(self):
        return(self)

    def __exit__(self,exc_type, exc_value, exc_traceback):
        self.option()

        self.ax.set_xlim(self.xlim) if self.xlim else None
        self.ax.set_ylim(self.ylim) if self.ylim else None
        self.ax.set_xlabel(self.xlabel, fontsize=self.xlabelfontsize) if self.xlabel else None
        self.ax.set_ylabel(self.ylabel, fontsize=self.ylabelfontsize) if self.ylabel else None
        if self.xscale is not None:
            self.ax.set_xscale(self.xscale)
        if self.yscale is not None:
            self.ax.set_yscale(self.yscale)
        self.ax.tick_params(axis='x', which='major', labelsize=self.xtickfontsize, 
                            rotation=self.xrotation)
        self.ax.tick_params(axis='y', which='major', labelsize=self.ytickfontsize,
                            rotation=self.yrotation)
        if not self.xticks_show:
            self.ax.set_xticks([])
        if not self.yticks_show:
            self.ax.set_yticks([])
        if not self.xticklabels_show:
            self.ax.set_xticklabels([])
        if not self.yticklabels_show:
            self.ax.set_yticklabels([])
        if self.hide_spines:
            if self.hide_spines == "all":
                self.ax.set_axis_off()
            else:
                self.ax.spines[self.hide_spines].set_visible(False)
        plt.title(self.title, fontsize=self.titlefontsize)
        plt.tight_layout() if self.tight else None
        if self.save_path:
            plt.savefig(self.save_path, **self.savefig_kargs)
        if self.show:
            plt.show()
        else:
            plt.close()

    def option(self):
        '''This method is for additional graphic setting. 
        See DatePlot for example.'''
        pass

class Date(Single):
    def __init__(self,rotation=90,x_fontsize=10,**kargs):
        super().__init__(**kargs)
        self.rotation = rotation
        self.x_fontsize = x_fontsize

    def option(self):
        self.ax.xaxis.set_major_locator(mdates.DayLocator(bymonthday=None, interval=1, tz=None))
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        plt.xticks(rotation=self.rotation,fontsize=self.x_fontsize)

@dataclass(repr=True)
class Multiple():
    """Create multiple figures in one picture with arguments. 

    Args:
        mosaic : Support of matplotlib.pyplot.subplot_mosaic. After specifying this mosaic parameter,
            access each ax by passing a character in mosaic.
        sharex : for mosaic plot.
        sharey : for mosaic plot.

    Examples:
        Basic usage. 
        
        >>> import numpy as np
        >>> import contextplt as cplt
        >>> x1, x2, y1, y2= np.random.rand(4, 100)
        >>> with cplt.Multiple(grid=(2,1),figsize=(5,4), dpi=150) as mul:
        >>>     with mul.Single(index=1) as p:
        >>>         p.ax.scatter(x1,y1)
        >>>     with mul.Single(index=2) as p:
        >>>         p.ax.scatter(x2,y2)

        Various options. Label_outer only leaves the outside of ticks and labels. 

        >>> with cplt.Multiple(grid=(2,2),figsize=(6,4), dpi=150,
        ...         suptitle="super title", label_outer=True) as mul:
        >>>     for i in range(4):
        >>>         with mul.Single(index=i+1,xlabel=f"xlabel{i+1}", ylabel=f"ylabel{i+1}") as p:
        >>>             x, y = np.random.rand(2,100)
        >>>             p.ax.plot(x,y)
    """
    figsize : Tuple[float, float] =(5,3)
    dpi : int =150
    grid : Tuple[int,int] = (2,2)
    suptitle : Optional[str] = None
    show : bool = True
    tight : bool = False
    label_outer : bool = False
    save_path : Optional[str] = None
    savefig_kargs : dict = field(default_factory=dict)
    mosaic : Optional[List] = None
    constrained_layout : Optional[bool] = None
    sharex : bool = False
    sharey : bool = False

    def __post_init__(self):
        if self.mosaic is not None:
            self.constrained_layout = True if self.constrained_layout is None else self.constrained_layout
        self.fig = plt.figure(figsize=self.figsize, dpi=self.dpi, 
                              constrained_layout=self.constrained_layout)
        if self.mosaic is not None:
            self.ax_dict = self.fig.subplot_mosaic(self.mosaic, sharex=self.sharex, sharey=self.sharey)
        plt.suptitle(self.suptitle)

        # Note: class variable is used for accessing this Multiple class instance
        #   from a MulSingle object. MulSingle.mul is set to be None 
        #   when exit from the context.
        self.Single = MulSingle
        self.Single.mul = self

    def set_ax(self,index,xlim=None, ylim=None, 
               xlabel="", ylabel="",title="", rotation : int = 0):
        """Return axis object. 

        Args: 
            index (int) : index of which axes object is pointed at. 

        Note:
            Currently this method is not maintained, and intended to use
            self.mul attribute to create another figure.
        """
        print("Future deplicate notice: Use mul.Single attribute.")
        ax = self.fig.add_subplot(*self.grid,index)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_xlim(xlim) if xlim else None
        ax.set_ylim(ylim) if ylim else None
        ax.set_title(title)
        plt.xticks(rotation=rotation)
        return(ax)

    def __enter__(self):
        return(self)

    def __exit__(self,exc_type, exc_value, exc_traceback):
        self.option()
        if self.label_outer:
            for ax in self.fig.get_axes():
                ax.label_outer()
        plt.tight_layout() if self.tight else None
        plt.savefig(self.save_path, **self.savefig_kargs) if self.save_path else None

        if self.show:
            plt.show()
        else:
            plt.close()

        self.Single.mul = None

    def option(self):
        """This method is for additional graphic setting. 
        See DatePlot for example."""
        pass

@dataclass(repr=True)
class MulSingle():
    """

    Args:
        hide_spines : Hide outlines of axes. Takes "right","top","bottom","left" or these list.
            Also takes "all" to hide outlines and ticks of plot.
    """
    index : int 
    mul : ClassVar[Multiple] 
    sharex : Optional[plt.Axes] = None
    sharey : Optional[plt.Axes] = None
    xlim : Optional[List[float]] = None
    ylim : Optional[List[float]] = None 
    xlabel : Optional[str] = None 
    ylabel : Optional[str] = None
    xlabelfontsize : Optional[float] = None
    ylabelfontsize : Optional[float] = None
    xtickfontsize : Optional[float] = None
    ytickfontsize : Optional[float] = None
    title : Optional[str] =None
    titlefontsize : Optional[float] = None
    tight : bool =True
    xrotation : Optional[int] = None
    yrotation : Optional[int] = None 
    xscale : Optional[str] = None
    yscale : Optional[str] = None
    xticklabels_show : bool = True
    yticklabels_show : bool = True
    hide_spines : Optional[Union[List[str]]] = None
    xticks_show : bool = True
    yticks_show : bool = True

    def __post_init__(self):
        if self.mul.mosaic is None:
            self.ax = self.mul.fig.add_subplot(
                *self.mul.grid, 
                self.index, 
                sharex=self.sharex,
                sharey=self.sharey,
            )
        else:
            self.ax = self.mul.ax_dict[self.index]
            if self.sharex is not None: 
                self.ax.get_shared_x_axes().join(self.ax, self.sharex)
            if self.sharey is not None:
                self.ax.get_shared_y_axes().join(self.ax, self.sharey)

    def __enter__(self):
        return(self)
    
    def __exit__(self,exc_type, exc_value, exc_traceback):
        self.ax.set_xlim(self.xlim) if self.xlim else None
        self.ax.set_ylim(self.ylim) if self.ylim else None
        self.ax.set_xlabel(self.xlabel, fontsize=self.xlabelfontsize) if self.xlabel else None
        self.ax.set_ylabel(self.ylabel, fontsize=self.ylabelfontsize) if self.ylabel else None
        if self.xscale is not None:
            self.ax.set_xscale(self.xscale)
        if self.yscale is not None:
            self.ax.set_yscale(self.yscale)
        self.ax.tick_params(axis='x', which='major', labelsize=self.xtickfontsize, 
                            rotation=self.xrotation)
        self.ax.tick_params(axis='y', which='major', labelsize=self.ytickfontsize,
                            rotation=self.yrotation)
        if not self.xticks_show:
            self.ax.set_xticks([])
        if not self.yticks_show:
            self.ax.set_yticks([])
        if not self.xticklabels_show:
            self.ax.set_xticklabels([])
        if not self.yticklabels_show:
            self.ax.set_yticklabels([])
        if self.hide_spines:
            if self.hide_spines == "all":
                self.ax.set_axis_off()
            else:
                self.ax.spines[self.hide_spines].set_visible(False)
        plt.title(self.title, fontsize=self.titlefontsize)

