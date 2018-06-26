import logging

import numpy as np
import pandas as pd

from gdfplot.exceptions import ColumnNameNotFound
from gdfplot.exceptions import ColumnNameNotInIndex
from gdfplot.exceptions import WrongIndexWarning

log = logging.getLogger(__name__)


def list_metric_column_names(df, force_list=False):
	"""Returns a name or a list of names of column(s) with numerical data.

	:param <DataFrame> df: pandas dataframe table
	:param bool force_list: if True forces to return a list of names even
	if only one column name found."""

	metrics = df.select_dtypes(include=[np.int, np.float]).columns.values

	if not force_list and len(metrics) == 1:
		metrics = metrics[0]

	return metrics


def list_plottable_index_values(grouped_df, colname, stdev_colname='St.Dev'):
	"""Goes through all unique values in a specified column name of a grouped dataframe
	(ie. with MultiIndex), grabs the subset for each such value (via .xs() method)
	and then checks if the subset has plottable metric data columns,
	ignoring st.dev columns."""

	col_values = grouped_df.reset_index()[colname].unique()
	plottable_subsets = []

	if not isinstance(grouped_df.index, pd.MultiIndex):
		raise WrongIndexWarning('Cannot infer plottable columns for each row value of {} '
		                        'index column: dataframe must have a MultiIndex for that'
		                        '.'.format(colname))
	for colvalue in col_values:
		metric_cols = list(grouped_df.xs(colvalue, level=colname).columns)
		if not grouped_df.xs(colvalue, level=colname)\
				.dropna(subset=[nm for nm in metric_cols if nm != stdev_colname])\
				.empty:
			plottable_subsets.append(colvalue)

	return plottable_subsets


def calculate_ylim_range_from_df(df, scaling_factor=1.2):
	df2 = df[list_metric_column_names(df, force_list=True)]
	max_height = int(df2.max().max()) * scaling_factor
	return 0, max_height


def check_gdf_against_parameters(gdf, metrics=None, **params):
	index_columns = gdf.index.names
	metric_columns = gdf.columns
	non_empty_params = {k: v for k, v in params.items() if v}

	for k, v in non_empty_params.items():
		if v not in index_columns:
			raise ColumnNameNotInIndex(name=v, suffix=' ("{}" parameter).'.format(k))

	if metrics and metrics not in metric_columns:
		raise ColumnNameNotFound(name=metrics, suffix=' (metrics).')

	if len(non_empty_params) == len(index_columns) and 'hue' in non_empty_params:
		log.warning("Nr of index columns equals nr. of plot parameters - hue parameter "
		            "will be ignored to avoid confusing results")
