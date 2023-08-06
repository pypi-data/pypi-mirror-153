from __future__ import annotations

import dir_ops as do
from parent_class import ParentClass
from parent_class import ParentPluralList

import datetime
from typing import List, Any, Tuple
import os
import py_starter as ps

class BaseDir( ParentClass ):

    STATIC_METHOD_SUFFIX = '_dir'
    INSTANCE_METHOD_ATTS = ['path']
    inherited_kwargs = {}

    def __init__( self, *args, **kwargs ):

        ParentClass.__init__( self )
        self.dir_construct( *args, **kwargs )

        self.DIR_CLASS = BaseDir
        self.PATH_CLASS = BasePath
        self.DIRS_CLASS = BaseDirs
        self.PATHS_CLASS = BasePaths

    def dir_construct( self, path = '', **kwargs ):

        self.path = do.replace_delims( path )
        self.path = do.remove_hanging_slashes( self.path )  # 'C:/Users/e150445/Documents/MO-EE/Data/Raw'
        self.dirs = do.path_to_dirs( self.path )                #[ 'C','Users','e150445','Documents','MO-EE','Data','Raw' ]
        self.type_dir = True
        self.type_path = False
        self.type_dirs = False
        self.type_paths = False

        self.size = None                          # don't init with checking the size, takes too long
        self.size_units = None

        #alias just for quick coding
        self.p = self.path

    def print_imp_atts( self, **kwargs ):

        return self._print_imp_atts_helper( atts = ['path','dirs'], **kwargs )

    def print_one_line_atts(self, **kwargs ):

        return self._print_one_line_atts_helper( atts = ['type','path'], **kwargs )

    def __eq__( self, other_Dir ):

        if isinstance( other_Dir, self.DIR_CLASS ):
            return self.path == other_Dir.path
        return False

    @staticmethod
    def is_Dir( Object: Any ) -> bool:

        """returns boolean if Object is a Dir"""
        return isinstance( Object, BaseDir )

    def ascend( self, level_to_ascend: int = 1 ) -> BaseDir:
        
        """go up a x number directories -> "levels_to_ascend" """

        return self.DIR_CLASS( path = do.join( *self.dirs[:-1*level_to_ascend] ), **self.inherited_kwargs )
    
    @staticmethod
    def ascend_dir( dir: str, levels_to_ascend: int = 1 ) -> str:

        """go up a x number directories -> "levels_to_ascend" """

        dirs = do.path_to_dirs( dir )
        return do.join( *dirs[:-1*levels_to_ascend] )

    @do.base_instance_method
    def join( self, *args, **kwargs ):
        pass
    
    @staticmethod
    def join_dir( dir: str, *other_dirs, **kwargs ):
        
        """add more dirs to the Dir path"""
        if dir != '':
            return do.join( dir, *other_dirs )
        else:
            return do.join( *other_dirs )

    def join_Dir( self, Dir: BaseDir = None, path: str = '' ) -> BaseDir:
        
        if Dir != None:
            path = Dir.path
        return self.DIR_CLASS( path = self.join( path ), **self.inherited_kwargs )

    def join_Path( self, Path: BasePath = None, path: str = '' ) -> BasePath:

        if Path != None:
            path = Path.path

        return self.PATH_CLASS( path = self.join( path ), **self.inherited_kwargs )

    ##################

    @ps.try_operation_wrap( debug = do.DEBUG )
    @do.inherited_instance_method
    def open( self, *args, **kwargs ):
        pass

    @staticmethod
    def open_dir( *args, **kwargs ): #should be defined by a child class
        assert False

    ##################

    @ps.try_operation_wrap( debug = do.DEBUG )
    @do.inherited_instance_method
    def exists( self, *args, **kwargs ) -> bool:
        pass
    
    @staticmethod
    def exists_dir( *args, **kwargs ): 
        return None

    ##################

    @do.remove_wrap
    @ps.try_operation_wrap( debug = do.DEBUG )
    @do.inherited_instance_method
    def remove(self, *args, **kwargs):
        pass

    @staticmethod
    def remove_dir( *args, **kwargs ): 
        assert False

    ##################


    def create_parents(self, *args, **kwargs):

        """use recursion to travel all the way up the parent directories until we find one that exists, then unfold and create each directory"""

        parent_Dir = self.ascend()
        if parent_Dir.exists() or len(self.dirs) <= 1: #Parent Dir exists or we are at the base directory
            return

        else:
            parent_Dir.create_parents( *args, **kwargs )
            parent_Dir.create( *args, **kwargs )

    ##################

    @do.create_wrap
    @ps.try_operation_wrap( debug = do.DEBUG )
    @do.inherited_instance_method
    def create(self, *args, **kwargs) -> bool:
        pass

    @staticmethod
    def create_dir( *args, **kwargs ) -> bool: #should be defined by a child class
        assert False

    ##################

    @do.copy_wrap
    @ps.try_operation_wrap( debug = do.DEBUG )
    @do.inherited_instance_method
    def copy(self, *args, **kwargs) -> bool:
        pass
    
    @staticmethod
    def copy_dir( *args, **kwargs ) -> bool:
        assert False

    ##################

    def list_contents( self, *args, print_off: bool = False, **kwargs ):

        filenames = []
        filenames.extend( self.list_subfolders() )
        filenames.extend( self.list_files() )

        if print_off:
            ps.print_for_loop( filenames )
        
        return filenames

    ##################

    @do.inherited_instance_method
    def list_files( self, *args, **kwargs ):
        pass

    @staticmethod
    def list_files_dir( *args, **kwargs ):
        return []

    ##################

    @do.inherited_instance_method
    def list_subfolders( self, *args, **kwargs ):
        pass

    @staticmethod
    def list_subfolders_dir( *args, **kwargs ):
        return []

    ##################

    @do.get_size_wrap
    @do.inherited_instance_method
    def get_size( self, *args, **kwargs ):
        pass

    @staticmethod
    def get_size_dir( *args, **kwargs ):
        return 0

    ##################

    def get_rel( self, other_Dir: BaseDir ) -> BaseDir:

        """Given a Dir object, find the relative Dir from Dir to self"""

        return self.DIR_CLASS( path = self.get_rel_dir( self.path, other_Dir.path ), **self.inherited_kwargs )

    @staticmethod
    def get_rel_dir( dir, other_dir ) -> str:
        
        if dir != '':
            return os.path.relpath( dir, other_dir )
        else:
            return other_dir
    
    ##################

    def list_contents_Paths( self, block_dirs: bool = True, block_paths: bool = False, **kwargs ) -> BasePaths:

        Paths_inst = self.PATHS_CLASS( **self.inherited_kwargs )

        # 1. Add all files
        if not block_paths:
            paths = self.list_files( **kwargs )

            for path in paths:
                Paths_inst._add( self.join_Path( path = path ) )

        # 2. Add all dirs
        if not block_dirs:
            dirs = self.list_subfolders( **kwargs )

            for dir in dirs:
                Paths_inst._add( self.join_Dir( path = dir ) )
          
        return Paths_inst


    def walk( self, folders_to_skip: List[str] = ['.git'], **kwargs ) -> BasePaths:

        """Walk through all the contents of the directory"""

        Paths_inst = self.PATHS_CLASS( **self.inherited_kwargs )
        Paths_inst._add( self )

        Paths_under = self.list_contents_Paths( block_dirs = False, block_paths = False, **kwargs )

        for Path_inst in Paths_under:

            # all Paths are also Dirs
            if Path_inst.type_path:
                Paths_inst._add( Path_inst )

            elif Path_inst.type_dir:
                
                if Path_inst.dirs[-1] not in folders_to_skip:
                    Paths_inst.merge( Path_inst.walk( folders_to_skip = folders_to_skip, **kwargs ) )

        return Paths_inst

    def walk_contents_Paths( self, block_dirs: bool = True, block_paths: bool = False, folders_to_skip: List[str] = ['.git'], **kwargs ) -> BasePaths:

        """get all Paths and/or Dirs underneath the entire directory, optional params for returning paths and/or dirs"""

        Paths_inst = self.walk( folders_to_skip=folders_to_skip, **kwargs )
        keep_Paths = self.PATHS_CLASS( **self.inherited_kwargs )

        for Path_inst in Paths_inst:
            if Path_inst.type_path and not block_paths:
                keep_Paths._add( Path_inst )

            if Path_inst.type_dir and not block_dirs:
                keep_Paths._add( Path_inst )

        return keep_Paths

    def get_unique_Path( self, filename: str, **list_contents_Paths_kwargs ) -> str:

        """finds a unique Path for the proposed filename based on the contents of the Directory
        if file.txt already exists in the dir, return file1.txt or file2.txt, etc  """

        # 
        Paths_in_Dir = self.list_contents_Paths( block_dirs=True, block_paths=False, **list_contents_Paths_kwargs )
        filenames = [ P.filename for P in Paths_in_Dir ]

        filename_Path = self.join_Path( path = filename )
        if filename not in filenames:
            return filename_Path
        
        counter = 0
        while True:
            proposed_filename = filename_Path.root + str(counter) + filename_Path.extension
            if proposed_filename not in filenames:
                return self.join( path = proposed_filename )

            counter += 1


class BasePath( BaseDir ):

    STATIC_METHOD_SUFFIX = '_path'
    INSTANCE_METHOD_ATTS = ['path']

    def __init__( self, *args, **kwargs ):

        ParentClass.__init__( self )
        BaseDir.__init__( self, *args, **kwargs ) 
        self.path_construct()

        self.DIR_CLASS = BaseDir
        self.PATH_CLASS = BasePath
        self.DIRS_CLASS = BaseDirs
        self.PATHS_CLASS = BasePaths

    def path_construct(self):

        """Since the Path is different from a Dir, add the extra attiributes"""

        self.filename =     self.get_filename( self.path )                  # feb_mar_v1.0.txt
        self.root =         self.get_root( self.path )                      # feb_mar_v1
        self.root_dots =    self.get_root( self.path, allow_dots=True )     # feb_mar_v1.0
        self.ending =       self.get_ending( self.path )                    # txt
        self.extension =    '.' + self.ending                               # .txt
        self.size = None                          # don't init with checking the size, takes too long
        self.size_units = None
        self.mtime = None                        # a datetime object when its ready

        self.parent_Dir = self.ascend()
        self.type_dir = False
        self.type_path = True
        self.type_dirs = False
        self.type_paths = False

    def __eq__( self, other_Path: BasePath ) -> bool:

        """checks if self is equal to other_Path, returns bool"""

        if isinstance( other_Path, self.PATH_CLASS ):
            return self.path == other_Path.path
        return False

    @staticmethod
    def is_Path( Object: Any ) -> bool:

        """returns boolean if Object is a Dir"""
        return isinstance( Object, BasePath )

    def print_imp_atts(self, print_off = True):

        return self._print_imp_atts_helper( atts = ['path','dirs','ending','size'], print_off = print_off )

    @staticmethod
    def exists_path( *args, **kwargs ):
        return False
    
    @staticmethod
    def remove_path( *args, **kwargs ):
        assert False

    @do.rename_wrap
    @ps.try_operation_wrap( debug = do.DEBUG )
    @do.inherited_instance_method
    def rename( self, *args, **kwargs):
        pass
    
    @staticmethod
    def rename_path( *args, **kwargs ):
        assert False

    @do.get_mtime_wrap
    @do.inherited_instance_method
    def get_mtime( self, *args, **kwargs ):
        pass
    
    @staticmethod
    def get_mtime_path( *args, **kwargs ) -> datetime.datetime:
        return datetime.datetime.utcfromtimestamp( 0 )

    @staticmethod
    def create_path( *args, **kwargs ) -> bool:
        assert False

    @do.inherited_instance_method
    def read( self, *args, **kwargs):
        pass
    
    @staticmethod
    def read_path( path, **kwargs ) -> Any:
        return None

    @ps.try_operation_wrap( debug = do.DEBUG )
    @do.inherited_instance_method
    def write( self, *args, **kwargs):
        pass

    @staticmethod
    def write_path( *args, **kwargs ) -> bool:
        assert False

    def smart_format( self, *args, formatting_dict, write = True, **kwargs) -> str:

        string = self.read()
        formatted_string = ps.smart_format( string, formatting_dict, **kwargs )

        if write:
            self.write( string = formatted_string )

        return formatted_string

    def get_rel( self, Dir_inst: BaseDir, path = '' ) -> BasePath:

        """Given a Dir object, find the relative Path from Dir to self"""

        if Dir_inst != None:
            path = Dir_inst.path

        return self.PATH_CLASS( path = self.get_rel_path( self.path, path ), **self.inherited_kwargs )

    @staticmethod
    def get_rel_path( path: str, dir: str ) -> str:
        return os.path.relpath( path, dir )

    @staticmethod
    def get_filename( path: str ) -> str:

        """returns the filename ('file.txt') from a long path ('C:/path/to/file.txt') """

        dirs = do.path_to_dirs(path)

        if len(dirs) > 0:
            return dirs[-1]
        else:
            return ''
    
    @staticmethod
    def get_root( path: str, allow_dots: bool = False ) -> str:

        '''returns the root of the filename from a path  Dir/a_file1.txt returns "a_file1" '''
        filename = BasePath.get_filename(path)

        if allow_dots:
            root = '.'.join( filename.split('.')[:-1] )

        else:
            root = filename.split('.')[0]
        
        return root
    
    @staticmethod
    def get_ending( path: str ) -> str:

        '''returns the file ending from a path'''
        
        filename = BasePath.get_filename(path)
        ending = filename.split('.')[-1]
        return ending



class BaseDirs( ParentPluralList ):

    inherited_kwargs = {}

    def __init__( self, *args, given_Dirs = [], given_Paths = [], **kwargs ):

        ParentPluralList.__init__( self, att = 'Objs' )
        self.DIR_CLASS = BaseDir
        self.PATH_CLASS = BasePath
        self.DIRS_CLASS = BaseDirs
        self.PATHS_CLASS = BasePaths

        self.Dirs = self.Objs # Make an Alias

        for D in given_Dirs:
            self._add( D )
        for D in given_Paths:
            self._add( D )
        
        self.type_dir = False
        self.type_path = False
        self.type_dirs = True
        self.type_paths = False

    @staticmethod
    def is_Dirs( Object: Any ) -> bool:

        """returns boolean if Object is a Dir"""
        return isinstance( Object, BaseDirs )

    def join_Dir( self, Dir_inst: BaseDir ) -> BasePaths:

        """Joins Dir_inst to each Dir/Path contained in the Object"""

        Paths_inst = self.PATHS_CLASS( **self.inherited_kwargs )

        for DirPath in self:

            if DirPath.type_path:
                Paths_inst._add( Dir_inst.join_Path( DirPath ) )
            
            if DirPath.type_dir:
                Paths_inst._add( Dir_inst.join_Dir( DirPath ) )

        return Paths_inst

    def merge( self, other_Dirs: Any ) -> None:

        """add all Dir objects from another Dirs instance to self"""

        for Dir_inst in other_Dirs:
            self._add( Dir_inst )

    def export_strings( self ) -> List[str]:

        """Returns all the paths of each Dir/Path contained"""

        return [ O.path for O in self ]

    @do.dirs_wrap( 'create', track_success=True )
    def create( self, *args, **kwargs ):
        pass

    @do.dirs_wrap( 'remove', track_success=True )
    def remove( self, *args, **kwargs ):
        pass


class BasePaths( BaseDirs ):

    def __init__ ( self, *args, **kwargs ):

        BaseDirs.__init__( self, **kwargs )
        self.Paths = self.Objs # Make an Alias

        self.DIR_CLASS = BaseDir
        self.PATH_CLASS = BasePath
        self.DIRS_CLASS = BaseDirs
        self.PATHS_CLASS = BasePaths

        self.type_dir = False
        self.type_path = False
        self.type_dirs = False
        self.type_paths = True

    @staticmethod
    def is_Paths( Object: Any ) -> bool:

        """returns boolean if Object is a Dir"""
        return isinstance( Object, BasePaths )

    def get_rels( self, Dir_inst ) -> BasePaths:

        """Given a Dir object, find the relative Paths from Dir to the Paths"""

        Paths_inst = self.PATHS_CLASS( **self.inherited_kwargs )
        for P in self:
            Paths_inst._add( P.get_rel( Dir_inst ) )

        return Paths_inst

   