import json


def start():
    profiles = load_profiles()
    if len(profiles) == 0:
        print("No profiles exists. To create a backup profile, input 'create' \n")
    else:
        for key in profiles.keys():
            print(key + ": ")
            print("  Host: " + profiles[key][0]['host'])

    user_input = input("Inputs: "
                       "\n  [profile_name]: starts the backup procedure for given profile."
                       "\n  create: create a backup profile."
                       "\n  delete [profile_name]: delete a profile.\n")
    print("\n")

    user_input = user_input.split(' ')
    if user_input[0] == "create":
        create_profile(profiles)
    elif user_input[0] == "delete":
        delete_profile(user_input[1], profiles)
    elif has_profile(user_input[0], profiles):
        return select_profile(user_input[0], profiles)
    else:
        print("Invalid input.")
        start()


def create_profile(profiles):
    temp_profiles = profiles
    new_profile_name = input("Enter new profile's name: ")

    if has_profile(new_profile_name, temp_profiles):
        user_input = input("Profile already exists, do you want to override " + new_profile_name + "(yes/no)")
        if user_input == "no":
            start()

    temp_profiles[new_profile_name] = []
    hostname = input("Input hostname: ")
    username = input("Input username: ")
    ftp_backup_path = input("FTP backup path:  ")
    local_backup_path = input("Local backup directory path (if blank, defaults to /backups in project directory): ")

    if local_backup_path == "":
        local_backup_path = "./backups"

    temp_profiles[new_profile_name].append({
        'host': hostname,
        'username': username,
        'ftp_backup_path': ftp_backup_path,
        'local_backup_path': local_backup_path
    })

    save_profiles(temp_profiles)

    start()


def has_profile(profile, profiles):
    return profile in profiles


def select_profile(profile, profiles):
    if has_profile(profile, profiles):
        return profiles[profile][0]
    else:
        print("Profile does not exists.")
        start()


def delete_profile(profile, profiles):
    if has_profile(profile, profiles):
        removed_profile = profiles.pop(profile)
        save_profiles(profiles)
        print("Successfully removed profile " + profile)
        start()
    else:
        print("Profile does not exists.")
        start()


def load_profiles():
    with open('profiles.json', 'r') as open_file:
        try:
            json_object = json.load(open_file)
        except:
            return {}
        return json_object


def save_profiles(profiles):
    json_object = json.dumps(profiles, indent=2)
    with open('profiles.json', 'w') as outfile:
        outfile.write(json_object)
