
import sys, os, ctypes
from re import match
from os.path import isdir, isfile, islink, join, basename
from os.path import join, isfile, isdir
from .COLORS import *

class DirTree:
    """
    Create and print a directory tree from the given directory
        dotfiles = [default] False -don't show
    """

    def __init__( self,
                  directory     = None,
                  depth         = 999999, *,
                  dotfiles      = False,
                  exclude_dirs  = [],
                  exclude_files = [],
                  regex_ex      = [],
                  regex_in      = [] ):

        if not directory:
            directory = os.getcwd()

        elif not isdir( directory ):
            try:
                assert isdir( join( os.getcwd(), directory ))
                directory = join( os.getcwd(), directory )
            except:
                directory = os.getcwd()

        self.base_dir      = directory
        self.depth         = depth
        self.dotfiles      = dotfiles
        self.regex_ex      = regex_ex
        self.regex_in      = regex_in
        self.exclude_dirs  = exclude_dirs
        self.exclude_files = exclude_files

        self.__getSkel()

    def __getSkel(self):
        """
        Recursive scan of base directory

            Returns layered dictionary { 'dirs': {}, 'files': [] }
        """
        @staticmethod
        def create_subdir():
            subdir = { 'dirs' : {},
                       'files': [] }
            return subdir

        base_dir     = self.base_dir
        dotfiles     = self.dotfiles
        scandirs     = []
        self.listing = create_subdir()


        @staticmethod
        def iterDir(directory):
            def has_hidden_attr(filepath):
                try:
                    attrs = ctypes.windll.kernel32.GetFileAttributesW(unicode(filepath))
                    assert attrs != -1
                    result = bool(attrs & 2)
                except (AttributeError, AssertionError):
                    result = False
                return result

            dirs, files = [], []
            for i in os.listdir(directory):
                if ( match( '^\.+', i ) or has_hidden_attr( join( directory, i )) ) and not dotfiles:
                    continue

                if isdir( join( directory, i )):
                    dirs.append(i)

                else:
                    files.append(i)

            dirs.sort()
            files.sort()

            return files, dirs

        level = 0
        scandirs = [( self.listing, base_dir, level )]

        scan = True
        while scan:
            try:
                current = scandirs[0][0]
                scandir = scandirs[0][1]
                level   = scandirs[0][2]
                scandirs.pop(0)
            except:
                scan = False
                continue

            F, D = iterDir(scandir)
            for d in D:
                if self.__chk_exclude(d, ftype = 'dir'):
                    current['dirs'][d] = create_subdir()
                    if level < self.depth:
                        scandirs.append(( current['dirs'][d], join(scandir, d), level + 1 ))

            for f in F:
                if self.__chk_exclude(f):
                    current['files'].append(f)

    def __chk_reg(func):
        def __wrapper(self, item, ftype = 'file'):
            if ( not self.regex_ex and not self.regex_in ) or ftype == 'dir':
                R = func(self, item, ftype)
                return R

            exclude = False

            if self.regex_in:
                exclude = True
                for inc in self.regex_in:
                    if match( inc, item ):
                        exclude = False
                        break

            if exclude:
                return False

            for ex in self.regex_ex:
                if match( ex, item ):
                    return False

            R = func(self, item, ftype)
            return R

        return __wrapper

    @__chk_reg
    def __chk_exclude(self, item, ftype = 'file'):
        if ftype == 'dir':
            if item in self.exclude_dirs:
                return False

            return True

        else:
            if item in self.exclude_files:
                return False

            return True

    def list_tty(self):
        """
        Return directory tree formatted for terminal view
        """
        _FORMAT = { 'dir'   : f"{C_b()}_-_{C__()}",     # blue
                    'text'  : f"{C_Gr()}_-_{C__()}",    # dark gray
                    'file'  : f"{C_gri()}_-_{C__()}",   # italic gray
                    'tree'  : f"{C_g()}_-_{C__()}",     # green
                    'pre'   : f"\n{C_W()}    {F_U()}Base Directory{C__()}\n\n",
                    'post'  : "",
                    'nl'    : '\n' }

        self.__getSkel()
        list_tree = self.get_tree( self.listing, _FORMAT, self.base_dir )

        return list_tree

    def list_gui(self):
        """
        Return directory tree in html formatting
        """
        _FORMAT = { 'dir'   : "<font color=\"cyan\" >_-_</font>",          # cyan
                    'text'  : "<font color=\"gray\" >_-_</font>",          # gray
                    'file'  : "<font color=\"light gray\" >_-_</font>",    # light gray
                    'tree'  : "<font color=\"green\" >_-_</font>",         # green
                    'pre'   : "<pre><font color: white;>  <u>Skeleton Directory</u></font><br>",
                    'post'  : "</pre>",
                    'nl'    : "<br>" }

        self.__getSkel()
        list_tree = self.get_tree( self.listing, _FORMAT, self.base_dir )

        return list_tree

    @staticmethod
    def get_tree( listing, F, skel ):
        def tree(f):
            T, B, L = '     ├', '──', '     └'

            if f == 'T':
                return T + B

            elif f == 'L':
                return L + B

            else:
                raise RuntimeError(f"Invalid key for 'f' - '{f}'")

        def indentText(num):
            pbT = '     │'
            pbF = '      '
            R = ''

            if num == 0:
                return ''

            for i in range(0, num):
                if passbar[i]:
                    R = R + pbT
                else:
                    R = R + pbF

            return R

        def getlist(obj):
            d = []
            for i in obj['dirs']:
                d.append(( obj['dirs'][i], i ))

            f = obj['files']
            f.sort()

            return d, f

        Ilist, Plist = [], [ F['pre'], F['dir'].replace('_-_', '      ' + skel + '/'),  ]
        form = F

        dirs, files = getlist(listing)
        passbar = {0: False}
        level = 1
        passbar[level] = True
        Plist.append( f"{F['tree'].replace('_-_', indentText(level))}" )
        if len(dirs) + len(files) <= 1:
            passbar[level] = False

        Ilist.append(( dirs, files, level ))
        dirs, files = [], []

        while True:
            try:
                nextdir = dirs[0][0]

                if len(dirs) + len(files) == 1:
                    Plist.append( f"{F['tree'].replace('_-_', indentText(level) + tree('L'))} {F['dir'].replace('_-_', dirs[0][1] + '/')}" )
                    passbar[level] = False
                else:
                    Plist.append( f"{F['tree'].replace('_-_', indentText(level) + tree('T'))} {F['dir'].replace('_-_', dirs[0][1] + '/')}" )
                    passbar[level] = True

                dirs.pop(0)
                Ilist.append(( dirs, files, level ))
                level += 1
                dirs, files = getlist(nextdir)

            except IndexError:
                for i in range(0, len(files)):
                    if i == len(files) - 1:
                        t = 'L'
                    else:
                        t = 'T'

                    preT = F['tree'].replace('_-_', indentText(level) + tree(t))
                    Plist.append( f"{preT} {F['file'].replace('_-_', files[i])}" )

                try:
                    dirs, files, level = Ilist[-1]
                    Ilist.pop(-1)

                except IndexError:
                    Plist.append( F['post'] )
                    break

        return F['nl'].join(Plist)

if __name__ == "__main__":
    from getopt import getopt
    from tabulate import tabulate
    from time import sleep

    def help_message():
        headers = [ f"{C_W()}Short{C__()}", f"{C_W()}Long{C__()}", f"{C_W()}Description{C__()}" ]

        body = []

        opts = [ ( "-b", "--base-dir", f"Set base directory{C__()}\n{C_Gri()}  -uses current directory if not specified" ),
                 ( "-d", "--depth", f"Integer to set the depth of directory tree{C__()}\n{C_Gri()}  -ex: '0' will only print the base directory list" ),
                 ( "-D", "--dotfiles", f"Include hidden files in tree" ),
                 ( "-e", "--exclude", f"Filenames/directories to exclude from the tree{C__()}\n{C_Gri()}  -see *Exclusions*" ),
                 ( "-h", "--help", "This help message" ),
                 ( "-q", "--qt-html", "Print in *html format for use with QT" ),
                 ( "-r", "--regex", f"Use regex to include/exclude files in tree{C__()}\n{C_Gri()}  -see *Regex*" )]

        table = []
        for i in opts:
            table.append([ C_Y() + i[0] + C__(),
                           C_Y() + i[1] + C__(),
                           C_Gr() + i[2] + C__() ])

        tab  = tabulate(table, headers, tablefmt="fancy_grid").split('\n')

        _ = f"{C_Gr()}|{C_Y()}"
        print( '\n'.join([ f"\n{C_W()}    {F_U()}DirTree{C__()}",
                           f"{C_gr()}      Windows:",
                           f"{C_B()}        py{C_Y()} -m{C_P()} bbdirtree{C_gri()} [OPTIONS]{C_Gri()} [ARGS]{C__()}\n",
                           f"{C_gr()}      Linux/Mac:",
                           f"{C_B()}        python{C_Y()} -m{C_P()} bbdirtree{C_gri()} [OPTIONS]{C_Gri()} [ARGS]{C__()}\n",
                           f"{C_gr()}    {F_U()}Options:{C__()}",
                           "      " + "\n      ".join(tab),
                           '\n',
                           f"{C_W()}  *{F_U()}Exclusions{F__U()}*{C__()}",
                           f"{C_gri()}      Provide names of files or directories to exclude. To exclude",
                           "    multiple files/directories, quote entire list and seperate",
                           f"    with a colon '{C__()}{C_W()}:{C_gri()}'. Add a '{C__()}{C_W()}/{C_gri()}' to specify a directory name to",
                           "    exclude.\n",
                           "      Example:",
                           f"{C_P()}        bbdirtree{C_Y()} --exclude{C_Gri()} \"excluded dir/:excluded file\"\n",
                           f"{C_W()}  *{F_U()}Regex{F__U()}*{C__()}",
                           f"{C_gri()}      Prefix regex with {C__()}{C_Y()}include={C_Gr()} or{C_Y()} exclude={C_gri()}.",
                           "    Seperate each regex with a space, quoting each individual argument.\n",
                           "      Example:",
                           f"{C_P()}        bbdirtree{C_Y()} --regex{C_Gri()} \"exclude=.*\\.ini$\"{C_gri()} will",
                           "          exclude any files that have an 'ini' extension.",
                           f"{C_P()}        bbdirtree{C_Y()} --regex{C_Gri()} \"include=.*\\.mp3$\"{C_gri()} will",
                           "          include only files with an 'mp3' extension.\n",
                           "      This has no effect on directories. Multiple regex can be",
                           f"    used by specifying{C__()}{C_Y()} --regex{C_gri()} multiple times.\n\n" ]))

    try:
        opts, args = getopt( sys.argv[1:], "b:d:De:hqr:", [ "base-dir=",
                                                            "depth=",
                                                            "dotfiles",
                                                            "exclude=",
                                                            "help",
                                                            "qt-html",
                                                            "regex=" ] )
    except:
        opts = []

    BASE_DIR      = os.getcwd()
    DEPTH         = 999999
    DOTFILES      = False
    EXCLUDE_FILES = []
    EXCLUDE_DIRS  = []
    HTML          = False
    REGEX_IN      = []
    REGEX_EX      = []

    for opt, arg in opts:
        if opt in ('-b', '--base-dir'):
            bdir = arg
            if not isdir(bdir):
                bdir = join( os.getcwd(), bdir )
                if isdir(bdir):
                    BASE_DIR = bdir
                else:
                    raise FileNotFoundError(f"Can't find directory - '{arg}'")
            else:
                BASE_DIR = arg

        elif opt in ('-d', '--depth'):
            try:
                dpth = int(arg)
            except:
                raise TypeError("Depth must be an integer")

            DEPTH = dpth

        elif opt in ('-D', '--dotfiles'):
            DOTFILES = True

        elif opt in ('-e', '--exclude'):
            for i in arg.split(':'):
                if match( '.*/$', arg ):
                    EXCLUDE_DIRS.append(i[:-1])
                else:
                    EXCLUDE_FILES.append(i)

        elif opt in ('-h', '--help'):
            help_message()
            sys.exit(0)

        elif opt in ('-q', '--qt-html'):
            HTML = True

        elif opt in ('-r', '--regex'):
            try:
                m = arg.split('=', 1)[0]
                reg = arg.split('=', 1)[1]
            except:
                raise RuntimeError("Invalid format for regex option. See 'dirtree --help'")

            if m == 'include':
                REGEX_IN.append(reg)
            elif m == 'exclude':
                REGEX_EX.append(reg)
            else:
                raise RuntimeError(f"Invalid regex option '{m}'. See 'dirtree --help'")

    x = DirTree( BASE_DIR,
                 DEPTH,
                 dotfiles = DOTFILES,
                 exclude_dirs = EXCLUDE_DIRS,
                 exclude_files = EXCLUDE_FILES,
                 regex_ex = REGEX_EX,
                 regex_in = REGEX_IN )

    if HTML:
        print(x.list_gui())
    else:
        print(x.list_tty())

    sys.exit()
