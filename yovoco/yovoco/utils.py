from datetime import date

def now_to_string():
	return date.today().strftime('%Y%m%d')

def get_not_null_or_default(value, default):
	if value is None:
		return default
	return value