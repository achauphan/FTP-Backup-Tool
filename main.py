from ftplib import *
from datetime import datetime
import os
from zipfile import ZipFile
import getpass
from input_handler import start

ftp = FTP()


# 192.168.0.34
def main():
    global ftp
    profile_data = start()

    try:
        ftp = FTP(profile_data['host'])
    except:
        print("  Unable to connect to host. \n")
        main()

    password = getpass.getpass(prompt="Enter password: ")
    try:
        ftp.login(profile_data['username'], password)
    except:
        print("  Invalid login. \n")
        main()

    ftp_path = profile_data['ftp_backup_path']

    parent_dir = get_parent_dir(ftp_path)
    local_backup_dir = profile_data['local_backup_path']  # allow for user to set their backup dir

    try:
        os.chdir(local_backup_dir)
    except FileNotFoundError:
        print("Backup directory did not exist from given path. Created a new directory at path.")
        os.mkdir(local_backup_dir)
        os.chdir(local_backup_dir)

    current_date_time = datetime.now().strftime("%m-%d-%y--%H-%M-%S")
    backup_dir_name = parent_dir + "--" + current_date_time

    try:
        os.makedirs(backup_dir_name)
        os.chdir(backup_dir_name)
    except FileExistsError:
        print("Local backup directory already exists.")

    ftp.cwd(ftp_path)

    # get list of all files in current ftp directory
    files = ftp.nlst()
    # backup files from ftp directory to local machine
    backup_files(files)
    # zip the backup directory and remove directory
    zip_and_remove_backup_dir(backup_dir_name)

    print("Backup of " + parent_dir + " was successful.")
    user_input = input("Input anything to exit. \n")


# Traverse the given ftp file structure while downloading and re-creating the
# file structure locally.
def backup_files(files):
    for file in files:
        if is_file(file, "ftp"):
            with open(file, 'wb') as f:
                ftp.retrbinary('RETR ' + file, f.write)
        else:  # is a directory
            os.mkdir(file)
            os.chdir(file)
            ftp.cwd(file)
            backup_files(ftp.nlst())
            os.chdir('..')
            ftp.cwd('..')


# Zip a given directory path. Once the directory has been archived, delete the directory.
def zip_and_remove_backup_dir(backup_dir_path):
    os.chdir('..')
    with ZipFile(backup_dir_path + ".zip", 'w') as zip:
        for root, dirs, files in os.walk(backup_dir_path):
            for file in files:
                file_path = os.path.join(root, file)
                zip.write(file_path, os.path.relpath(file_path, os.path.join(backup_dir_path, '..')))
    remove_dir_tree([backup_dir_path])


# Checks whether a given path is a directory or a file.
# Has two modes, "ftp" and "os" for their respective checking system.
def is_file(path, mode):
    if mode == "ftp":
        try:
            ftp.size(path)
        except error_perm:
            return False
        return True
    elif mode == "os":
        return os.path.isfile(path)
    else:
        raise Exception("Mode type is not valid.")


# Given a directory path, get name of parent directory
# By using String.split(), need to account for if the given path includes a / and the end.
def get_parent_dir(path):
    split_path = path.split('/')
    length = len(split_path)
    if split_path[length - 1] == '':
        return split_path[len(split_path) - 2]
    else:
        return split_path[len(split_path) - 1]


# Completely delete a directory tree.
# Removes all directories and files.
def remove_dir_tree(files):
    for file in files:
        if is_file(file, "os"):
            os.remove(file)
        else:  # is a directory
            try:
                os.rmdir(file)
            except OSError:
                os.chdir(file)
                remove_dir_tree(os.listdir())
                os.chdir('..')
                # dir_ must be empty
                os.rmdir(file)


if __name__ == '__main__':
    main()
