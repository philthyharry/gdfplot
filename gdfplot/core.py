import logging

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from gdfplot.helpers import calculate_ylim_range_from_df
from gdfplot.helpers import check_gdf_against_parameters
from gdfplot.helpers import list_plottable_index_values


STDEV_COLNAME = 'St.Dev'

log = logging.getLogger(__name__)


def plot_grouped_dataframe(gdf, metrics, h_subplots=None, v_subplots=None, hue=None, **kwargs):
	"""Creates a chart from a provided grouped data frame object. Allows to specify
	columns for splitting data into horizontal, vertical subplots (h_subplots and
	v_subplots respectively) and then further separate data into two colors (hue). Note,
	that the h_subplots, v_subplots and hue parameter values must refer to existing
	column names present in the grouped df index. Also note, that the three plot
	parameters will be ignored if the dataframe has no MultiIndex (i.e. must have be
	grouped by at least two categories/columns) and redirected to standard pd.plot()."""

	check_gdf_against_parameters(gdf, **dict(
		metrics=metrics, h_subplots=h_subplots,
		v_subplots=v_subplots, hue=hue))

	if not isinstance(gdf.index, pd.MultiIndex):
		log.warning('Dataframe lacks index type MultiIndex - '
		            'using standard pandas plot() instead.')
		return gdf[metrics].plot(**kwargs)

	plot_params = {
		'kind': 'bar',
		'fontsize': 12,
	}
	plot_params.update(kwargs)

	if v_subplots:
		figures = plot_loop_over_rows(gdf, metrics, v_subplots, h_subplots=h_subplots,
									  hue=hue, **plot_params)

	elif h_subplots:
		fig = plot_loop_over_cols(gdf, metrics, h_subplots=h_subplots, hue=hue, **plot_params)
		figures = [fig, ]

	else:
		fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(16, 4))
		plot_with_or_without_hue(gdf, metrics, hue=hue, ax=ax, **plot_params)
		figures = [fig, ]

	return figures


def plot_with_or_without_hue(df, metrics, hue, ax, title='', **plot_params):
	"""Plots a given dataframe to a specified axis; decides whether to split
	data according to hue if the hue column name given or not."""

	_ = plot_params.setdefault('ylim', calculate_ylim_range_from_df(df))

	if not title:
		title = metrics
	if hue and isinstance(df.index, pd.MultiIndex):
		plot_with_hue(df, ax=ax, metrics=metrics, title=title, hue=hue, **plot_params)
	else:
		plot_without_hue(df, ax=ax, metrics=metrics, title=title, **plot_params)
	plt.xlabel('')


def plot_with_hue(df, ax, metrics, hue, title='', **plot_params):
	"""Splits the dataframe according to hue column values and plots it to a given axis"""
	if STDEV_COLNAME in df.columns:
		plot_params['yerr'] = df.unstack(level=hue)[STDEV_COLNAME]
	df.unstack(level=hue)[metrics].plot(ax=ax, legend=True, title=title, **plot_params)


def plot_without_hue(df, ax, metrics, title='', **plot_params):
	"""Plots a given data frame to a given axis."""
	if STDEV_COLNAME in df.columns:
		plot_params['yerr'] = df[STDEV_COLNAME]
	df[metrics].plot(ax=ax, legend=False, title=title, **plot_params)


def plot_loop_over_cols(gdf, metrics, h_subplots, title_suffix='', hue=None, **plot_params):
	"""Creates a plot with splitting a data to separate column figures (horizontal)
	according to categorical data from a column name given via h_subplots.

	:param gdf: data frame with grouped metrics data
	:param metrics: name of the metrics being plot, must be equal to the metric column name!
	:param h_subplots: gdf column name used to split the figure into horizontal subfigures
	:param title_suffix: additional string to be appended to the subplots main title (note,
	that's not the same as each subplots titles...)
	:param hue: gdf column name used to split the data into color groups within each subplot
	:param plot_params: dictionary with additional plotting parameters to be passed to each
	subplot
	:return: pyplot figure object
	"""

	suptitle = '{}'.format(metrics)
	if title_suffix:
		suptitle += ' - {}'.format(title_suffix)

	if not h_subplots or not isinstance(gdf.index, pd.MultiIndex):
		fig, axeslist = plt.subplots(nrows=1, ncols=1, figsize=(16, 4))
		plot_with_or_without_hue(
			gdf, metrics, hue, ax=axeslist, title=suptitle, **plot_params)
		return fig

	plottable_values = list_plottable_index_values(
		gdf, h_subplots, stdev_colname=STDEV_COLNAME)

	fig, axeslist = plt.subplots(nrows=1, ncols=len(plottable_values), figsize=(16, 4))
	plt.suptitle(suptitle, fontsize=14)

	if not isinstance(axeslist, np.ndarray):
		axeslist = np.array([axeslist, ])

	for i, h_value in enumerate(plottable_values):
		plot_with_or_without_hue(
			gdf.xs(h_value, level=h_subplots), metrics=metrics, hue=hue,
			ax=axeslist[i], title=h_value, **plot_params)
		axeslist[i].set_xlabel("")
		plt.subplots_adjust(top=0.80)

	return fig


def plot_loop_over_rows(gdf, metrics, v_subplots, h_subplots=None, hue=None, **plot_params):
	"""For each unique value from a gdf v_subplots column it takes a subset of values and
	creates a new figure object. Figures are vertically distributed and each subset is also
	sent for splitting into horizontal subplots if h_subplots is given.

	:param pd.DataFrame gdf: data frame with grouped metrics data
	:param metrics: name of the metrics being plot, must be equal to the metric column name!
	:param str v_subplots: gdf column name used to split the data into individual figures
	distributed vertically.
	:param str h_subplots: gdf column name used to split the figure into horizontal
	subfigures
	:param str hue: gdf column name used to split the data into color groups within
	each subplot
	:param dict plot_params: dictionary with additional plotting parameters to be passed
	to each subplot
	:return: list of pyplot figure objects
	"""

	figures = []
	plottable_values = list_plottable_index_values(gdf, v_subplots,
	                                               stdev_colname=STDEV_COLNAME)
	for row_subplot_name in plottable_values:

		grouped_metric = gdf.xs(row_subplot_name, level=v_subplots)
		fig = plot_loop_over_cols(
			grouped_metric, metrics=metrics, hue=hue, h_subplots=h_subplots,
			title_suffix=row_subplot_name, **plot_params)
		figures.append(fig)

	return figures
