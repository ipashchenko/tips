def fields_view(arr, fields):
    """
    How to return a view of several columns in numpy structured array?
    http://stackoverflow.com/questions/15182381/how-to-return-a-view-of-several-columns-in-numpy-structured-array
    Answered by http://stackoverflow.com/users/772649/hyry
    """
    dtype2 = np.dtype({name:arr.dtype.fields[name] for name in fields})
    return np.ndarray(arr.shape, dtype2, arr, 0, arr.strides)