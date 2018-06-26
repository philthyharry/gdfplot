import itertools as itr


def two_states_permutator(values_list, repeats=None,
                          alt=None):  # todo: remove as not used
	"""Iterator creating all possible combinations of a list, where each value
	is permutated with two states: value or None. Eg. ['test', 'value'] for 2 repeats
	yields (test, value), (test, None), (None, value) and (None, None)"""
	if repeats and repeats > len(values_list):
		raise ValueError('Parameter repeats cannot exceed nr of values in values_list!')
	if not repeats:
		repeats = len(values_list)
	for combo in itr.product([True, False], repeat=repeats):
		yield [v if f else alt for v, f in zip(values_list, combo)]


def permulate_dict_values_two_states(keys, values, alt=None):  #todo: remove as not used
	"""Returns a list of dictionaries with various combinations of values assigned to
	the corresponding keys; each entry can take one of two values: its predefined value
	from the corresponding 'values' list or None. Eg. given keys=['a', 'b'] and
	values=['val1', 'val2'], the function will return
	[{'a': 'val1', 'b': 'val2'},
	 {'a': 'val1', 'b': None  },
	 {'a':  None,  'b': 'val2'},
	 {'a':  None,  'b': None  }]
	 """
	return [dict(zip(keys, combo)) for combo in two_states_permutator(values, alt=alt)]


def permuate_dictionary_keys(keys, values):
	"""Given a list of keys and values generates a list of dictionaries with all
	combinations of keys, used for the specified (fixed) number of values.
	Number of keys must be equal to or greater than the number of values to cycle
	through the possible combinations.
	eg. keys=['a', 'b', 'c'] and values = [1, 2] will generate:
	[{'a': 1, 'b': 2},
	 {'a': 1, 'c': 2},
	 {'b': 1, 'a': 2},
	 {'b': 1, 'c': 2},
	 {'c': 1, 'a': 2},
	 {'c': 1, 'b': 2}]
	"""
	n = len(values)
	if len(keys) < n:
		raise AttributeError('number of keys must be equal or greater '
		                     'than the number of values provided')
	result = []
	for k in itr.permutations(keys, n):
		result.append(dict(zip(k, values)))
	return result

