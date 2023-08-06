from typing import List, Any, Tuple
import os
import platform

DELIM = '/'
SECONDARY_DELIM = '\\'

def get_cwd() -> str:

    """returns current working directory"""

    cd = os.getcwd()

    #replace the cd with primary delim
    cd_replaced = join( * path_to_dirs(cd) )
    return cd_replaced

def path_to_dirs( path: str ) -> List[str]:

    """splits a path into directories"""
    if path == '':
        return []
    return path.split( DELIM )

def is_file( path: str ) -> bool :

    """returns a boolean value to check if the path is a file"""
    return os.path.isfile( path )

def is_dir( path: str ) -> bool :

    """returns a boolean value to check if the path is a directory"""
    return os.path.isdir( path )

def replace_delims( path: str, secondary_delim: str = SECONDARY_DELIM, delim: str = DELIM ) -> str :

    """turns data\dir\file.txt into data/dir/file.txt"""
    return path.replace( secondary_delim, delim )

def join( *items: str ) -> str:

    """joins a list of dirs into a path"""
    return DELIM.join( items )

def convert_bytes( bytes: int, conversion: str = 'MB' ) -> Tuple[ Any, Any ]:

    try:
        conversion = conversion.upper()
    except:
        pass

    kb_to_b = 1024

    conversion_factors = ['KB','MB','GB','TB','PB','EB']
    if conversion in conversion_factors:

        power = conversion_factors.index(conversion) + 1
        return bytes / (kb_to_b ** power), conversion

    return bytes, None


def add_prefix_to_paths( prefix_path, relative_paths ):

    """adds prefix to a list of relaive paths"""

    full_paths = []
    for relative_path in relative_paths:
        full_paths.append( join(prefix_path, relative_path) )

    return full_paths

def remove_prefix_from_paths( prefix_path, full_paths ):

    """Removes prefix from full paths"""

    number_of_dirs = len( path_to_dirs(prefix_path) )

    relative_paths = []
    for full_path in full_paths:

        folder_list = path_to_dirs( full_path )
        relative_list = folder_list[ number_of_dirs : ]

        relative_paths.append( join(*relative_list) )

    return relative_paths

def remove_hanging_slashes( path ):

    """removes ending slashes from paths
    turns "asdf/asdf//" into "asdf/sadf"   """

    # dont go through all the
    for i in range( len(path)-1, -1, -1 ):

        if path[i] != '/':
            return path[:i+1]

    return path

def get_desktop_dir() -> Any:

    """get the location of the desktop"""

    if platform.system() == 'Windows':
        import winshell
        return winshell.desktop()

    return None

def create_shortcut( target_Path, shortcut_Dir ) -> None:

    """places a shortcut from target_Path to shortcut_Dir"""

    if platform.system() == 'Windows':
        import winshell

        shortcut_path = shortcut_Dir.join( target_Path.root + '.lnk' )
        winshell.CreateShortcut( Path=shortcut_path, Target=target_Path.p )

    else:
        print ('No instructions for current OS')

def get_env_var_path_delim() -> str:

    """Returns the delimitter for the OS's path environment variables"""

    if platform.system() == 'Windows':
        return ';'
    elif platform.system() == 'Linux':
        return ':'

def split_env_var_paths( string: str ) -> List[str]:

    """returns a list of path strings split on the system delimitter"""

    return string.split( get_env_var_path_delim() )

def join_env_var_paths( paths: List[str] ) -> str:

    """ returns 'C:/Path1;C:/Path2' """
    return get_env_var_path_delim().join( paths )

def print_to_from( print_off: bool, action_str: str, from_str: str, to_str: str ):

    """ Copying C:/Users/path/file.txt ->  C:/Users/newfile.txt """

    if print_off:
        print ( "{action_str} \t {from_str} -> \t {to_str}".format( action_str = action_str, to_str = to_str, from_str = from_str ) )
