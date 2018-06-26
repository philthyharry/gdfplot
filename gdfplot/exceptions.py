
class WrongIndexWarning(Exception):
	def __init__(self, suffix='.'):
		msg = 'Dataframe with a wrong index type' + suffix
		super().__init__(msg)
		self.msg = msg

class ColumnNameNotFound(Exception):
	def __init__(self, name='column-name', suffix='.'):
		msg = 'Column name "{}" not present in the dataframe'.format(name) + suffix
		super().__init__(msg)
		self.msg = msg

class ColumnNameNotInIndex(Exception):
	def __init__(self, name='column-name', suffix='.'):
		msg = 'Column name "{}" not present in the dataframe index'.format(name) + suffix
		super().__init__(msg)
		self.msg = msg
