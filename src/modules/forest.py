"""This module is a forest class to simulate fire process"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib import colors

# state 为可更新对象，也可以改写成一个列表记录所有状态

class Forest:
    """
    forest to conduct fire percolation
    """
    # class attribute
    EMPTY, TREE, FIRE = 0, 1, 2
    neighbourhood_8 = ((-1, -1), (-1, 0), (-1, 1), (0, -1),
                       (0, 1), (1, -1), (1, 0), (1, 1))
    neighbourhood_4 = ((-1, 0), (0, -1), (0, 1), (1, 0))

    def __init__(self, n_x=100, n_y=100):
        """instance attri
        n_x,n_y: Forest size (number of cells in x and y directions).
        """
        self.n_x = n_x
        self.n_y = n_y
        self.initstate = np.zeros((n_y, n_x))
        self.state = np.zeros((n_y, n_x))  # set zero

    def init_trees(self, tree_fraction=0.3, rnd_seed=None):
        '''
        forest_fraction: The initial fraction of the forest occupied by trees.
        '''
        np.random.seed(rnd_seed)
        self.initstate[1:self.n_y-1, 1:self.n_x -
                       1] = np.random.randint(0, 2, size=(self.n_y-2, self.n_x-2))
        self.initstate[1:self.n_y-1, 1:self.n_x -
                       1] = np.random.random(size=(self.n_y-2, self.n_x-2)) < tree_fraction

    def ignite(self, rnd_seed=None):
        """get random point to ignite fire

        rnd_seed: random seed
        """
        np.random.seed(rnd_seed)
        idx_trees = np.where(self.initstate == Forest.TREE)
        idx = np.random.choice(range(len(idx_trees[0])))
        self.initstate[idx_trees[0][idx], idx_trees[1][idx]] = Forest.FIRE
        self.state = self.initstate.copy()

    def get_tofire(self, neighbor=neighbourhood_8):
        """get set of trees that will be in fire in the next stage

        Args:
            neighbor (set, optional): neighborgood type. Defaults to neighbourhood_8.

        Returns:
            set: coors of trees
        """
        idxs_y, idxs_x = np.where(self.state == Forest.FIRE)
        assert len(idxs_x) == len(idxs_y)
        tofire = []
        for y, x in zip(idxs_y, idxs_x):
            for d_x, d_y in neighbor:
                xx = x+d_x
                yy = y+d_y
                if self.state[yy, xx] == Forest.TREE:
                    tofire.append((yy, xx))
        return set(tofire)

    def iterate_perco(self, tofire):
        """iterate one step"""
        for y, x in tofire:
            self.state[y, x] = Forest.FIRE

## plot parameters and functions ========================================

colors_list = [(0.2, 0, 0), (0, 0.5, 0), (1, 0, 0), 'orange']
cmap = colors.ListedColormap(colors_list)
bounds = [0, 1, 2, 3]
norm = colors.BoundaryNorm(bounds, cmap.N)

def plot_state(state,ax,title="state"):
    """plot state of a forest"""
    ax.set_axis_off()
    ax.set_title(title)
    ax.imshow(state, cmap=cmap, norm=norm)
    return ax

def animate(f, steps=100,neighbor=Forest.neighbourhood_4):
    """animate fire process"""
    fig, ax = plt.subplots(figsize=(25/3, 6.25), dpi=200)
    ax.set_axis_off()
    im = ax.imshow(np.zeros([100, 100]), cmap=cmap, norm=norm)
    ax.set_title('')
    plt.close()  # close plot

    def update(i):
        if i != 0:
            im.set_data(f.state)
            f.iterate_perco(f.get_tofire(neighbor=neighbor))
        ax.set_title(f'step={i}')

    f.state = f.initstate.copy()  # 重置state一下
    animm = animation.FuncAnimation(
        fig, update, interval=200, frames=steps+1,repeat_delay=400)
    return animm

if __name__ == "__main__":
    # Fixing random state for reproducibility

    f = Forest(n_x=100, n_y=100)
    f.init_trees(tree_fraction=0.4,rnd_seed= 33)
    f.ignite(rnd_seed=43)

    STEP = 1
    ls_tofire = f.get_tofire()
    while len(ls_tofire) > 0:
        f.iterate_perco(ls_tofire)
        ls_tofire = f.get_tofire()
        # print(STEP, ls_tofire)
        STEP += 1

    ## plot initstate and end state
    fig,ax = plt.suplots(1,2,figsize=(12, 6.25), dpi=200)
    plot_state(f.initstate, ax[0], title="Begin")
    plot_state(f.state, ax[1], title="End")
    plt.close()

    ## animate 
    anim = animate(f, steps=STEP)
    with open("forest_fire.html", "w", encoding="utf-8") as x:
        print(anim.to_jshtml(), file=x)
