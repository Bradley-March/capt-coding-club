# %% Python preamble
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

# set up interactive plots for VS Code
mpl.use("TkAgg")
plt.ion()

# %% Using **kwargs

# create some (irrelevant) data
x = np.linspace(0, 10, 100)
data = np.random.rand(x.size)
y1 = data
y2 = data**2
y3 = data**(1/2)


# create a simple plot
fig, (ax1, ax2) = plt.subplots(2, figsize=(8, 6))
# plot the data with matplotlib defaults
ax1.plot(x, y1)
ax1.plot(x, y2)
ax1.plot(x, y3)

# defining kwargs for each plot
kwargs1 = {"color": "r", "linestyle": "-", "linewidth": 2,
           "label": r"$y \sim x$"}
kwargs2 = {"color": "g", "linestyle": "", "marker": "o", "markersize": 4,
           "label": r"$y \sim x^2$"}
kwargs3 = {"color": "b", "linestyle": "", "marker": "x", "markersize": 2,
           "label": r"$y \sim x^{1/2}$"}

# ploting each by unpacking kwargs
for y, kwargs in zip([y1, y2, y3], [kwargs1, kwargs2, kwargs3]):
    ax2.plot(x, y, **kwargs)
    # Note, we can add extra kwargs to the plot function that aren't in the dict
    # e.g. ax2.plot(x, y, **kwargs, alpha=0.5)

# add a legend
ax2.legend()
# make the figure layout tight
fig.tight_layout
