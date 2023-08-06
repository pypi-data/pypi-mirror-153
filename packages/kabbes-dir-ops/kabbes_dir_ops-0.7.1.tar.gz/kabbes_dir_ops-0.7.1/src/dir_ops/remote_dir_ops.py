import dir_ops as do
import py_starter as ps

class RemoteDir ( do.BaseDir ) :

    def __init__ ( self, *args, **kwargs ):

        do.BaseDir.__init__( self, *args, **kwargs )
        self.DIR_CLASS = RemoteDir
        self.PATH_CLASS = RemotePath
        self.DIRS_CLASS = RemoteDirs
        self.PATHS_CLASS = RemotePaths

    @do.upload_wrap
    @ps.try_operation_wrap( debug = do.DEBUG )   
    @do.inherited_instance_method
    def upload( self, *args, **kwargs ):
        pass

    @staticmethod
    def upload_dir( *args, **kwargs ):
        assert False

    @do.download_wrap
    @ps.try_operation_wrap( debug = do.DEBUG )   
    @do.inherited_instance_method
    def download( self, *args, **kwargs ):
        pass
    
    @staticmethod
    def download_dir( *args, **kwargs ):
        assert False
   


class RemotePath( RemoteDir, do.BasePath ):

    def __init__( self, *args, **kwargs ):

        RemoteDir.__init__( self, *args, **kwargs )
        do.BasePath.__init__( self, *args, **kwargs )
        self.DIR_CLASS = RemoteDir
        self.PATH_CLASS =  RemotePath
        self.DIRS_CLASS = RemoteDirs
        self.PATHS_CLASS = RemotePaths

    @staticmethod
    def upload_path( *args, **kwargs ):
        assert False

    @staticmethod
    def download_path( *args, **kwargs ):
        assert False


class RemoteDirs( do.BaseDirs ):

    def __init__( self, *args, **kwargs ):

        do.BaseDirs.__init__( self, *args, **kwargs )
        self.DIR_CLASS = RemoteDir
        self.PATH_CLASS =  RemotePath
        self.DIRS_CLASS = RemoteDirs
        self.PATHS_CLASS = RemotePaths




class RemotePaths( RemoteDirs, do.BasePaths ):

    def __init__( self, *args, **kwargs ):

        RemoteDirs.__init__( self )
        do.Paths.__init__( self, *args, **kwargs )
        self.DIR_CLASS = RemoteDir
        self.PATH_CLASS =  RemotePath
        self.DIRS_CLASS = RemoteDirs
        self.PATHS_CLASS = RemotePaths

