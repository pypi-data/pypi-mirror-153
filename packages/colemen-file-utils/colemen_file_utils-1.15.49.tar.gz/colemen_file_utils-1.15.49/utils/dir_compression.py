# pylint: disable=too-many-lines
# pylint: disable=too-many-locals
# pylint: disable=too-many-branches
# pylint: disable=bare-except
# pylint: disable=line-too-long
'''
    Contains the general methods for manipulating directories.
'''

# import json
# from re import search
import re
# import json
# from threading import Thread
# import patoolib
import shutil
import utils.objectUtils as obj
import utils.dir as dirUtils
import utils.file as file
# import utils.resources


# logger = logging.getLogger(__name__)

def create_zip(src,dst,**kwargs):
    '''
        Create a zip archive of the directory provided.

        ----------

        Arguments
        -------------------------
        `src` {string}
            The file path to the directory to be archived.

        `dst` {str}
            The file path to the zip file to be created.\
            `WITHOUT AN EXTENSION`

        Keyword Arguments
        -------------------------
        [`delete_after`=False] {bool}
            If True, the source directy will be deleted after the zip is created.
            
        [`overwrite`=True] {bool}
            If False, it will skip creating the archive.

        Return {void}
        ----------------------
        returns nothing

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 03\26\2022 11:15:20
        `memberOf`: dir_compression
        `version`: 1.0
        `method_name`: create_zip
        # @xxx [03\26\2022 11:31:44]: documentation for create_zip
    '''
    
    delete_after = obj.get_kwarg(["delete after"], False, (bool), **kwargs)
    overwrite = obj.get_kwarg(["overwrite"], True, (bool), **kwargs)
    
    if file.exists(dst):
        if overwrite is False:
            return True
    
    try:
        result = shutil.make_archive(dst, 'zip', src)
    except:
        print("Failed to create zip archive.")
        return False
    else:
        if result == dst:
            if delete_after:
                dirUtils.delete(src)
            return True