#!/usr/bin/python

import sys, os
from pathlib import Path
from collections import defaultdict

ROOT = '/Users/vishakhagoel/Desktop/test/twitter/repo_root/'
OWNERS = '/OWNERS'
DEPENDENCIES = '/DEPENDENCIES'
APPROVED = 'Approved'
NOT_APPROVED = 'Insufficient Approvals'


def read_file(file_path):
    with open(str(file_path), 'r') as data:
        return [line.strip() for line in data.readlines()]


# For each directory A, find all the [directories] that are dependent on A
def build_dependency_map(directory):
    dependency_dict = defaultdict(list)
    for root, dirs, files in os.walk(directory):
        subdir = os.path.basename(root)                                 # follow, message, tweet, or user
        dependency_file = Path(directory + subdir + DEPENDENCIES)       # path of the dependency file in the current sub-directory
        dependency_data = read_file(dependency_file) if dependency_file.exists() else None      # read DEPENDENCIES file of all sub-directories and store it in dependency_data

        # create a map of all dependencies key:value where "value" is a list of directories dependent on "key"
        if dependency_data == None:
            continue
        for index in range(len(dependency_data)):
            dependency_dict.setdefault(dependency_data[index], []).append(directory + subdir)
    return dependency_dict


def check_owners(approvers, directory_path):
    owners_file = Path(str(directory_path) + OWNERS)
    owners_data = read_file(owners_file) if owners_file.exists() else None
    if owners_data == None:
        check_owners(approvers, os.path.dirname(directory_path))
    for index in range(len(owners_data)):
        if owners_data[index] in approvers:
            return True
    return False


def check_dependencies(approvers, directory_path):
    dependency_dict = defaultdict(list)
    dependency_dict = build_dependency_map(ROOT + 'src/com/twitter/')
    dependency_list = []
    if directory_path in dependency_dict:
        dependency_list = dependency_dict[directory_path]
        for index in range(len(dependency_list)):
            if check(approvers, dependency_list[index]) == False:
                return False


def check(approvers, files_changed):
    for index in range(len(files_changed)):
        directory_path = Path(ROOT + os.path.dirname(files_changed[index]))
        #directory_path = os.path.dirname(os.path.abspath(files_changed[index])) ---- gives current project path
        if check_owners(approvers, directory_path) == False:
            return NOT_APPROVED
        if check_dependencies(approvers, directory_path) == False:
            return NOT_APPROVED
        return APPROVED


def main():
    approvers = ["alovelace"]
    #files_changed = ["src/com/twitter/follow/Follow.java"]
    files_changed = ["src/com/twitter/user/User.java"]
    print(check(approvers, files_changed))
    #print(build_dependency_map(root_path))

main()

# traverse root directory, and list directories as dirs and files as files
#for root, dirs, files in os.walk("/Users/vishakhagoel/Desktop/PE/"):
#    path = root.split(os.sep)
#    print((len(path) - 1) * '-', os.path.basename(root))
#    for file in files:
#        print(len(path) * '-', file)

