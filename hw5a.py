# region imports
import numpy as np
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
# endregion
'''
Utilized CHATGPT for coding logic
'''

# region functions
def ff(Re, rr, CBEQN=False):
    """
    This function calculates the friction factor for a pipe based on the
    notion of laminar, turbulent and transitional flow.
    :param Re: the Reynolds number under question.
    :param rr: the relative pipe roughness (expect between 0 and 0.05)
    :param CBEQN:  boolean to indicate if I should use Colebrook (True) or laminar equation
    :return: the (Darcy) friction factor
    """
    if (CBEQN):
        # note:  in numpy log is for natural log.  log10 is log base 10. Colebrook Equation
        ff = lambda f: 1 / f ** 0.5 + 2.0 * np.log10(rr / 3.7 + 2.51 / (Re * f ** 0.5))
        return fsolve(ff, 0.001)
    else:
        return 64 / Re
    pass

def plotMoody(plotPoint=False, pt=(0,0)):
    """
    This function produces the Moody diagram for a Re range from 1 to 10^8 and
    for relative roughness from 0 to 0.05 (20 steps).  The laminar region is described
    by the simple relationship of f=64/Re whereas the turbulent region is described by
    the Colebrook equation.
    :return: just shows the plot, nothing returned
    """
    #Step 1:  create logspace arrays for ranges of Re
    ReValsCB = np.logspace(np.log10(4000.0), 8, 100)
    ReValsL = np.logspace(np.log10(600.0), np.log10(2000.0), 20)
    ReValsTrans = np.logspace(np.log10(2000.0), np.log10(4000.0), 20)
    #Step 2:  create array for range of relative roughnesses
    rrVals=np.array([0,1E-6,5E-6,1E-5,5E-5,1E-4,2E-4,4E-4,6E-4,8E-4,1E-3,2E-3,4E-3,6E-3,8E-8,1.5E-2,2E-2,3E-2,4E-2,5E-2])

    #Step 2:  calculate the friction factor in the laminar range
    ffLam = np.array([ff(Re, 0.0) for Re in ReValsL])
    ffTrans = np.array([ff(Re, 0.0) for Re in ReValsTrans])

    #Step 3:  calculate friction factor values for each rr at each Re for turbulent range.
    ffCB = np.array([[ff(Re, rr, CBEQN=True) for Re in ReValsCB] for rr in rrVals])

    #Step 4:  construct the plot
    plt.loglog(ReValsL, ffLam[:], color="k")
    plt.loglog(ReValsTrans, ffTrans[:], linestyle='dashed', color="k")

    for nRelR in range(len(ffCB)):
        plt.loglog(ReValsCB, ffCB[nRelR], color='k', label=nRelR)
        plt.annotate(xy=(1E8, ffCB[nRelR][-1]), text=rrVals[nRelR])

    plt.xlim(600,1E8)
    plt.ylim(0.008, 0.10)
    plt.xlabel('Reynolds number ' r'$Re = \frac{Vd}{\nu}$', fontsize=16)
    plt.ylabel('Friction factor ' r'$f = \frac{h}{\left(\frac{L}{d}\cdot\frac{V^2}{2g}\right)}$', fontsize=16)
    plt.text(2.5E8, 0.02, 'Relative roughness ' r'$\frac{\epsilon}{d}$', rotation=90,
             fontsize=16)
    plt.title('Moody Chart', fontsize=16)
    ax = plt.gca()  # capture the current axes for use in modifying ticks, grids, etc.
    ax.tick_params(axis='both', which='both', direction='in', top=True, right=True, labelsize=12)  # format tick marks
    ax.tick_params(axis='both', grid_linewidth=1, grid_linestyle='solid', grid_alpha=0.5)
    ax.tick_params(axis='y', which='minor')
    ax.yaxis.set_minor_formatter(FormatStrFormatter("%.3f"))
    plt.grid(which='both')
    if(plotPoint):
        plt.plot(pt[0],pt[1],marker='o' if (pt[0]<=2000 or pt[0]>=4000) else '^', markersize=12, mec='r',mfc='none')

    plt.show()

def main():
    plotMoody()
# endregion

# region function calls
if __name__=="__main__":
    main()
# endregion