import pandas as pd
import pytest

from gdfplot.core import plot_grouped_dataframe
from gdfplot.exceptions import ColumnNameNotInIndex
from tests.helpers import permuate_dictionary_keys


@pytest.fixture
def dataframe():
	from seaborn import load_dataset
	dots = load_dataset('dots')
	return dots.loc[(dots['time'] >= 0) & (dots['time'] <= 50)]


class TestSetupCheck:
	def test_sample_dataframe_has_right_format(self, dataframe):
		"""Checks if the test data frame has the right type"""
		assert isinstance(dataframe, pd.DataFrame)


param_names = ['h_subplots', 'v_subplots', 'hue']
columns = ['align', 'choice', 'coherence']
hue_ignored_warning = "hue parameter will be ignored"


class TestIndexColumnsMoreThanPlotParameters:
	"""Tests for situations where the number of index parameters (MultiIndex)
	is greater than the number of plot parameters used (hue, v_subplots, h_subplots).
	All plot parameter configurations should work without errors"""

	@pytest.mark.parametrize(
		'params', permuate_dictionary_keys(param_names, columns[:0]),
		ids=lambda d: " | ".join(["{}={}".format(k, v) for k, v in d.items()]) \
				if d else 'NO parameters')
	def test_one_column_index_(self, params, dataframe):
		gdf = dataframe[columns[:1] + ['firing_rate']].groupby(columns[:1]).sum()
		plot_grouped_dataframe(gdf, metrics='firing_rate', **params)

	@pytest.mark.parametrize(
		'params', permuate_dictionary_keys(param_names, columns[:1]),
		ids=lambda d: " | ".join(["{}={}".format(k, v) for k, v in d.items()]))
	def test_two_column_index_(self, params, dataframe):
		gdf = dataframe[columns[:2] + ['firing_rate']].groupby(columns[:2]).sum()
		plot_grouped_dataframe(gdf, metrics='firing_rate', **params)

	@pytest.mark.parametrize(
		'params', permuate_dictionary_keys(param_names, columns[:2]),
		ids=lambda d: " | ".join(["{}={}".format(k, v) for k, v in d.items()]))
	def test_three_column_index_(self, params, dataframe):
		gdf = dataframe[columns + ['firing_rate']].groupby(columns).sum()
		plot_grouped_dataframe(gdf, metrics='firing_rate', **params)


class TestIndexColumnsFewerThanPlotParameters:
	"""Tests for situations where the number of index parameters (MultiIndex)
	is smaller than the number of plot parameters used (hue, v_subplots, h_subplots).
	All plot parameter configurations should result in ColumnNameNotInIndex error."""

	@pytest.mark.parametrize(
		'params', permuate_dictionary_keys(param_names, columns[:2]),
		ids=lambda d: " | ".join(["{}={}".format(k, v) for k, v in d.items()]))
	def test_one_column_index(self, params, dataframe):
		gdf = dataframe[columns[:1] + ['firing_rate']].groupby(columns[:1]).sum()

		with pytest.raises(ColumnNameNotInIndex):
			plot_grouped_dataframe(gdf, metrics='firing_rate', **params)

	@pytest.mark.parametrize(
		'params', permuate_dictionary_keys(param_names, columns[:3]),
		ids=lambda d: " | ".join(["{}={}".format(k, v) for k, v in d.items()]))
	def test_two_column_index(self, params, dataframe):
		gdf = dataframe[columns[:2] + ['firing_rate']].groupby(columns[:2]).sum()

		with pytest.raises(ColumnNameNotInIndex):
			plot_grouped_dataframe(gdf, metrics='firing_rate', **params)


class TestIndexColumnsEqualsPlotParameters:
	"""Tests for situations where the number of index parameters (MultiIndex)
	is is equal to the number of plot parameters used (hue, v_subplots, h_subplots).
	All plot parameter configurations should work without errors, however some
	combinations can yield log warnings (when hue is ignored)."""

	@pytest.mark.parametrize(
		'params', permuate_dictionary_keys(param_names, columns[:1]),
		ids=lambda d: " | ".join(["{}={}".format(k, v) for k, v in d.items()]))
	def test_one_column_index(self, params, dataframe):
		gdf = dataframe[columns[:1] + ['firing_rate']].groupby(columns[:1]).sum()
		plot_grouped_dataframe(gdf, metrics='firing_rate', **params)

	@pytest.mark.parametrize(
		'params', permuate_dictionary_keys(param_names, columns[:2]),
		ids=lambda d: " | ".join(["{}={}".format(k, v) for k, v in d.items()]))
	def test_two_column_index(self, params, dataframe, caplog):
		gdf = dataframe[columns[:2] + ['firing_rate']].groupby(columns[:2]).sum()

		if 'hue' in params:
			plot_grouped_dataframe(gdf, metrics='firing_rate', **params)
			assert hue_ignored_warning in caplog.text
		else:
			plot_grouped_dataframe(gdf, metrics='firing_rate', **params)

	@pytest.mark.parametrize(
		'params', permuate_dictionary_keys(param_names, columns),
		ids=lambda d: " | ".join(["{}={}".format(k, v) for k, v in d.items()]))
	def test_three_column_index(self, params, dataframe, caplog):

		gdf = dataframe[columns + ['firing_rate']].groupby(columns).sum()
		plot_grouped_dataframe(gdf, metrics='firing_rate', **params)
		assert hue_ignored_warning in caplog.text
