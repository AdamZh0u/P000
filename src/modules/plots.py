"""scientific plt functions"""
import matplotlib as mpl

def setup_mpl(as_default=1):
    """My mpl setup""" 

    if as_default:
        mpl.rcdefaults()
    else:
        # FONT
        mpl.rcParams["font.size"] = 7 # 10 default
        mpl.rcParams['font.family']='sans-serif' # sans-serif
        mpl.rcParams['legend.fontsize'] = 'small' # medium

        # TICK 
        mpl.rcParams['xtick.labelsize'] = 'small' # medium
        mpl.rcParams['ytick.labelsize'] = 'small' # medium
        mpl.rcParams['xtick.major.width'] = 2/3. # 0.8
        mpl.rcParams['ytick.major.width'] = 2/3.
        mpl.rcParams['xtick.minor.width'] = 2/3. # 0.6
        mpl.rcParams['ytick.minor.width'] = 2/3.
        mpl.rcParams['xtick.major.size'] = 3 # 3.5
        mpl.rcParams['ytick.major.size'] = 3
        mpl.rcParams['xtick.minor.size'] = 1.5 # 2
        mpl.rcParams['ytick.minor.size'] = 1.5
        mpl.rcParams['xtick.major.pad']='2.3' # 3.5
        mpl.rcParams['ytick.major.pad']='2.3'
        mpl.rcParams['xtick.minor.pad']='2.3' # 3.5
        mpl.rcParams['ytick.minor.pad']='2.3'
        mpl.rcParams['ytick.direction'] = 'in' # out
        mpl.rcParams['xtick.direction'] = 'in'
        mpl.rcParams['xtick.top']=True
        mpl.rcParams['ytick.right']=True

        # 
        mpl.rcParams['axes.linewidth'] = 2/3. # 0.8
        mpl.rcParams['axes.labelpad']= 2 # 4
        mpl.rcParams['lines.linewidth'] = 1 # 1.5
        mpl.rcParams['mathtext.default']='regular'

        # EXPORT 
        mpl.rcParams['figure.dpi'] = 400 # 100
        mpl.rcParams['svg.fonttype'] = "none"
        mpl.rcParams['figure.autolayout'] = True # tight_layout

        # PARAMS
        alpha = 0.6
        to_rgba = mpl.colors.ColorConverter().to_rgba