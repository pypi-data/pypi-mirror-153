# pylint: disable=too-many-lines
# pylint: disable=too-many-branches
# pylint: disable=line-too-long
# pylint: disable=bare-except
# pylint: disable=unused-import
"""
    Contains the general methods for manipulating files.
"""

# import json
# import shutil
# import time
# import json
# import re
# from pathlib import Path
import time
import json
import patoolib
from datetime import timezone
from datetime import datetime
import gzip
import zipfile
import os
import io
import shutil
import traceback
from threading import Thread
import logging

# import ftputil
# from secure_delete import secure_delete
import colemen_string_utils as csu
import utils.dir as directory
# import utils.resources
# import utils.dir as dirUtils
# from utils.dir import create as create_dir
import utils.objectUtils as obj
from utils import file
# import utils.file_read as read
# import utils.file_write as write
# import utils.file_search as search
# import utils.file_convert as convert
# import utils.file_image as image
# import utils.exiftool as exiftool
# from utils.dir import get_folders_ftp
# import utils.string_utils as strUtils


def decompress_zip_file(file_path,dst=None,**kwargs):
    '''
        Decompress a zip file and optionally decompress all nested zip files.

        ----------

        Arguments
        -------------------------
        `file_path` {string}
            The path to the zip file to decompress.
        [`dst`] {string}
            The destination path for the extraction.
            If not provided, it will be extracted in place.

        Keyword Arguments
        -------------------------
        [`recursive`=True] {bool}
            if True, it will decompress all nested zip files.
            otherwise it will only decompress the first set of zip files it finds.

        [`delete_after`=False] {bool}
            If True, the zip file will be deleted after its contents are extracted.

        Return {bool}
        ----------------------
        True upon success, false otherwise.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 03\25\2022 09:39:08
        `memberOf`: file_compression
        `version`: 1.0
        `method_name`: decompress_all_zip_files
        # @xxx [03\25\2022 09:54:50]: documentation for decompress_all_zip_files
    '''
    recursive = obj.get_kwarg(["recursive"], True, (bool), **kwargs)
    delete_after = obj.get_kwarg(["delete after"], False, (bool), **kwargs)

    file_data = file.get_data(file_path)
    if file_data:
        if dst is None:
            dst = f"{file_data['dir_path']}/{file_data['name_no_ext']}"

        if recursive is True:
            decompress_single_zip_file(file_data['file_path'],dst,delete_after=delete_after)
            decompress_all_zip_files(dst,delete_after=delete_after)
            return True
        else:
            decompress_single_zip_file(file_data['file_path'],f"{file_data['dir_path']}/{file_data['name_no_ext']}",delete_after=delete_after)
            return True
    return False

def decompress_all_zip_files(start_path,**kwargs):
    '''
        Finds and decompresses all zip files in the start_path directory.

        ----------

        Arguments
        -------------------------
        `start_path` {string}
            The directory to search for zip files in.

        Keyword Arguments
        -------------------------
        [`recursive`=True] {bool}
            if True, it will decompress all nested zip files.
            otherwise it will only decompress the first set of zip files it finds.

        [`delete_after`=False] {bool}
            If True, the zip file will be deleted after its contents are extracted.

        Return {type}
        ----------------------
        return_description

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 03\25\2022 09:39:08
        `memberOf`: file_compression
        `version`: 1.0
        `method_name`: decompress_all_zip_files
        # @xxx [03\25\2022 09:54:50]: documentation for decompress_all_zip_files
    '''

    recursive = obj.get_kwarg(["recursive"], True, (bool), **kwargs)
    delete_after = obj.get_kwarg(["delete after"], False, (bool), **kwargs)

    if recursive is True:
        cycle = True
        cycle_count = 0
        extracted = []
        while(cycle):
            cycle_count += 1
            if cycle_count > 100:
                print("Maximum recursive depth of 100 zip files reached.")
                return None
            zips = file.get_files(start_path,extension=["zip","rar"],show_count=False)
            zips = _filter_extracted(zips,extracted)
            if len(zips) == 0:
                cycle = False
            else:
                # print(f"Zip files found: {len(zips)}")
                for zf in zips:
                    dst = f"{zf['dir_path']}/{zf['name_no_ext']}"
                    if directory.exists(dst) is False:
                        directory.create(dst)

                    decompress_single_zip_file(zf['file_path'],dst,delete_after=delete_after)
                    extracted.append(zf['file_path'])
    else:
        zips = file.get_files(start_path,extension="zip",show_count=False)
        for zf in zips:
            decompress_single_zip_file(zf['file_path'],f"{zf['dir_path']}/{zf['name_no_ext']}",delete_after=delete_after)





def _filter_extracted(files,extracted):
    '''
        Filters a list of files so only indices whos "file_path" is not in the extracted
        list are kept.

        This is utility method used by decompress_all_zip_files.

        ----------

        Arguments
        -------------------------
        `files` {list}
            A list of file dicts each with the "file_path" key
        `extracted` {list}
            A list of file paths that have already been extracted.

        Return {list}
        ----------------------
        A list of file dicts that have do not match anything in the extracted list.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 03\25\2022 10:09:33
        `memberOf`: file_compression
        `version`: 1.0
        `method_name`: _filter_extracted
        # @xxx [03\25\2022 10:12:04]: documentation for _filter_extracted
    '''

    new_files = []
    for zf in files:
        if zf['file_path'] not in extracted:
            new_files.append(zf)
    return new_files

def decompress_single_zip_file(src,dst=None,**kwargs):
    '''
        Decompress a single zip or rar file.

        ----------

        Arguments
        -------------------------
        `src` {string}
            The file path to the zip/rar file that will be decompressed.

        [`dst`] {string}
            The path to where the extracted contents will be placed.
            If not provided, it will be extracted in place.
        Keyword Arguments
        -------------------------
        [`delete_after`=False] {bool}
            If True, the zip file will be deleted after its contents are extracted.

        Return {bool}
        ----------------------
        True upon success, false otherwise.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 03\25\2022 09:42:13
        `memberOf`: file_compression
        `version`: 1.0
        `method_name`: decompress_single_zip_file
        # @xxx [03\26\2022 10:14:59]: documentation for decompress_single_zip_file
    '''
    delete_after = obj.get_kwarg(["delete after"], False, (bool), **kwargs)
    valid_ext = ['.zip','.rar']

    src_data = file.get_data(src)
    if src_data['extension'] not in ['.zip','.rar']:
        print(f"Invalid zip extension {src_data['extension']}.")
        print(f"Supported extensions: {valid_ext}")
        return False


    if dst is None:
        dst = f"{src_data['dir_path']}\\{src_data['name_no_ext']}"


    src = csu.format.file_path(src)
    dst = csu.format.file_path(dst)
    directory.create(dst)

    src_ext = file.get_ext(src)

    if src_ext in [".zip"]:
        try:
            with zipfile.ZipFile(src, 'r') as zip_ref:
                zip_ref.extractall(dst)
        except:
            print("failed to decompress zip file")
            return False
        else:
            if delete_after:
                os.remove(src)
            return True

    if src_ext in [".rar"]:
        try:
            patoolib.extract_archive(src,verbosity=-1,outdir=dst,interactive=False)
        except:
            print("failed to unpack rar.")
            return False
        else:
            if delete_after:
                os.remove(src)
            return True

