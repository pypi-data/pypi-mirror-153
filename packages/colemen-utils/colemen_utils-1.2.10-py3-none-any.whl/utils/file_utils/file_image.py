# pylint: disable=bare-except
# pylint: disable=line-too-long

'''
    A module of utility methods used for manipulating image files.

    ----------

    Meta
    ----------
    `author`: Colemen Atwood
    `created`: 06-04-2022 10:58:25
    `memberOf`: file_utils
'''

import time as _time
import os as _os
import re as _re
from typing import Union as _Union
from PIL import Image as _Image
import utils.file_utils as _f
import utils.dict_utils as _obj
import utils.string_utils as _csu
import utils.directory_utils as _dir


REGEX_TYPE = type(_re.compile('hello, world'))


def _parse_file_obj_list(file):
    '''
        The "file" provided is parsed to into an array of file objects.
        "file" being a super general term for a file_path, list of paths, list of dicts with "file_path" prop.

        ----------

        Arguments
        -------------------------
        `file` {string|list|dict}
            A file path, list of paths, a file_object dictionary or list of dictionaries.

        Return {list}
        ----------------------
        A list of file_objects (created by file.get_data())
        If nothing is found the list is empty.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 01-27-2022 10:24:49
        `memberOf`: file_image
        `version`: 1.0
        `method_name`: _parse_file_obj_list
    '''
    file_array = []
    if isinstance(file, (str)):
        if _f.exists(file):
            file_array.append(_f.get_data(file))

    if isinstance(file, (list)):
        for i in file:
            if isinstance(i, (str)):
                if _f.exists(i):
                    file_array.append(_f.get_data(i))
            if isinstance(i, (dict)):
                if 'file_path' in i:
                    file_array.append(i)

    if isinstance(file, (dict)):
        if 'file_path' in file:
            file_array = [file]

    return file_array

def _keywords_to_list(keywords,delimiter=",",**kwargs):
    # print(f"")
    to_snake_case = _obj.get_kwarg(['snake case'],True,(bool),**kwargs)
    new_keys = []
    # print(f"_keywords_to_list: {keywords} {type(keywords)}")


    if isinstance(keywords,(float,int)):
        new_keys.append(f"{keywords}")

    if isinstance(keywords,(str)):
        if len(keywords) == 0:
            return ''
        if delimiter in keywords:
            # print(f"_keywords_to_list - comma found in keywords: {keywords}")
            new_keys = keywords.split(delimiter)
        else:
            # print(f"_keywords_to_list - no delimiter found in keywords: {keywords}")
            new_keys = [keywords]

    if isinstance(keywords,(list)):
        # print(f"_keywords_to_list - keyswords is a list")
        if len(keywords) == 0:
            return ''

        for x in keywords:
            new_keys.extend(_keywords_to_list(x))

    # print(f"newlist: ",new_keys)
    newlist = list(set(new_keys))
    if to_snake_case is True:
        newlist = [_csu.to_snake_case(x) for x in newlist]

    return newlist

def gen_css_media_scales(src_path):
    sizes = [1600,1400,1200,992,768,576,480]
    for size in sizes:
        scale(src_path, (size, size), keep_proportion=True)

def scale(src_path:str,size:_Union[list,tuple],**kwargs):
    '''
        Scale an image to a new size.

        ----------

        Arguments
        -------------------------
        `src_path` {str}
            The path to the image to scale.

        `size` {list|tuple}
            A lsit or tuple [width,height]

        `keep_proportion` {bool}
            if False, it will not attempt to keep the images proportions.

        Return {None}
        ----------------------
        returns nothing.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-04-2022 13:11:55
        `memberOf`: file_image
        `version`: 1.0
        `method_name`: scale
        * @xxx [06-04-2022 13:14:03]: documentation for scale
    '''


    if isinstance(size,(list,tuple)):
        width = size[0]
        height = size[1]
    else:
        print("Size must be a list or tuple [width,height]")
        return False


    dst_path = _obj.get_kwarg(['dst_path'], False, (str), **kwargs)
    keep_proportion = _obj.get_kwarg(['keep_proportion'], True, (bool), **kwargs)

    size_tuple = (width,height)
    if keep_proportion is True:
        if width > height:
            size_tuple = (width,width)
        else:
            size_tuple = (height, height)

    file_data = _f.get_data(src_path)
    if dst_path is False:
        dst_path = f"{file_data['dir_path']}/{file_data['name_no_ext']}_{size_tuple[0]}x{size_tuple[1]}{file_data['extension']}"

    image = _Image.open(src_path)
    image.thumbnail(size_tuple, _Image.ANTIALIAS)
    image.save(dst_path)

def delete_all_keywords(files:list)->None:
    '''
        Remove all keywords from the files

        ----------

        Arguments
        -------------------------
        `files` {list}
            A list of file paths or file data dictionary's

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-04-2022 13:16:09
        `memberOf`: file_image
        `version`: 1.0
        `method_name`: delete_all_keywords
        * @xxx [06-04-2022 13:18:02]: documentation for delete_all_keywords
    '''


    file_array = _parse_file_obj_list(files)
    for file in file_array:
        if 'meta_data' not in file:
            file = get_meta(file)
        set_keywords(file)
        purge_original(file)

def delete_keyword(files,keywords='*',**kwargs):
    case_sensitive = _obj.get_kwarg(['case sensitive'],True,(bool),**kwargs)
    save = _obj.get_kwarg(['save'],False,(bool),**kwargs)
    needle_array = _keywords_to_list(keywords)
    update_array = []
    if len(needle_array) == 0:
        return False
    if needle_array[0] == "*":
        delete_all_keywords(files)
        return
    file_array = _parse_file_obj_list(files)
    for file in file_array:
        if 'meta_data' not in file:
            file = get_meta(file)
        kws = get_keywords(file)

        new_keys = []
        # print(f"kws: ",kws)
        for haystack in kws:
            haystack = f"{haystack}"
            for needle in needle_array:
                if isinstance(needle,(str)):
                    if case_sensitive is False:
                        try:
                            if needle.lower() != haystack.lower():
                                new_keys.append(haystack)
                        except AttributeError:
                            print(f"skipping haystack: {haystack}")
                    if case_sensitive is True:
                        if needle != haystack:
                            new_keys.append(haystack)
                        # else:
                        #     matchFound = True
        # _f.write.to_json("imgs.json",file)
        # exit()
        if len(new_keys) > 1:
            new_keys = list(set(new_keys))
        if len(kws) != len(new_keys):
            # print(f"total original keys: {len(kws)}")
            # print(f"total new_keys: {len(new_keys)}")
            file['meta_data']['XMP:Subject'] = new_keys
            file['meta_data']['IPTC:Keywords'] = new_keys
            update_array.append(file)
    if save is True:
        save_file_obj(update_array)
    return file_array
            # purge_original(file)

def add_keyword(files,keywords='',**kwargs):
    snake_case = _obj.get_kwarg(['snake case'],True,(bool),**kwargs)
    save = _obj.get_kwarg(['save'],False,(bool),**kwargs)

    file_array = _parse_file_obj_list(files)
    # print(f"add_keyword.keywords: ",keywords)
    keywords = _keywords_to_list(keywords,",",snake_case=snake_case)
    # print(f"add_keyword.keywords: ",keywords)
    # exit()
    update_array = []
    for file in file_array:
        if 'meta_data' not in file:
            file = get_meta(file)
        kws = get_keywords(file)
        new_keys = kws + keywords
        file['meta_data']['XMP:Subject'] = new_keys
        file['meta_data']['IPTC:Keywords'] = new_keys
        if len(kws) != len(new_keys):
            update_array.append(file)

    if save is True:
        save_file_obj(update_array)
    return file_array

def set_keywords(files,keywords='',**kwargs):
    '''
        Sets the keyword values on the file(s) provided.

        ----------

        Arguments
        -------------------------
        `files` {list|string|dict}
            A file path, list of paths, file object dictionary or list of dictionaries.

        `keywords` {list|string}
            A string of comma separated keywords or a list of keywords to add to the file.

        Keyword Arguments
        -------------------------
        [`save`=False] {bool}
            if True, the file is saved after its keywords are updated.

        [`snake_case`=False] {bool}
            format the keywords to be in snake case notation.

        Return {list}
        ----------------------
        The list of files with updated keywords.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 01-27-2022 11:08:05
        `memberOf`: file_image
        `version`: 1.0
        `method_name`: set_keywords
    '''
    save = _obj.get_kwarg(['save'],False,(bool),**kwargs)
    snake_case = _obj.get_kwarg(['snake case'],True,(bool),**kwargs)

    file_array = _parse_file_obj_list(files)
    keywords = _keywords_to_list(keywords,",",snake_case=snake_case)
    # exif_tool_array = []
    for file in file_array:
        print(f"updating file's keywords: {file['file_path']}")
        if 'meta_data' not in file:
            file = get_meta(file)
        file['meta_data']['XMP:Subject'] = keywords
        file['meta_data']['IPTC:Keywords'] = keywords
        # exif_tool_array.append([file['file_path'],keywords])

    if save is True:
        save_file_obj(files)

    return file_array

def save_file_obj(files):
    file_array = _parse_file_obj_list(files)

    with _f.exiftool.ExifTool(executable_=r"Z:\Structure\Archive\Programming Packages - Libraries\Python\colemen_file_utils\.venv\exiftool.exe") as et:
        for file in file_array:
            if 'meta_data' in file:
                print(f"save_file__obj.filePath: {file['file_path']}")
                et.set_tags(file['meta_data'],file['file_path'])

def tags_to_snakecase(files):
    file_array = _parse_file_obj_list(files)
    update_array = []
    for file in file_array:
        if 'meta_data' not in file:
            print("file missing meta_data")
            file = get_meta(file)
        # _f.write.to_json("result_array.json",file)

        # xmpTags = file['meta_data']['XMP:Subject']
        # iptcTags = file['meta_data']['IPTC:Keywords']
        if isinstance(file['meta_data']['XMP:Subject'],(str)):
            file['meta_data']['XMP:Subject'] = [file['meta_data']['XMP:Subject']]
        if isinstance(file['meta_data']['IPTC:Keywords'],(str)):
            file['meta_data']['IPTC:Keywords'] = [file['meta_data']['IPTC:Keywords']]

        tags = file['meta_data']['XMP:Subject'] + file['meta_data']['IPTC:Keywords']
        # print(f"tags: ",tags)
        new_tags = []
        for tag in tags:
            new_tags.append(_csu.to_snake_case(tag))
        if len(new_tags) > 1:
            new_tags = list(set(new_tags))
        file['meta_data']['XMP:Subject'] = new_tags
        file['meta_data']['IPTC:Keywords'] = new_tags
        update_array.append(file)

    save_file_obj(update_array)
    return update_array

def get_meta_only(file_path):
    meta_data = {}
    if isinstance(file_path,(list)) is False:
        file_path = [file_path]

    # paths_array = []
    # for path in file_path:
    #     if _f.exists(path):
    #         paths_array.append(path)

    # et = _f.exiftool.ExifTool(executable_=r"Z:\Structure\Archive\Programming Packages - Libraries\Python\colemen_file_utils\.venv\exiftool.exe")
    with _f.exiftool.ExifTool(executable_=r"Z:\Structure\Archive\Programming Packages - Libraries\Python\colemen_file_utils\.venv\exiftool.exe") as et:
        meta_data = et.get_metadata_batch(file_path)[0]
        if 'XMP:Subject' not in meta_data:
            meta_data['XMP:Subject'] = []
        if 'IPTC:Keywords' not in meta_data:
            meta_data['IPTC:Keywords'] = []
    return meta_data

def get_meta(files,force_update=False):
    result_array = []
    file_array = _parse_file_obj_list(files)
    # et = _f.exiftool.ExifTool(executable_=r"Z:\Structure\Archive\Programming Packages - Libraries\Python\colemen_file_utils\.venv\exiftool.exe")
    for file in file_array:
        file['file_path'] = _csu.file_path(file['file_path'],url=True)
        file['file_path_exif_copy'] = _csu.file_path(f"{file['file_path']}_original",url=True)

        if 'meta_data' not in file or force_update is True:
        # print(f"get_meta.file_path: {file['file_path']}")
            with _f.exiftool.ExifTool(executable_=r"Z:\Structure\Archive\Programming Packages - Libraries\Python\colemen_file_utils\.venv\exiftool.exe") as et:
                file['meta_data'] = et.get_metadata_batch([file['file_path']])[0]
                if 'XMP:Subject' not in file['meta_data']:
                    file['meta_data']['XMP:Subject'] = []
                if 'IPTC:Keywords' not in file['meta_data']:
                    file['meta_data']['IPTC:Keywords'] = []
        result_array.append(file)

    #     # file = _f.get_data(file_path)
    #     file['update_file'] = False
    #     # im = _Image.open(x['file_path'])
    #     info = IPTCInfo(file['file_path'], force=True)
    #     # print(info.__dict__.items())
    #     for k, v in info.__dict__.items():
    #         # print(f"k: {k}    ::::     v: {v}")
    #         if k == '_data':
    #             file['iptc_data'] = formatIPTCData(v)
    #     if 'iptc_data' not in file:
    #         file['iptc_data'] = {"Keywords": [], "Description": [], "Contact": []}
    #     result_array.append(file)

    if len(result_array) == 1:
        return result_array[0]
    return result_array

def purge_original(files):
    file_array = _parse_file_obj_list(files)
    for file in file_array:
        if 'meta_data' not in file:
            file = get_meta(file)
        if _f.exists(file['file_path_exif_copy']):
            _f.delete(file['file_path_exif_copy'])

def get_keywords(files):
    # print(f"")
    keywords = []
    file_array = _parse_file_obj_list(files)
    # print(f"get_keywords 1: ",keywords)
    for file in file_array:
        if 'meta_data' not in file:
            # print(f"get_keywords.meta_data not found.")
            file = get_meta(file)
        # print(f"xmpTags: {type(file['meta_data']['XMP:Subject'])}",file['meta_data']['XMP:Subject'])
        # print(f"IPTCTags: {type(file['meta_data']['IPTC:Keywords'])}",file['meta_data']['IPTC:Keywords'])
        xmpKeys = file['meta_data']['XMP:Subject']
        iptcKeys = file['meta_data']['IPTC:Keywords']
        if isinstance(xmpKeys,(list)) is False:
            xmpKeys = [xmpKeys]
        if isinstance(iptcKeys,(list)) is False:
            iptcKeys = [iptcKeys]

        for k in xmpKeys:
            if isinstance(k,(str)) is False:
                keywords.append(f"{k}")
            else:
                keywords.append(k)
        for k in iptcKeys:
            if isinstance(k,(str)) is False:
                keywords.append(f"{k}")
            else:
                keywords.append(k)
        # keywords.extend(xmpKeys)
        # keywords.extend(iptcKeys)


    # print(f"get_keywords: ",keywords)
    return keywords

def replace_keyword(files,needle,replace):
    '''
        Find and replace keyword(s) in the files.

        ----------

        Arguments
        -------------------------
        `files` {list|string|dict}
            A file path, list of paths, file object dictionary or list of dictionaries.

        `needle` {list|string}
            The keyword or list of keywords to replace.

        `replace` {string}
            What to replace the keyword with.

        Return {list}
        ----------------------
        The list of files with updated keywords.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 01-27-2022 11:12:23
        `memberOf`: file_image
        `version`: 1.0
        `method_name`: replace_keyword
    '''
    if isinstance(needle,(list)) is False:
        needle = [needle]
    file_array = _parse_file_obj_list(files)
    update_array = []
    for file in file_array:
        if 'meta_data' not in file:
            file = get_meta(file)
        kws = get_keywords(file)
        for ndl in needle:
            if ndl in kws:
                print(f"replacing {ndl} with {replace}")
                # kws.remove(ndl)
                # kws.append(replace)
                file = delete_keyword(file,ndl,save=False)[0]
                file = add_keyword(file,replace,save=False)[0]
                # file = set_keywords(file,kws,save=False)[0]
                update_array.append(file)
    if len(update_array) > 0:
        print(f"saving {len(update_array)} files.")
        save_file_obj(update_array)

    return file_array

def has_keyword(files,keywords,**kwargs):
    # Causes the search to reverse, so if the image does NOT have a tag, it is returned
    reverse = _obj.get_kwarg(['reverse'],False,(bool),**kwargs)
    keyword_array = _keywords_to_list(keywords,",",snake_case=False)
    file_array = _parse_file_obj_list(files)
    result_array = []

    for file in file_array:
        if 'meta_data' not in file:
            # print(f"file does not have meta_data: {file['file_path']}")
            file = get_meta(file)
        kws = get_keywords(file)
        # print(f"has_keyword.kws: ",kws)

        # reverse_match_found = True
        match_found = False
        for k in keyword_array:
            # if reverse is False:
            if k in kws:
                # print(f"File contains {k}: {file['file_path']}")
                match_found = True
                    # result_array.append(file)
            # if reverse is True:
            #     if k in kws:
            #         print(f"File does not contain {k}: {file['file_path']}")
            #         match_found = True
                    # result_array.append(file)
        if match_found is True and reverse is False:
            result_array.append(file)
        if match_found is False and reverse is True:
            result_array.append(file)

    # If we are only searching one file, return a boolean
    # if len(file_array) == 1 and len(result_array) == 1:
    #     return True
    # if len(file_array) == 1 and len(result_array) == 0:
    #     return False
    # if we are searching multiple files, we return an array of files with the keywords
    return result_array

def apply_keyword_synonyms(files,synonyms,**kwargs):
    '''
        Iterates the files provided, and applies synonyms if a matching key is found.

        ----------

        Arguments
        -------------------------
        `files` {list|string|dict}
            A file path, list of paths, file object dictionary or list of dictionaries.
        `synonyms` {dict}
            The synonym object should be organized like this:

            {'key':['synonym1','synonym2']}


        Return {list}
        ----------------------
        The list of files provided, with the synonyms added.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 01-27-2022 10:43:23
        `memberOf`: file_image
        `version`: 1.0
        `method_name`: apply_keyword_synonyms
    '''
    save = _obj.get_kwarg(['save'],True,(bool),**kwargs)
    # Prepare the files array for iteration and gather necessary info.
    files_array = _parse_file_obj_list(files)
    update_array = []
    # key_synonyms = synonyms
    update_array = []

    # If there are no files, just return the empty array.
    if len(files_array) == 0:
        return files_array

    for file in files_array:
        kws = _f.get_keywords(file)
        kws_hash_prime = _csu.to_hash(kws)
        if isinstance(kws,(list)) is False:
            kws = [kws]
        # new_tags = kws
        new_tags = apply_synonyms(kws,synonyms)
        # for key in kws:
            # # print(f"key: ",key)
            # if isinstance(key,(str)) is True:
            #     if key in key_synonyms:
            #         for k in key_synonyms[key]:
            #             if k not in new_tags:
            #             # if k not in kws and k not in new_tags:
            #                 new_tags.append(k)
        file['meta_data']['XMP:Subject'] = new_tags
        file['meta_data']['IPTC:Keywords'] = new_tags


        # print(f"kws_hash_prime: {kws_hash_prime}")
        # kws = cfu.file.image.get_keywords(file)
        kwsHash = _csu.to_hash(new_tags)
        # print(f"kwsHash:        {kwsHash}")

        # compare the original keyword hash to the new one
        # if they are not identical, that means new keywords
        # were added, so we add it to the update_array.
        if kws_hash_prime != kwsHash:
            # print(f"new tags found.")
            # file['meta_data']['XMP:Subject'] = kws
            # file['meta_data']['IPTC:Keywords'] = kws
            update_array.append(file)
            # print(f"file['meta_data']['XMP:Subject']: ",file['meta_data']['XMP:Subject'])
            # exit()

    # if any files need updating, then we save the data to the file..
    if len(update_array) > 0 and save is True:
        _f.save_file_obj(update_array)
    return files_array

def apply_synonyms(file_keys,synonyms):
    if len(file_keys) > 1:
        file_keys = list(set(file_keys))
    # file_keys_hash = _csu.to_hash(file_keys)
    added_keys = False
    new_file_keys = file_keys
    for k,v in synonyms.items():

        if k in file_keys or k in new_file_keys:
            new_keys = [x for x in v if x not in new_file_keys]
            if len(new_keys) > 0:
                added_keys = True
                print(f"k: {k}:{v}")
                new_file_keys.extend(new_keys)
                print(f"new_file_keys: {new_file_keys}")
                # print(f"")

    if len(new_file_keys) > 1:
        new_file_keys = list(set(new_file_keys))

    # new_file_keys_hash = _csu.to_hash(new_file_keys)
    # if new_file_keys_hash != file_keys_hash:
    if added_keys is True:
        return apply_synonyms(new_file_keys,synonyms)
    else:
        return new_file_keys

def auto_tag_by_folder_name(watch_path,**kwargs):
    '''
        Watch a directory of images and apply the folder name to the image(s) when they are moved.

        ----------

        Arguments
        -------------------------
        `watch_path` {str}
            The path to the directory that will be watched.

        Keyword Arguments
        -------------------------
        [`synonyms`=False] {dict}
            A dictionary of synonyms that will be applied if a matching keyword is found.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 02-05-2022 10:00:34
        `memberOf`: file_image
        `version`: 1.0
        `method_name`: auto_tag_by_folder_name
    '''
    print("auto_tag_by_folder_name")
    synonyms = _obj.get_kwarg(['synonyms'],False,(bool,dict),**kwargs)
    apply_current_tags = _obj.get_kwarg(['apply_current_tags'],False,(bool),**kwargs)
    print(f"Indexing images in {watch_path}")
    all_files = _f.get_files(watch_path, ext="images",include_meta_data=True)
    print(f"Watching {len(all_files)} files")
    # duration = 0

    if apply_current_tags is True:
        apply_current_folders_as_tag(all_files)

    while True:
        _time.sleep(.5)
        if len(all_files) == 0:
            all_files = _f.get_files(watch_path, ext="images",include_meta_data=True)
        # duration += .5
        # if duration % 30 == 0:
        #     transferCompleteImages.transferCompleteImages()
        #     transferDLToOrg()
        #     convertOrgFolder()
        moved_files = []
        new_all_files = []
        update_files = []

        for file in all_files:
            # if the file does not exist, append it to the moved_files list.
            if _f.exists(file['file_path']) is False:
                print(f"moved: {file['file_name']}")
                moved_files.append(file)
            else:
                new_all_files.append(file)

        for file in moved_files:
            # search for the file by its name
            result = _f.by_name(file['file_name'], watch_path)
            if result is not None:
                # print(f"result: {result}")
                # get the file data, essentially update its paths and such.
                file_data = _f.get_data(result[0])
                # append the file to the update_files array
                update_files.append(file_data)

        new_files = _tag_by_folder_name(update_files,_os.path.basename(watch_path),save=False)
        if synonyms is not False:
            new_files = apply_keyword_synonyms(new_files,synonyms,save=False)
        save_file_obj(new_files)

        new_all_files.extend(new_files)
        all_files = new_all_files

def apply_current_folders_as_tag(files,**kwargs):
    save = _obj.get_kwarg(['save'],False,(bool),**kwargs)
    if _dir.exists(files):
        files = _f.get_files(files, ext="images",include_meta_data=True)
    # if files is False:
    files_array = _parse_file_obj_list(files)
    update_array = []
    # new_file_array = []
    for file in files_array:
        # parse the folder name from the file object
        dir_name = _os.path.basename(file['dir_path'])
        file = add_keyword(file,dir_name,save=False)[0]
        update_array.append(file)
    if save is True:
        save_file_obj(update_array)
    return files_array

def _tag_by_folder_name(files,exclude='',**kwargs):
    save = _obj.get_kwarg(['save'],False,(bool),**kwargs)
    if isinstance(exclude,(str)):
        exclude = [exclude]
    files_array = _parse_file_obj_list(files)
    update_array = []
    # new_file_array = []
    for file in files_array:
        # parse the folder name from the file object
        dir_name = _os.path.basename(file['dir_path'])
        if dir_name not in exclude:
            file = add_keyword(file,dir_name,save=False)[0]
            update_array.append(file)
        # new_file_array.append(file)
    # new_file_array = applyKeywordSynonyms(new_file_array)
    # update_files(new_file_array)
    if save is True:
        save_file_obj(update_array)
    return files_array

def tag_if_missing_keyword(files,needles,keyword):
    update_array = []
    files_array = _parse_file_obj_list(files)
    # print(f"")
    # get all of the files with a needle in their keywords.
    has_needle = has_keyword(files_array,needles)
    # get all of the files that already have the "keyword" and a needle
    missing_needle = has_keyword(has_needle,keyword)
    if len(missing_needle) > 0:
        # remove the "keyword" from those files.
        update_array.extend(delete_keyword(missing_needle,keyword))

    # get all of the files that do NOT have a needle in their keywords
    result = has_keyword(files_array,needles,reverse=True)
    # add the "keyword" to them
    update_array.extend(add_keyword(result,keyword))

    save_file_obj(update_array)


# def has_tag(file,tag):
#     result_array = []
#     tags_array = []
#     if isinstance(tag,(str)):
#         tags_array = [tag]
#     if isinstance(tag,(list)):
#         tags_array = tag
#     file_array = _parse_file_obj_list(file)
#     for file in file_array:
#         if 'iptc_data' not in file:
#             file = get_meta(file)
#         # print(f"file['iptc_data']['Keywords']: ", file['iptc_data']['Keywords'])
#         for t in tags_array:
#             # print(f"t: {t}")
#             if t in file['iptc_data']['Keywords']:
#                 result_array.append(file)
#     if len(result_array) == 1:
#         return result_array[0]
#     return result_array



# def save(file):
#     file_array = _parse_file_obj_list(file)

#     for file in file_array:
#         if 'iptc_data' in file:
#             info = IPTCInfo(file['file_path'], force=True)
#             info['Keywords'] = keywordsToBytes(file['iptc_data']['Keywords'])
#             # info['supplemental category'] = file['iptc_data']['supplemental category']
#             # info['Contact'] = file['iptc_data']['Contact']
#             info.save_as(file['file_path'])
#             _f.delete(f'{file["file_path"]}~')

# def formatIPTCData(d):
#     data = {}
#     if isinstance(d, str) or isinstance(d, bytes):
#         return d.decode('utf-8')
#     # print(f"d Type: {type(d)}")
#     for k, v in d.items():
#         if isinstance(v, dict):
#             data[k] = formatIPTCData(v)
#         if isinstance(v, list):
#             nl = []
#             for x in v:
#                 nl.append(formatIPTCData(x))

#             key = decodeIPTCKey(k)
#             data[key] = nl
#         # else:
#             # print(f"formatIPTCData: {k} : {v}")
#     return data




# def add_tag(file, keyword):
#     result_array = []
#     # Split the keyword by commas if there are any
#     if isinstance(keyword,(str)):
#         keyword = keyword.split(",")
#     # generate a list of file objects from the file argument.
#     file_array = _parse_file_obj_list(file)
#     # print(f"file_array: ", json.dumps(file_array,indent=4))
#     for file in file_array:
#         if 'iptc_data' not in file:
#             file = get_meta(file)
#         # print(f"file: ", json.dumps(file, indent=4))
#         iptc = file['iptc_data']
#         if 'Keywords' not in iptc:
#             iptc['Keywords'] = []

#         if isinstance(keyword, list):
#             for x in keyword:
#                 if x not in iptc['Keywords']:
#                     iptc['Keywords'].append(x)
#         if isinstance(keyword, str):
#             if keyword not in iptc['Keywords']:
#                 iptc['Keywords'].append(keyword)
#         if file['iptc_data']['Keywords'] != iptc:
#             file['update_file'] = True
#         file['iptc_data'] = iptc
#         save(file)
#         result_array.append(file)

#     if len(result_array) == 1:
#         return result_array[0]
#     return result_array

# def delete_tag(file, keyword):
#     result_array = []
#     # Split the keyword by commas if there are any
#     if isinstance(keyword, (str)):
#         keyword = keyword.split(",")
#     # generate a list of file objects from the file argument.
#     file_array = _parse_file_obj_list(file)
#     # print(f"file_array: ", json.dumps(file_array,indent=4))
#     for file in file_array:
#         if 'iptc_data' not in file:
#             file = get_meta(file)
#         # print(f"file: ", json.dumps(file, indent=4))
#         iptc = file['iptc_data']
#         if 'Keywords' not in iptc:
#             iptc['Keywords'] = []

#         new_keywords = []
#         for k in iptc['Keywords']:
#             if k not in keyword:
#                 new_keywords.append(k)
#         iptc['Keywords'] = new_keywords

#         if file['iptc_data']['Keywords'] != iptc:
#             file['update_file'] = True
#         file['iptc_data'] = iptc
#         save(file)
#         result_array.append(file)

#     if len(result_array) == 1:
#         return result_array[0]
#     return result_array



# def decodeIPTCKey(n):
#     d = {
#         "25": "Keywords",
#         "20": "supplemental category",
#         "118": "Contact",
#         "05": "Title",
#         "55": "Date Created",
#     }
#     n = str(n)
#     return d[n]

# def keywordsToBytes(keys):
#     nk = []
#     for k in keys:
#         nk.append(bytes(k.encode()))
#     return nk
