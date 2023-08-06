import functools
import dir_ops as do
import py_starter as ps

def base_instance_method(method):

    """instance methods call the corresponding staticmethod 
    Example: Dir_instance.exists(*,**) calls Dir.exists_dir( Dir_instance.path,*,** )   
    """

    @functools.wraps(method)
    def wrapper( self, *called_args, **called_kwargs):

        new_method_name = method.__name__ + self.STATIC_METHOD_SUFFIX
        return self.get_attr( new_method_name )( self.path, *called_args, **called_kwargs )
        
    return wrapper

def inherited_instance_method(method):

    """instance methods call the corresponding staticmethod 
    Example: Dir_instance.exists(*,**) calls Dir.exists_dir( Dir_instance.path,*,** )   """

    @functools.wraps(method)
    def wrapper( self, *called_args, **called_kwargs):

        new_method_name = method.__name__ + self.STATIC_METHOD_SUFFIX
        instance_args = [ self.get_attr( attr ) for attr in self.INSTANCE_METHOD_ATTS ]

        return self.get_attr( new_method_name )( *instance_args, *called_args, **called_kwargs )
      
    return wrapper

def dirs_wrap( method_name, track_success = False ):

    def dirs_gen( method ):

        @functools.wraps( method )
        def wrapper( self, *args, **kwargs ):

            valid = True
            for DirPath in self:
                value = DirPath.get_attr( method_name )( *args, **kwargs )

                if value == False:
                    valid = False

            if track_success:
                return valid

        return wrapper

    return dirs_gen
  

###

def to_from_wrapper_factory( method, action_str, self, *args, override: bool = False, print_off: bool = False, 
                    Destination = None, destination = '', 
                    overwrite: bool = False,
                    **kwargs  ):

    if Destination == None:
        if self.type_path:
            Destination = do.Path( destination )
        if self.type_dir:
            Destination = do.Dir( destination )


    ######  Insert special instructions
    if action_str == 'download' or action_str == 'copy' or action_str == 'rename':
        Destination.create_parents()
    
    ######
    if not override:
        do.print_to_from( True, action_str, str(self), str(Destination) )
        override = ps.confirm_raw( string = '' )

    if override:
        ###### Check for conflicting destination locations
        if action_str == 'download' or action_str == 'copy' or action_str == 'rename':
            if self.exists() and Destination.exists():
                if not overwrite:
                    print ('ERROR: Destination ' +str(Destination)+ ' already exists. Pass "overwrite=True" to overwrite existing file.')
                    return False
                else:
                    Destination.remove()

        # perform the actual method        
        do.print_to_from( print_off, action_str, str(self), str(Destination) )

        if method( self, *args, destination = Destination.path, override=override, print_off=print_off, **kwargs ):
            return True
        else:
            do.print_to_from( True, action_str, str(self), str(Destination) )
            print ('ERROR: could not complete ' + action_str)

    return False



def download_wrap( method ):

    @functools.wraps( method )
    def wrapper( self, *args, **kwargs ):
        return to_from_wrapper_factory( method, 'download', self, *args, **kwargs )

    return wrapper

def upload_wrap( method ):

    @functools.wraps( method )
    def wrapper( self, *args, **kwargs ):
        return to_from_wrapper_factory( method, 'upload', self, *args, **kwargs )

    return wrapper

def copy_wrap( method ):

    @functools.wraps( method )
    def wrapper( self, *args, **kwargs ):
        return to_from_wrapper_factory( method, 'copy', self, *args, **kwargs )

    return wrapper

def rename_wrap( method ):

    @functools.wraps( method )
    def wrapper( self, *args, **kwargs ):
        return to_from_wrapper_factory( method, 'rename', self, *args, **kwargs )

    return wrapper


def remove_wrap( method ):

    @functools.wraps( method )
    def wrapper( self, *args, **kwargs ):
        return to_from_wrapper_factory( method, 'remove', self, *args, **kwargs )

    return wrapper


def create_wrap( method ):

    @functools.wraps( method )
    def wrapper( self, *args, **kwargs ):
        return to_from_wrapper_factory( method, 'create', self, *args, **kwargs )

    return wrapper


###

def get_size_wrap( method ):

    @functools.wraps( method )
    def wrapper( self, *args, conversion=None, **kwargs ):

        size_bytes = method( self, *args, conversion=None, **kwargs )
        
        size, size_units = do.convert_bytes( size_bytes, conversion=conversion )
        self.size = size
        self.size_units = size_units

        return size, size_units

    return wrapper

def get_mtime_wrap( method ):

    @functools.wraps( method )
    def wrapper( self, *args, **kwargs ):

        mtime = method( self, *args, **kwargs )
        self.mtime = mtime

        return mtime

    return wrapper

