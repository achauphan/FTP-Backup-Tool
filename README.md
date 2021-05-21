# FTP-Backup-Tool
This tool is used for quickly accessing a FTP file server and downloading a specified directory onto your local machine to create a backup. Backup profiles can be create for
file servers that need to be backed up often. 

## Download
Visit [release page](https://github.com/achauphan/FTP-Backup-Tool/releases/tag/v1.0.0) and download the latest version.

## Usage
Run main.py

### Creating profiles
To create a new backup profile, either enter the create command and following instructions or modify the profiles.json file following the given example profile format.
```
{
  "example_profile": [
    {
      "host": "example_hostname",
      "username": "example_username",
      "ftp_backup_path": "/",
      "local_backup_path": "./backups"
    }
  ],
  "example_profile 2": [
    {
      "host": "example_hostname 2",
      "username": "example_username 2",
      "ftp_backup_path": "/",
      "local_backup_path": "./backups"
    }
  ]
} 
```
Note: This structure is a python dictionary. Add additional profiles manually according to normal python dictionary conventions.
