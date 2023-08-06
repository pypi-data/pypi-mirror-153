""" Low level file system utilities that import only `os` and `sys` (no constants.py)

FIXME: Use builtin pathlib.Path and URL classes

>>> url_filename('http://whatever.com/abs/dir/name/')
'name'
>>> path_filename('/whatever.com/abs/dir/name/')
'name'
>>> path_filename('/whatever.com/abs/dir/name.txt')
'name.txt'
>>> basename('http://example.com/abs/dir/name/')
'name'
>>> basename('http://www.example.com/basename.some.big.tar.gz')
'basename'
"""
try:
    from collections.abc import Mapping
except ImportError:  # python <3.7
    from collections import Mapping
from configparser import ConfigParser
import datetime
import errno
import gzip
import io
import json
import logging
import os
from pathlib import Path
import subprocess
import yaml

from qary.config import DATA_DIR, BASE_DIR, MAX_LEN_FILEPATH

logger = logging.getLogger(__name__)


def url_filename(url):
    """ Extract filename.ext from a url ([protocol] [fqdn] path)

    >>> url_filename('http://whatever.com/abs/dir/name/')
    'name'
    >>> url_filename('whatever.com/abs/dir/name.txt')
    'name.txt'
    """
    return Path(url).name


def path_filename(url):
    """ Extract filename.ext from a path

    >>> path_filename('/whatever.com/abs/dir/name/')
    'name'
    >>> path_filename('/whatever.com/abs/dir/name.txt')
    'name.txt'
    """
    return url_filename(url)


def basename(filename):
    """ Extract filename from a protocol://fqdn/path/filename.ext

    >>> basename('basename.some.big.tar.gz')
    'basename'
    >>> basename('http://www.example.com/basename.some.big.tar.gz')
    'basename'
    >>> basename('http://example.com/abs/dir/name/')
    'name'
    """
    filename = str(url_filename(filename))
    for i in range(256):
        filename, ext = os.path.splitext(filename)
        if not ext or not filename:
            return filename
    return filename


def read_bigdata_directory(
        path=None, data_dir=Path(__file__).parent.parent.joinpath('data')):
    """ Loads the YAML file that contains the LARGE_FILES nested dictionary of bigdata info

    >>> bdd = read_bigdata_directory()
    >>> len(bdd) >= 13
    True
    >>> all(('/qary/data/' in meta['path'].as_posix()
    ...      for name, meta in bdd.items()))
    True
    >>> bdd['wikipedia-titles']['relative_path']
    'corpora/wikipedia/enwiki-latest-all-titles-in-ns0.gz'
    """
    path = path or Path(data_dir, 'downloadable_bigdata_directory.yml')
    file_stream = Path(path).open()
    relative_large_files = yaml.safe_load(file_stream)
    large_files = relative_large_files.copy()
    for name, meta in relative_large_files.items():
        large_files[name].update({
            'path': Path(data_dir, meta['relative_path'])})
    return large_files


LARGE_FILES = read_bigdata_directory(Path(DATA_DIR, 'downloadable_bigdata_directory.yml'))
tmp_large_files = {}
for name, meta in LARGE_FILES.items():
    m = dict()
    m.update(meta)
    # add redundant keys for the url and the filenames in the url
    m['url_filename'] = url_filename(m['url'])
    m['filename'] = path_filename(m['path']) or m['url_filename']
    for k in m['url'], m['filename'], m['url_filename'], basename(m['url_filename']):
        tmp_large_files[k] = m
LARGE_FILES.update(tmp_large_files)
del tmp_large_files, m, k
LARGE_FILES['wikipedia'] = LARGE_FILES['wikipedia_articles']
LARGE_FILES['albert'] = LARGE_FILES['albert-large-v2']
LARGE_FILES['albert_large'] = LARGE_FILES['albert-large-v2']
LARGE_FILES['albert_large_v2'] = LARGE_FILES['albert-large-v2']


LARGE_FILES['stanford_words'] = {
    'url': 'https://nlp.stanford.edu/~lmthang/morphoNLM/cwCsmRNN.words',
    'relative_path': 'corpora/stanford.words',
    'url_filename': 'cwCsmRNN.words',
    'filename': 'stanford.words',
    'documentation': "[Better Word Representations with Recursive Neural Networks for Morphology](https://nlp.stanford.edu/~lmthang/morphoNLM/)"
}


##################################################
# from pugnlp.futils

def expand_filepath(filepath):
    """ Expand any '~', '.', '*' variables in filepath.

    >>> len(expand_filepath('~')) > 3
    True
    """
    return os.path.abspath(os.path.expandvars(os.path.expanduser(filepath)))


def ensure_open(f, mode='r'):
    r""" Return a file pointer using gzip.open if filename ends with .gz otherwise open()

    TODO: try to read a gzip rather than relying on gz extension, likewise for zip and other formats
    TODO: monkey patch the file so that .write_bytes=.write and .write writes both str and bytes

    >>> fn = os.path.join(DATA_DIR, 'unittests', 'wsj_pugnlp.detector_morse.Detector.json.gz')
    >>> fp = ensure_open(fn)
    >>> fp
    <gzip _io.BufferedReader name='...qary/data/unittests/wsj_pugnlp.detector_morse.Detector.json.gz' 0x...>
    >>> fp.closed
    False
    >>> with fp:
    ...     print(len(fp.read()))
    7038854
    >>> fp.read()
    Traceback (most recent call last):
      ...
    ValueError: I/O operation on closed file
    >>> len(ensure_open(fp).read())
    7038854
    >>> fn = os.path.join(DATA_DIR, 'constants', 'emoticons-from-wikipedia.csv')
    >>> fp = ensure_open(fn)
    >>> len(fp.readlines())
    43
    >>> len(fp.read())
    0
    >>> len(ensure_open(fp).read())
    0
    >>> fp.close()
    >>> len(fp.read())
    Traceback (most recent call last):
      ...
    ValueError: I/O operation on closed file.
    """
    fin = f
    if isinstance(f, (str, bytes)):
        if len(f) <= MAX_LEN_FILEPATH:
            f = find_filepath(f) or f
            if f and (not hasattr(f, 'seek') or not hasattr(f, 'readlines')):
                if f.lower().endswith('.gz'):
                    return gzip.open(f, mode=mode)
                return open(f, mode=mode)
            f = fin  # reset path in case it is the text that needs to be opened with StringIO
        else:
            f = io.StringIO(f)
    elif f and getattr(f, 'closed', None):
        if hasattr(f, '_write_gzip_header'):
            return gzip.open(f.name, mode=mode)
        else:
            return open(f.name, mode=mode)
    return f


def update_dict_types(d, update_keys=True, update_values=True, typ=(int,)):
    """Coerce dict keys and values into a new type (usually `int`)

    Retains original key/value mappings and just add new mappings for new types
    >>> update_dict_types({'1': '2', '3': {'4': 'five'}})
    {'1': '2', '3': {'4': 'five', 4: 'five'}, 1: 2, 3: {'4': 'five', 4: 'five'}}
    """
    di = {}
    if not isinstance(typ, tuple):
        typ = (typ, )
    for k, v in d.items():
        ki, vi = k, v
        for t in typ:  # stop coercing type when the first conversion works
            if update_values and vi is v:
                try:
                    vi = t(v)
                except ValueError:
                    pass
                except TypeError:   # FIXME: nested dicts inside of dicts need to be dealt with here
                    if isinstance(v, Mapping):
                        vi = update_dict_types(v, update_keys=update_keys, update_values=update_values, typ=typ)
            if update_keys and ki is k:
                try:
                    ki = t(k)
                except ValueError:
                    pass
        di[ki] = vi
    d.update(di)
    return d


def read_json(filepath, intkeys=True, intvalues=True):
    """ read text from filepath (`open(find_filepath(expand_filepath(fp)))`) then json.loads()

    >>> js = read_json('wsj_pugnlp.detector_morse.Detector.json.gz', intvalues=False)
    >>> list(js.keys())
    ['py/object', 'classifier', 'nocase']
    """
    d = json.load(ensure_open(find_filepath(filepath), mode='rt'))
    d = update_dict_types(d, update_keys=intkeys, update_values=intvalues)
    return d


def expand_path(path, follow_links=False):
    """ Expand shell variables ("$VAR"), user directory symbols (~), and return absolute path

    >>> path0 = '~/whatever.txt'
    >>> path = expand_path(path0)
    >>> path.endswith(path0[2:])
    True
    >>> len(path) > len(path0)
    True
    >>> '~' in path
    False
    >>> path.startswith(os.path.sep)
    True
    """
    path = os.path.expandvars(os.path.expanduser(path))
    if follow_links:
        return os.path.realpath(path)
    return os.path.abspath(path)


def find_filepath(
        filename,
        basepaths=(
            os.path.curdir, DATA_DIR, os.path.join(DATA_DIR, 'constants'),
            os.path.join(DATA_DIR, 'unittests'),
            BASE_DIR, '~', '~/Downloads', os.path.join('/', 'tmp'), '..')):
    """ Given a filename or path see if it exists in any of the common places datafiles might be

    >>> p = find_filepath('tlds-from-iana.csv')
    >>> p == expand_filepath(os.path.join(DATA_DIR, 'constants', 'tlds-from-iana.csv'))
    True
    >>> p.endswith(os.path.join('qary', 'data', 'constants', 'tlds-from-iana.csv'))
    True
    >>> os.path.isfile(p)
    True
    >>> find_filepath('exponentially-crazy-filename-2.718281828459045.nonexistent')
    False
    """
    if os.path.isfile(filename):
        return filename
    for basedir in basepaths:
        fullpath = expand_filepath(os.path.join(basedir, filename))
        if os.path.isfile(fullpath):
            return fullpath
    return False


def walk_level(path, level=1):
    """Like os.walk, but takes `level` kwarg that indicates how deep the recursion will go.

    Notes:
        TODO: refactor `level`->`depth`

    References:
        http://stackoverflow.com/a/234329/623735

    Args:
        path (str):  Root path to begin file tree traversal (walk)
            level (int, optional): Depth of file tree to halt recursion at.
            None = full recursion to as deep as it goes
            0 = nonrecursive, just provide a list of files at the root level of the tree
            1 = one level of depth deeper in the tree

    Examples:
        >>> root = os.path.dirname(__file__)
        >>> all((os.path.join(base,d).count('/') == (root.count('/')+1))
        ...     for (base, dirs, files) in walk_level(root, level=0) for d in dirs)
        True
    """
    if level is None:
        level = float('inf')
    path = expand_path(path)
    if os.path.isdir(path):
        root_level = path.count(os.path.sep)
        for root, dirs, files in os.walk(path):
            yield root, dirs, files
            if root.count(os.path.sep) >= root_level + level:
                del dirs[:]
    elif os.path.isfile(path):
        yield os.path.dirname(path), [], [os.path.basename(path)]
    else:
        raise RuntimeError("Can't find a valid folder or file for path {0}".format(repr(path)))


def get_type(full_path):
    """Get the type (socket, file, dir, symlink, ...) for the provided path"""
    status = {'type': []}
    if os.path.ismount(full_path):
        status['type'] += ['mount-point']
    elif os.path.islink(full_path):
        status['type'] += ['symlink']
    if os.path.isfile(full_path):
        status['type'] += ['file']
    elif os.path.isdir(full_path):
        status['type'] += ['dir']
    if not status['type']:
        if os.stat.S_ISSOCK(status['mode']):
            status['type'] += ['socket']
        elif os.stat.S_ISCHR(status['mode']):
            status['type'] += ['special']
        elif os.stat.S_ISBLK(status['mode']):
            status['type'] += ['block-device']
        elif os.stat.S_ISFIFO(status['mode']):
            status['type'] += ['pipe']
    if not status['type']:
        status['type'] += ['unknown']
    elif status['type'] and status['type'][-1] == 'symlink':
        status['type'] += ['broken']
    return status['type']


def get_stat(full_path):
    """Use python builtin equivalents to unix `stat` command and return dict containing stat data about a file"""
    status = {}
    status['size'] = os.path.getsize(full_path)
    status['accessed'] = datetime.datetime.fromtimestamp(os.path.getatime(full_path))
    status['modified'] = datetime.datetime.fromtimestamp(os.path.getmtime(full_path))
    status['changed_any'] = datetime.datetime.fromtimestamp(os.path.getctime(full_path))
    # first 3 digits are User, Group, Other permissions: 1=execute,2=write,4=read
    status['mode'] = os.stat(full_path).st_mode
    status['type'] = get_type(full_path)
    return status


def path_status(path, filename='', status=None, deep=False, verbosity=0):
    """ Retrieve the access, modify, and create timetags for a path along with its size

    Arguments:
        path (str): full path to the file or directory to be statused
        status (dict): optional existing status to be updated/overwritten with new status values
        try_open (bool): whether to try to open the file to get its encoding and openability

    Returns:
        dict: {'size': bytes (int), 'accessed': (datetime), 'modified': (datetime), 'changed_any': (datetime)}

    >>> stat = path_status(__file__)
    >>> stat['path'] == __file__
    True
    >>> 256000 > stat['size'] > 14373
    True
    >>> stat['type']
    'file'
    """
    status = {} if status is None else status

    path = expand_path(path)
    if filename:
        dir_path = path
    else:
        dir_path, filename = os.path.split(path)  # this will split off a dir as `filename` if path doesn't end in a /
    full_path = os.path.join(dir_path, filename)
    if verbosity > 1:
        print('stat: {}'.format(full_path))
    status['name'] = filename
    status['path'] = full_path
    status['dir'] = dir_path
    status['type'] = []
    try:
        status.update(get_stat(full_path))
    except OSError:
        status['type'] = ['nonexistent'] + status['type']
        logger.info("Unable to stat path '{}'".format(full_path))
    status['type'] = '->'.join(status['type'])

    return status


def find_files(path='', ext='', level=None, typ=list, dirs=False, files=True, verbosity=0):
    """ Recursively find all files in the indicated directory

    Filter by the indicated file name extension (ext)

    Args:
        path (str):  Root/base path to search.
        ext (str):   File name extension. Only file paths that ".endswith()" this string will be returned
        level (int, optional): Depth of file tree to halt recursion at.
                None = full recursion to as deep as it goes
                0 = nonrecursive, just provide a list of files at the root level of the tree
                1 = one level of depth deeper in the tree
        typ (type):  output type (default: list). if a mapping type is provided the keys will be the full paths (unique)
        dirs (bool):  Whether to yield dir paths along with file paths (default: False)
        files (bool): Whether to yield file paths (default: True)
                `dirs=True`, `files=False` is equivalent to `ls -d`

    Returns:
        list of dicts: dict keys are { 'path', 'name', 'bytes', 'created', 'modified', 'accessed', 'permissions' }
                path (str): Full, absolute paths to file beneath the indicated directory and ending with `ext`
                name (str): File name only (everythin after the last slash in the path)
                size (int): File size in bytes
                created (datetime): File creation timestamp from file system
                modified (datetime): File modification timestamp from file system
                accessed (datetime): File access timestamp from file system
                permissions (int): File permissions bytes as a chown-style integer with a maximum of 4 digits
                type (str): One of 'file', 'dir', 'symlink->file', 'symlink->dir', 'symlink->broken'
                              e.g.: 777 or 1755

    Examples:
        >>> 'fileutils.py' in [d['name'] for d in find_files(os.path.dirname(__file__), ext='.py', level=0)]
        True
        >>> next(d for d in find_files(os.path.dirname(__file__), ext='.py')
        ...      if d['name'] == 'fileutils.py')['size'] > 1000
        True

        There should be an __init__ file in the same directory as this script.
        And it should be at the top of the list.
        >>> sorted(d['name'] for d in find_files(os.path.dirname(__file__), ext='.py', level=0))[0]
        'accuracy_reports.py'
        >>> all(d['type'] in ('file', 'dir',
        ...                   'symlink->file', 'symlink->dir', 'symlink->broken',
        ...                   'mount-point->file', 'mount-point->dir',
        ...                   'block-device', 'pipe', 'special', 'socket', 'unknown')
        ...     for d in find_files(level=1, files=True, dirs=True))
        True
        >>> os.path.join(os.path.dirname(__file__), 'fileutils.py') in find_files(
        ... os.path.dirname(__file__), ext='.py', level=0, typ=dict)
        True
    """
    path = expand_path(path)
    gen = generate_files(path, ext=ext, level=level, dirs=dirs, files=files, verbosity=verbosity)
    if isinstance(typ(), Mapping):
        return typ((ff['path'], ff) for ff in gen)
    elif typ is not None:
        return typ(gen)
    else:
        return gen


def generate_files(path='', ext='', level=None, dirs=False, files=True, verbosity=0):
    """ Recursively generate files (and thier stats) in the indicated directory

    Filter by the indicated file name extension (ext)

    Args:
        path (str):  Root/base path to search.
        ext (str or list of str):  File name extension(s).
            Only file paths that ".endswith()" this string will be returned
        level (int, optional): Depth of file tree to halt recursion at.
            None = full recursion to as deep as it goes
            0 = nonrecursive, just provide a list of files at the root level of the tree
            1 = one level of depth deeper in the tree
        typ (type):  output type (default: list). if a mapping type is provided the keys will be the full paths (unique)
        dirs (bool):  Whether to yield dir paths along with file paths (default: False)
        files (bool): Whether to yield file paths (default: True)
            `dirs=True`, `files=False` is equivalent to `ls -d`

    Returns:
        list of dicts: dict keys are { 'path', 'name', 'bytes', 'created', 'modified', 'accessed', 'permissions' }
        path (str): Full, absolute paths to file beneath the indicated directory and ending with `ext`
        name (str): File name only (everythin after the last slash in the path)
        size (int): File size in bytes
        changed_any (datetime): Timestamp for modification of either metadata (e.g. permissions) or content
        modified (datetime): File content modification timestamp from file system
        accessed (datetime): File access timestamp from file system
        permissions (int): File permissions bytes as a chown-style integer with a maximum of 4 digits
        type (str): One of 'file', 'dir', 'symlink->file', 'symlink->dir', 'symlink->broken'
                e.g.: 777 or 1755

    Examples:
        >>> 'fileutils.py' in [d['name'] for d in generate_files(os.path.dirname(__file__), ext='.py', level=0)]
        True
        >>> next(d for d in generate_files(os.path.dirname(__file__), ext='.py')
        ...      if d['name'] == 'fileutils.py')['size'] > 1000
        True
        >>> sorted(next(generate_files()).keys())
        ['accessed', 'changed_any', 'dir', 'mode', 'modified', 'name', 'path', 'size', 'type']

        There should be an __init__ file in the same directory as this script.
        And it should be at the top of the list.
        >>> sorted(d['name'] for d in generate_files(os.path.dirname(__file__), ext='.py', level=0))[0]
        'accuracy_reports.py'
        >>> len(list(generate_files(__file__, ext='.')))
        0
        >>> len(list(generate_files(__file__, ext=['invalidexttesting123', False])))
        0
        >>> len(list(generate_files(__file__, ext=['.py', '.pyc', 'invalidexttesting123', False]))) > 0
        True
        >>> sorted(generate_files(__file__))[0]['name'] == os.path.basename(__file__)
        True
        >>> sorted(list(generate_files())[0].keys())
        ['accessed', 'changed_any', 'dir', 'mode', 'modified', 'name', 'path', 'size', 'type']
        >>> all(d['type'] in ('file', 'dir',
        ...                   'symlink->file', 'symlink->dir', 'symlink->broken',
        ...                   'mount-point->file', 'mount-point->dir',
        ...                   'block-device', 'pipe', 'special', 'socket', 'unknown')
        ...     for d in generate_files(level=1, files=True, dirs=True))
        True
    """
    path = expand_path(path or '.')
    # None interpreted as '', False is interpreted as '.' (no ext will be accepted)
    ext = '.' if ext is False else ext
    # multiple extensions can be specified in a list or tuple
    ext = ext if ext and isinstance(ext, (list, tuple)) else [ext]
    # case-insensitive extensions, '.' ext means only no-extensions are accepted
    ext = set(x.lower() if x else '.' if x is False else '' for x in ext)

    if os.path.isfile(path):
        fn = os.path.basename(path)
        # only yield the stat dict if the extension is among those that match or files without any ext are desired
        if not ext or any(path.lower().endswith(x) or (x == '.' and '.' not in fn) for x in ext):
            yield path_status(os.path.dirname(path), os.path.basename(path), verbosity=verbosity)
    else:
        for dir_path, dir_names, filenames in walk_level(path, level=level):
            if verbosity > 0:
                print('Checking path "{}"'.format(dir_path))
            if files:
                for fn in filenames:  # itertools.chain(filenames, dir_names)
                    if ext and not any((fn.lower().endswith(x) or (x == '.' and x not in fn) for x in ext)):
                        continue
                    stat = path_status(dir_path, fn, verbosity=verbosity)
                    if stat and stat['name'] and stat['path']:
                        yield stat
            if dirs:
                for fn in dir_names:
                    if ext and not any((fn.lower().endswith(x) or (x == '.' and x not in fn) for x in ext)):
                        continue
                    yield path_status(dir_path, fn, verbosity=verbosity)


def find_dirs(*args, **kwargs):
    kwargs['files'] = kwargs.get('files', False)
    kwargs.update({'dirs': True})
    return find_files(*args, **kwargs)


def mkdir_p(path, exist_ok=True):
    """`mkdir -p` functionality (don't raise exception if path exists)

    Make containing directory and parent directories in `path`, if they don't exist.

    Arguments:
                    path (str): Full or relative path to a directory to be created with mkdir -p

    Returns:
                    str: 'pre-existing: {path}' or 'new: {path}'

    References:
                    http://stackoverflow.com/a/600612/623735
    """
    path = expand_path(path)
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno == errno.EEXIST and os.path.isdir(path) and exist_ok:
            return 'pre-existing: ' + path
        else:
            raise
    return 'new: ' + path


def touch(filepath, times=None, mkdir=False):
    """ Update the modify (modify) and change (ctime) timestamps of a file, create if necessary

    >>> filepath = os.path.join(DATA_DIR, 'tmpfilefortouch.txt')
    >>> touch(filepath).endswith('tmpfilefortouch.txt')
    True
    >>> os.path.isfile(filepath)
    True
    >>> os.remove(filepath)
    """
    filepath = expand_path(filepath)
    if mkdir:
        mkdir_p(os.path.dirname(filepath))
    with open(filepath, 'a'):
        if times or times is None:
            os.utime(filepath, times)
    return filepath


def touch_p(filepath, times=None, mkdir=True):
    """ mkdir_p(filepath) then touch(filepath)

    >>> filepath = os.path.join(DATA_DIR, 'tmpdirfortouch', 'tmpfilefortouch.txt')
    >>> touch_p(filepath).endswith(os.path.join('tmpdirfortouch', 'tmpfilefortouch.txt'))
    True
    >>> os.path.isfile(filepath)
    True
    >>> os.remove(filepath)
    >>> os.rmdir(os.path.dirname(filepath))
    """
    return touch(filepath=filepath, times=times, mkdir=mkdir)


def sudo_yield_file_lines(file_path='/etc/NetworkManager/system-connections/*'):
    r"""Cat a file iterating/yielding one line at a time,

    shell will execute: `sudo cat $file_path` so if your shell doesn't have sudo or cat, no joy
    Input:
                    file_path(str): glob stars are fine

    >> for line in sudo_yield_file_lines('/etc/NetworkManager/system-connections/*')


    """
    # substitute your Windoze/DOS/PowerlessShell command here:
    sudo_cat_cmd = 'sudo cat {}'.format(file_path)

    process = subprocess.Popen(sudo_cat_cmd, stdout=subprocess.PIPE, shell=True)
    # read one line at a time, as it becomes available
    for line in iter(process.stdout.readline, ''):
        yield line


def sudo_iter_file_lines(file_path):

    class FileLineIterable:

        def __init__(self, file_path=file_path):
            file_path = expand_path(file_path)
            self.file_path = file_path
            self.cat_cmd = 'sudo cat {}'.format(self.file_path)
            self.process = subprocess.Popen(self.cat_cmd, stdout=subprocess.PIPE, shell=True)

        def __iter__(self):
            # __iter__ returns an `iterator` instance. having an __iter__ make this class `iterable`
            return self

        def next(self):  # noqa
            # substitute your Windoze/DOS/PowerlessShell command here:
            return self.process.stdout.readline()
            # raise StopIteration()

    return FileLineIterable(file_path)


def ssid_password(source='/etc/NetworkConnections/system-connections', ext=''):
    source = expand_path(source)
    if isinstance(source, ConfigParser):
        ssid = source.get('wifi', 'ssid') if source.has_option('wifi', 'ssid') else None
        psk = source.get('wifi-security', 'psk') if source.has_option('wifi-security', 'psk') else None
        return (ssid or os.path.basename(source), psk or '')
    elif os.path.isdir(source):
        return dict([ssid_password(meta['path']) for meta in find_files(source, ext=ext)])
    elif os.path.isfile(source) or callable(getattr(source, 'read', None)):
        config = ConfigParser()
        if hasattr(source, 'read'):
            config.read_file(source)
        else:
            config.read(source)
        return ssid_password(config)
    elif isinstance(source, (str, bytes)):
        return ssid_password(io.StringIO(source))

# from pugnlp.futils
##################################################
