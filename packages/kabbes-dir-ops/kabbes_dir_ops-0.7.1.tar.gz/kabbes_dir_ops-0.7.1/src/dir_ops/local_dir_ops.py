from __future__ import annotations
import shutil
import os
import pathlib
import datetime
import subprocess
import platform
from typing import List, Any, Tuple, Callable

import dir_ops as do
import py_starter as ps


class Dir ( do.BaseDir ) :


    def __init__ ( self, *args, **kwargs ):

        do.BaseDir.__init__( self, *args, **kwargs )
        self.DIR_CLASS = Dir
        self.PATH_CLASS = Path
        self.DIRS_CLASS = Dirs
        self.PATHS_CLASS = Paths

    
    @staticmethod
    def open_dir( dir ) -> None:

        """Opens the dir in the file explorer """

        if platform.system() == 'Windows':
            os.startfile(dir)

        elif platform.system() == 'Darwin':
            subprocess.call(['open', dir])


    @staticmethod
    def exists_dir( dir: str, *args, **kwargs ) -> bool:
        assert os.path.exists( dir )

    @staticmethod
    def remove_dir( dir: str, *args, **kwargs ) -> None:
        shutil.rmtree(dir)

    @staticmethod
    def create_dir( dir: str, *args, **kwargs ) -> None:
        os.mkdir( dir )

    @staticmethod
    def copy_dir( dir: str, *args, destination: str = '', **kwargs) -> None:
        shutil.copytree( dir, destination )

    @staticmethod
    def list_files_dir( dir: str ) -> List[str]:

        contents = os.listdir( dir )

        for i in range(len(contents)-1,-1,-1):
            if not os.path.isfile( dir + '/' + contents[i] ):
                del contents[i]

        return contents

    @staticmethod
    def list_subfolders_dir( dir: str) -> List[str]:

        contents = os.listdir( dir )

        for i in range(len(contents)-1,-1,-1):
            if not os.path.isdir( dir + '/' + contents[i] ):
                del contents[i]

        return contents

    @staticmethod
    def get_size_dir( dir: str, *args, **kwargs ) -> float:

        self = Path( path = dir, **self.inherited_kwargs )
        Paths_inst = self.list_contents_Paths( block_dirs=True, block_paths=False )

        bytes = 0
        for Path_inst in Paths_inst:
            Path_inst.get_size( conversion = None )
            bytes += Path_inst.size 

        return bytes         


class Path( Dir, do.BasePath ):

    """
    Inherits from the Dir class found in Dir.py
    Path (uppercase P) is a Path class, path (lowercase P) is a string with file absolute path
    """

    def __init__( self, *args, **kwargs ):

        do.Dir.__init__( self, *args, **kwargs )
        do.BasePath.__init__( self, *args, **kwargs )        
        self.DIR_CLASS = Dir
        self.PATH_CLASS = Path
        self.DIRS_CLASS = Dirs
        self.PATHS_CLASS = Paths

    @staticmethod
    def exists_path( path: str, *args, **kwargs ) -> bool:
        assert os.path.exists( path )

    @staticmethod
    def copy_path( path: str, *args, destination: str = '', **kwargs ) -> None:
        shutil.copyfile(path, destination)

    @staticmethod
    def create_path( path: str, *args, **kwargs) -> None:

        self = Path( path )        
        if not self.write( string = '' ):
            assert False

    @staticmethod
    def remove_path(path: str, *args, **kwargs) -> None:
        os.remove(path)

    @staticmethod
    def rename_path( path, *args, destination: str = '', **kwargs) -> None:
        os.rename( path, destination )

    @staticmethod
    def get_size_path( path, *args, **kwargs ) -> float:
        return os.stat( path ).st_size

    @staticmethod
    def get_mtime_path( path, *args, **kwargs ) -> datetime.datetime:

        """get the time of modification as a datetime object"""

        mtime = pathlib.Path(path).stat().st_mtime
        dt = datetime.datetime.fromtimestamp( mtime )
        return dt

    @staticmethod
    def read_path( path, **kwargs ) -> Any:
        """reads from a text file at path, read py_starter.read_text_file() for kwargs """

        return ps.read_text_file( path, **kwargs )

    @staticmethod
    def write_path( path, **kwargs ) -> None:
        """writes to a text file at path, read py_starter.write_text_file() for kwargs """

        ps.write_text_file( path, **kwargs )

    @do.inherited_instance_method
    def import_module( self, *args, **kwargs) -> Callable :
        pass
    
    @staticmethod
    def import_module_path( path, *args, **kwargs ) -> Callable:
        return ps.import_module_from_path( path, **kwargs )


class Dirs( do.BaseDirs ):


    def __init__ ( self, *args, **kwargs ):

        do.BaseDirs.__init__( self, *args, **kwargs )
        self.DIR_CLASS = Dir
        self.PATH_CLASS = Path
        self.DIRS_CLASS = Dirs
        self.PATHS_CLASS = Paths


class Paths( Dirs, do.BasePaths ):

    def __init__( self, *args, **kwargs ):

        Dirs.__init__( self )
        do.BasePaths.__init__( self, *args, **kwargs )
        self.DIR_CLASS = Dir
        self.PATH_CLASS = Path
        self.DIRS_CLASS = Dirs
        self.PATHS_CLASS = Paths


