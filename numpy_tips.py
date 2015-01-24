def fields_view(arr, fields):
    """
    How to return a view of several columns in numpy structured array?
    http://stackoverflow.com/questions/15182381/how-to-return-a-view-of-several-columns-in-numpy-structured-array
    Answered by http://stackoverflow.com/users/772649/hyry
    
    :param arr:
        Numpy structured array.
    :param fields:
        Iterable of fileds for view to return.
    :return:
        View to original array with only fields listed in ``fields``.
    """
    dtype2 = np.dtype({name:arr.dtype.fields[name] for name in fields})
    return np.ndarray(arr.shape, dtype2, arr, 0, arr.strides)


def add_field(a, descr):
    """
    Return a new array that is like "a", but has additional fields.
    http://stackoverflow.com/questions/1201817/adding-a-field-to-a-structured-numpy-array
    Answered by http://stackoverflow.com/users/17498/vebjorn-ljosa

    :param a:
        Structured numpy array
    :param descr:
        Numpy type description of the new fields
    :return:
        Copy of the original array with new fields.

    :notes:
        The contents of "a" are copied over to the appropriate fields in
        the new array, whereas the new fields are uninitialized.  The
        arguments are not modified.
        There's numpy.lib.recfunctions.append_fields available for this.

    >>> sa = numpy.array([(1, 'Foo'), (2, 'Bar')], \
                         dtype=[('id', int), ('name', 'S3')])
    >>> sa.dtype.descr == numpy.dtype([('id', int), ('name', 'S3')])
    True
    >>> sb = add_field(sa, [('score', float)])
    >>> sb.dtype.descr == numpy.dtype([('id', int), ('name', 'S3'), \
                                       ('score', float)])
    True
    >>> numpy.all(sa['id'] == sb['id'])
    True
    >>> numpy.all(sa['name'] == sb['name'])
    True
    """
    if a.dtype.fields is None:
        raise ValueError, "`A' must be a structured numpy array"
    b = np.empty(a.shape, dtype=a.dtype.descr + descr)
    for name in a.dtype.names:
        b[name] = a[name]
    return b
