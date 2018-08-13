import os
from fnmatch import fnmatch


def find_globs_from_files(node, initials, project_dir, files, ignore_list,
                          already_found_ext=[]):
    """
    Finds the globs from the files present in the section, looking first
    for the glob '**', then the glob '**' with different filename extensions
    present. Repeats the same process for the glob '*' on each iteration.
    :param node:
        The current Node object representing the file or folder we are on.
    :param initials:
        Constructing the name of the file by collecting names from the current
        node and passing it along to the children.
    :param project_dir:
        The name of the project directory.
    :param files:
        The files list for the section which is appended/changed on each
        recursion of this method.
    :param ignore_list:
        The list of files to ignore for the current section which is
        constructed along as the recursion algorithm proceeds.
    :param already_found_ext:
        The list of extensions already covered inside the glob '**' with
        the extension to be passed along the the children nodes to skip the
        checks.
    :return:
        List of appended files and list of files to ignore for the current
        section.
    """
    for child in node.children:
        if not child.children == []:
            if child.name == 'project_dir':
                child_name = project_dir
            else:
                child_name = child.name
            dir_name = initials + os.sep + child_name
            dir_name = dir_name.replace(os.sep + os.sep, os.sep)
            list_of_files = list()
            for (dirpath, dirnames, filenames) in os.walk(dir_name):
                list_of_files += [os.path.join(dirpath, file)
                                  for file in filenames]
            files_in_section = list(child.get_files(dir_name))
            number_of_common_files = 0
            files_not_common = []
            for file in list_of_files:
                if file in files_in_section:
                    number_of_common_files += 1
                else:
                    files_not_common.append(file)
            # The number 7 is chosen as a plausible guess for when
            # the number of files in the ignore
            # section exceed the limit.
            ratio = float(number_of_common_files/len(list_of_files))
            if list_of_files != [] and (ratio >= 0.9 or len(
                    files_not_common) <= 7):
                glob = dir_name + os.sep + '**'
                new_files = []
                for file in files:
                    if not fnmatch(file, glob):
                        new_files.append(file)
                new_files.append(glob)
                files = new_files
                ignore_list += files_not_common
                # Since the glob '**' is found to be valid irresepective
                # of the extension,
                # all the files/leaves in the corresponding subtree are covered.
                return files, ignore_list
            else:
                files_in_section_ext_dict = {}
                for file in files_in_section:
                    ext = os.path.splitext(file)[1]
                    if ext in files_in_section_ext_dict:
                        files_in_section_ext_dict[ext].append(file)
                    else:
                        files_in_section_ext_dict[ext] = [file]

                list_of_files_ext_dict = {}
                for file in list_of_files:
                    ext = os.path.splitext(file)[1]
                    if ext in list_of_files_ext_dict:
                        list_of_files_ext_dict[ext].append(file)
                    else:
                        list_of_files_ext_dict[ext] = [file]

                for ext in files_in_section_ext_dict:
                    if ext in already_found_ext:
                        continue
                    val_in_sec = files_in_section_ext_dict[ext]
                    val_in_files = list_of_files_ext_dict[ext]
                    not_common_ext_files = []
                    num_ext_common_files = 0
                    for file in val_in_files:
                        if file in val_in_sec:
                            num_ext_common_files += 1
                        else:
                            not_common_ext_files.append(file)

                    if val_in_files != [] and (
                        float(len(val_in_sec)/len(
                            val_in_files)) >= 0.9 or len(
                            not_common_ext_files) <= 7):
                        already_found_ext.append(ext)
                        glob_ext = dir_name + os.sep + '**' + ext
                        new_files_ext = []
                        for file in files:
                            if not fnmatch(file, glob_ext):
                                new_files_ext.append(file)
                        new_files_ext.append(glob_ext)
                        files = new_files_ext
                        ignore_list += not_common_ext_files

            list_of_files_cd = list()
            for (dirpath, dirnames, filenames) in os.walk(dir_name):
                list_of_files_cd += [os.path.join(dirpath, file)
                                     for file in filenames]
                break

            files_in_section_cd = list(child.get_files_cd(dir_name))
            number_of_common_files_cd = 0
            files_not_common_cd = []
            for file in list_of_files_cd:
                if file in files_in_section_cd:
                    number_of_common_files_cd += 1
                else:
                    files_not_common_cd.append(file)
            if list_of_files_cd != [] and (
                    float(number_of_common_files_cd/len(
                        list_of_files_cd)) >= 0.9 or len(
                        files_not_common_cd) <= 7):
                glob_cd = dir_name + os.sep + '*'
                new_files_cd = []
                for file in files:
                    if (not fnmatch(file, glob_cd)):
                        new_files_cd.append(file)
                new_files_cd.append(glob_cd)
                files = new_files_cd
                ignore_list += files_not_common_cd
            else:
                files_in_section_ext_dict_cd = {}
                for file in files_in_section_cd:
                    ext_cd = os.path.splitext(file)[1]
                    if ext_cd in files_in_section_ext_dict_cd:
                        files_in_section_ext_dict_cd[ext_cd].append(file)
                    else:
                        files_in_section_ext_dict_cd[ext_cd] = [file]

                list_of_files_ext_dict_cd = {}
                for file in list_of_files_cd:
                    ext = os.path.splitext(file)[1]
                    if ext in list_of_files_ext_dict_cd:
                        list_of_files_ext_dict_cd[ext].append(file)
                    else:
                        list_of_files_ext_dict_cd[ext] = [file]

                for ext in files_in_section_ext_dict_cd:
                    if ext in already_found_ext:
                        continue
                    val_in_sec_cd = files_in_section_ext_dict_cd[ext]
                    val_in_files_cd = list_of_files_ext_dict_cd[ext]
                    not_common_ext_files_cd = []
                    num_ext_common_files_cd = 0
                    for file in val_in_files_cd:
                        if file in val_in_sec_cd:
                            num_ext_common_files_cd += 1
                        else:
                            not_common_ext_files_cd.append(file)
                    if val_in_files_cd != [] and (
                            float(len(val_in_sec_cd)/len(
                                val_in_files_cd)) >= 0.9 or len(
                                not_common_ext_files_cd) <= 7):
                        glob_ext_cd = dir_name + os.sep + '*' + ext
                        new_files_ext_cd = []
                        for file in files:
                            if not fnmatch(file, glob_ext_cd):
                                new_files_ext_cd.append(file)
                        new_files_ext_cd.append(glob_ext_cd)
                        files = new_files_ext_cd
                        ignore_list += not_common_ext_files_cd

            files, ignore_list = find_globs_from_files(
                child, dir_name, project_dir, files, ignore_list,
                already_found_ext)
    return files, ignore_list
