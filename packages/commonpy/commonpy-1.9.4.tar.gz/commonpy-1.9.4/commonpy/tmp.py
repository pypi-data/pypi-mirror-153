def readable(dest, uid = None, gid = None):
    '''Returns True if the given 'dest' is accessible and readable.

    The optional parameters 'gid' and 'gid' can be used to explicitly set
    the user id and/or group id to test, making it possible to test permissions
    for users and groups who are not the uid/gid of the current running user.
    '''

    test_uid = uid or getpwnam(user).pw_uid
    test_gid = gid or getpwnam(user).pw_gid

    dest_stat = os.stat(dest)
    mode = dir_stat[stat.ST_MODE]

    # https://stackoverflow.com/a/46745175/743730
    if test_uid == dest_stat[stat.ST_UID] and (mode & stat.S_IRWXU) == stat.S_IRWXU:
        return True
    elif test_gid == dest_stat[stat.ST_GID] and (mode & stat.S_IRWXG) == stat.S_IRWXG:
        return True
    elif (mode & stat.S_IRWXO) == stat.S_IRWXO:
        return True
    return False
