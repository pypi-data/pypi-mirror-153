# pylint: disable=bare-except
# pylint: disable=line-too-long

'''
    Module for file conversions
'''

# import subprocess
# import json
# import shutil
import os
from threading import Thread

import ffmpeg
from PIL import Image, UnidentifiedImageError
# import re
# from pathlib import Path

# import utils.file_read as read
# import colemen_string_utils as csu
# import facades.string_facade as csu

import utils.file_utils as f
import utils.dict_utils as obj
import utils.string_utils as csu

# from utils.dict_utils.dict_utils import get_kwarg as obj.get_kwarg
# from utils.file_utils.file_utils import exists as f.exists
# from utils.file_utils.file_utils import delete as f.delete
# from utils.file_utils.file_utils import get_name_no_ext as f.get_name_no_ext
# from utils.file_utils.file_utils import gen_path_list as f.gen_path_list
# from utils.file_utils.file_image import get_meta as f.get_meta
# from utils.file_utils.file_image import save_file_obj as f.save_file_obj
# from utils.file_utils.file_utils import get_files as f.get_files
# from utils.file_utils.file_utils import get_ext as f.get_ext
# from utils.string_utils.string_format import extension as csu.extension



def to_mp4(input_value, **kwargs):
    '''
        Convert an audio/video file to mp4

        ----------

        Arguments
        -------------------------
        `input_value` {str|list}
            The path or list of paths to convert.

        Keyword Arguments
        -------------------------
        [`delete_after`=False] {bool}
            If True, the original file is deleted after conversion.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12\\21\\2021 17:32:39
        `memberOf`: file_convert
        `version`: 1.0
        `method_name`: to_mp4
    '''

    delete_original_after = obj.get_kwarg(['delete after'], False, (bool), **kwargs)

    input_list = input_value
    if isinstance(input_value, (str)):
        input_list = [input_value]

    for path in input_list:
        if f.exists(path) is False:
            print(f"Could not find file: {path}")
            continue

        output_path = f"{os.path.dirname(path)}/{f.get_name_no_ext(path)}.mp4"
        try:
            ffmpeg.input(path).output(output_path, vcodec='copy').run(overwrite_output=True)
            if delete_original_after:
                f.delete(path)
        except:
            print(f"There was an error converting: {path}")


def to_mp3(input_value, **kwargs):
    '''
        Convert an audio/video file to mp3

        ----------

        Arguments
        -------------------------
        `input_value` {str|list}
            The path or list of paths to convert.

        Keyword Arguments
        -------------------------
        [`delete_after`=False] {bool}
            If True, the original file is deleted after conversion.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-21-2021 17:29:36
        `memberOf`: file_convert
        `version`: 1.0
        `method_name`: to_mp3
    '''
    delete_original_after = obj.get_kwarg(['delete after'], False, (bool), **kwargs)

    input_list = input_value
    if isinstance(input_value, (str)):
        input_list = [input_value]

    for path in input_list:
        if f.exists(path) is False:
            print(f"Could not find file: {path}")
            continue

        output_path = f"{os.path.dirname(path)}/{f.get_name_no_ext(path)}.mp3"
        try:
            ffmpeg.input(path).output(output_path, vcodec='copy').run(overwrite_output=True)
            if delete_original_after:
                f.delete(path)
        except:
            print(f"There was an error converting: {path}")

def to_webp(src_path,**kwargs):
    '''
        Convert an image or list of images to webp.

        ----------

        Arguments
        -------------------------
        `src_path` {str|list}
            The path or list of paths to convert.

        Keyword Arguments
        -------------------------
        [`delete_after`=False] {bool}
            If True, the original file is deleted after conversion.

        Return {list}
        ----------------------
        A list of paths that were converted to webp.\n
        If shit happens, the list will be empty.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 01-08-2022 09:21:10
        `memberOf`: file_convert
        `version`: 1.0
        `method_name`: to_webp
    '''
    delete_original_after = obj.get_kwarg(['delete after'], False, (bool), **kwargs)
    outputs = []
    src_list = f.gen_path_list(src_path)
    
    for path in src_list:
        if f.exists(path) is False:
            print(f"Could not find: {path}")
        # print(f"meta_data: {meta_data}")
        output_path = _convert_image(path, "webp")
        if f.exists(output_path):
            outputs.append(output_path)
            copy_meta_data(path,output_path)
            if delete_original_after is True:
                if output_path != path:
                    f.delete(path)
            
            
    return outputs

def copy_meta_data(src_path,dst_path):
    dst_data = f.get_meta(dst_path)
    src_data = f.get_meta(src_path)
    # kws = f.image.get_keywords(src_data)
    # print(f"kws: ",kws) 
    dst_data['meta_data']['XMP:Subject'] = src_data['meta_data']['XMP:Subject']
    f.save_file_obj(dst_data)

def to_jpg(src_path,dst_path=None,**kwargs):
    '''
        Convert an image or list of images to jpg.

        ----------

        Arguments
        -------------------------
        `src_path` {str|list}
            The path or list of paths to convert.

        Keyword Arguments
        -------------------------
        [`delete_after`=False] {bool}
            If True, the original file is deleted after conversion.

        Return {list}
        ----------------------
        A list of paths that were converted to jpg.\n
        If shit happens, the list will be empty.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 01-08-2022 09:21:10
        `memberOf`: file_convert
        `version`: 1.0
        `method_name`: to_jpg
    '''
    delete_original_after = obj.get_kwarg(['delete after'], False, (bool), **kwargs)
    outputs = []
    src_list = f.gen_path_list(src_path)
    
    for path in src_list:
        if f.exists(path) is False:
            print(f"Could not find: {path}")
            
        output_path = _convert_image(path, "jpg",dst_path)
        if f.exists(output_path):
            outputs.append(output_path)
            if delete_original_after is True:
                if output_path != path:
                    f.delete(path)

    return outputs

def thread_to_webp(file_path,delete_after=False):
    return to_webp(file_path,delete_after=delete_after)

def dir_to_webp(dir_path,**kwargs):
    '''
        Converts all images within the dir_path to webp.

        ----------

        Arguments
        -------------------------
        `dir_path` {str}
            The directory to search within.

        Keyword Arguments
        -------------------------
        [`delete_after`=False] {bool}
            if True, the original image will be deleted after conversion.

        [`recursive`=True] {bool}
            if False it will not search for images within sub directories.
            
        [`extensions`=['images]] {str|list}
            A list of image extensions to convert, if not provided it will convert these:
                bmp,dds,dib,eps,gif,icns,ico,im,jpg,jpeg,jpeg 2000,msp,pcx,png,ppm,sgi,spider,tga,tiff,xbm

        Return {list}
        ----------------------
        A list of paths that were converted to webp.\n
        If shit happens, the list will be empty.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 01-09-2022 15:05:23
        `memberOf`: file_convert
        `version`: 1.0
        `method_name`: dir_to_webp
    '''
    delete_original_after = obj.get_kwarg(['delete after'], False, (bool), **kwargs)
    extension_array = obj.get_kwarg(['extensions', 'ext', 'extension'], ['images'], (str, list), **kwargs)
    recursive = obj.get_kwarg(['recursive', 'recurse'], True, bool, **kwargs)
    images = f.get_files(dir_path, recursive=recursive, extensions=extension_array)
    if len(images) < 500:
        threads = []
        for img in images:
            thread = Thread(target=thread_to_webp, args=(img['file_path'],delete_original_after))
            threads.append(thread)
        for th in threads:
            th.start()
    else:
        return to_webp(images,delete_after=delete_original_after)

def dir_to_jpg(dir_path,**kwargs):
    '''
        Converts all images within the dir_path to jpg.

        ----------

        Arguments
        -------------------------
        `dir_path` {str}
            The directory to search within.

        Keyword Arguments
        -------------------------
        [`delete_after`=False] {bool}
            if True, the original image will be deleted after conversion.

        [`recursive`=True] {bool}
            if False it will not search for images within sub directories.
            
        [`extensions`=['images]] {str|list}
            A list of image extensions to convert, if not provided it will convert these:
                bmp,dds,dib,eps,gif,icns,ico,im,jpg,jpeg,jpeg 2000,msp,pcx,png,ppm,sgi,spider,tga,tiff,xbm

        Return {list}
        ----------------------
        A list of paths that were converted to jpg.\n
        If shit happens, the list will be empty.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 01-09-2022 15:05:23
        `memberOf`: file_convert
        `version`: 1.0
        `method_name`: dir_to_jpg
    '''
    delete_original_after = obj.get_kwarg(['delete after'], False, (bool), **kwargs)
    extension_array = obj.get_kwarg(['extensions', 'ext', 'extension'], ['images'], (str, list), **kwargs)
    recursive = obj.get_kwarg(['recursive', 'recurse'], True, bool, **kwargs)
    images = f.get_files(dir_path, recursive=recursive, extensions=extension_array,ignore=['.jpg'])
    return to_jpg(images,delete_after=delete_original_after)

def has_transparency(img):
    if img.mode == "P":
        transparent = img.info.get("transparency", -1)
        for _, index in img.getcolors():
            if index == transparent:
                return True
    elif img.mode == "RGBA":
        extrema = img.getextrema()
        if extrema[3][0] < 255:
            return True

    return False

def _convert_image(src_path,output_ext,dst_path=None):
    oext = f.get_ext(src_path)
    extension = csu.extension(output_ext)

    if oext == extension:
        return src_path
    
    if f.exists(src_path) is False:
        print(f"Could not find: {src_path}")
        return False
    else:
        if dst_path is None:
            dst_path = f"{os.path.dirname(src_path)}/{f.get_name_no_ext(src_path)}.{extension}"
        # print(f"output_path: {output_path}")
        try:
            im = Image.open(src_path)
            convert_to = 'RGB'
            if has_transparency(im) is True:
                convert_to = "RGBA"
            if extension == "jpg":
                extension ="jpeg"
                convert_to = "RGB"
            im = im.convert(convert_to)
            im.save(dst_path,extension)
            return dst_path
        except UnidentifiedImageError:
            print(f"Skipping file, could not convert: {src_path}.")
            return False

