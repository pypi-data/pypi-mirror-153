DEBUG = False

from .support_functions import *
from .decorators import *
from .base_dir_ops import *
from .local_dir_ops import *
from .remote_dir_ops import *
import os

_Dir = Dir( os.path.abspath( __file__ ) ).ascend()   #Dir that contains the package 
_src_Dir = _Dir.ascend()                                  #src Dir that is one above
_repo_Dir = _src_Dir.ascend()                    
_cwd_Dir = Dir( get_cwd() )

