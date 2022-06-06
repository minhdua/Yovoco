def remove_nulls(d):
    return {k: v for k, v in d.iteritems() if v is not None}