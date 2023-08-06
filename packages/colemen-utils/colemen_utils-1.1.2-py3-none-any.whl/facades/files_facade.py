# pylint: disable=missing-function-docstring
# pylint: disable=unused-import
# pylint: disable=line-too-long
'''
    A module of utility methods used for Creating, Reading, Updating and Deleting files..

    ----------

    Meta
    ----------
    `author`: Colemen Atwood
    `created`: 06-03-2022 10:22:15
    `memberOf`: file
    `version`: 1.0
'''


import utils.files.file as file

decompress = file.decompress
compress = file.compress
exists = file.exists
delete = file.delete
gen_path_list = file.gen_path_list
import_project_settings = file.import_project_settings
rename = file.rename
move_contents = file.move_contents
move = file.move
copy = file.copy
get_data = file.get_data
get_drive = file.get_drive
get_modified_time = file.get_modified_time
get_access_time = file.get_access_time
get_create_time = file.get_create_time
get_ext = file.get_ext
get_name_no_ext = file.get_name_no_ext
gen_relative_path = file.gen_relative_path
gen_dst_path = file.gen_dst_path
gen_src_path = file.gen_src_path
get_files = file.get_files
get_files_ftp = file.get_files_ftp















