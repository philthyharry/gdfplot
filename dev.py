import matplotlib.pyplot as plt
import seaborn as sns

from gdfplot.core import plot_grouped_dataframe


dots = sns.load_dataset('dots')
dots = dots.loc[(dots['time'] >= 0) & (dots['time'] <= 50)]

g2 = dots[['align', 'choice', 'firing_rate']].groupby(['align', 'choice']).sum()

plot_grouped_dataframe(g2, metrics='firing_rate', hue='align', h_subplots='choice')
plt.show()
