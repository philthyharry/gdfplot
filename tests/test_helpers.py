import pytest

from gdfplot.helpers import list_metric_column_names
from gdfplot.helpers import list_plottable_index_values
from gdfplot.helpers import calculate_ylim_range_from_df
from gdfplot.helpers import check_gdf_against_parameters


@pytest.fixture
def dataframe():
	from seaborn import load_dataset
	dots = load_dataset('dots')
	return dots.loc[(dots['time'] >= 0) & (dots['time'] <= 50)]


def test_list_metric_column_names_with_df(dataframe):
	"""Checks if the function returns all the numerical column names from a dataframe."""

	m = list_metric_column_names(dataframe)
	assert set(m) == {'time', 'coherence', 'firing_rate'}


@pytest.mark.parametrize('mcol', ['time', 'coherence', 'firing_rate'])
def test_list_metric_column_names_with_gdf(dataframe, mcol):
	"""Checks if the function returns all the numerical column names, except those
	that are part of the index column."""

	metric_cols = ['time', 'coherence', 'firing_rate']
	metric_cols.remove(mcol)
	g = list_metric_column_names(dataframe.groupby(mcol).sum())
	assert set(g) == set(metric_cols)

# todo: test list_plottable_index_values function
# todo: test calculate_ylim_range_from_df function
# todo: test check_gdf_against_parameters function
