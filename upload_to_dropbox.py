import sys
import dropbox
import pickle

from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError

# Access token
tokenFile = open("TOKEN.dat", "rb")
TOKEN = pickle.load(tokenFile)
tokenFile.close()


dbx = dropbox.Dropbox(TOKEN)

# Uploads contents of LOCALFILE to Dropbox
def backup(LOCALFILE, BACKUPPATH):
    with open(LOCALFILE, 'rb') as f:
        # We use WriteMode=overwrite to make sure that the settings in the file
        # are changed on upload
        print("Uploading " + LOCALFILE + " to Dropbox as " + BACKUPPATH + "...")
        try:
            dbx.files_upload(f.read(), BACKUPPATH, mode=WriteMode('overwrite'))
        except ApiError as err:
            # This checks for the specific error where a user doesn't have enough Dropbox space quota to upload this file
            if (err.error.is_path() and
                    err.error.get_path().error.is_insufficient_space()):
                sys.exit("ERROR: Cannot back up; insufficient space.")
            elif err.user_message_text:
                print(err.user_message_text)
                sys.exit()
            else:
                print(err)
                sys.exit()


# Adding few functions to check file details
def checkFileDetails():
    print("Checking file details")

    for entry in dbx.files_list_folder('').entries:
        print("File list is : ")
        print(entry.name)


# Run this script independently
def startDropboxUpload(fileName):
    # Check for an access token


    LOCALFILE = "images/" + fileName
    BACKUPPATH = '/' + fileName  # Keep the forward slash before destination filename

    if (len(TOKEN) == 0):
        sys.exit("ERROR: Looks like you didn't add your access token. Open up backup-and-restore-example.py in a text editor and paste in your token in line 14.")

    # Create an instance of a Dropbox class, which can make requests to the API.
    print("Creating a Dropbox object...")

    # Check that the access token is valid
    try:
        dbx.users_get_current_account()
    except AuthError as err:
        sys.exit(
            "ERROR: Invalid access token; try re-generating an access token from the app console on the web.")

    try:
        checkFileDetails()
    except Error as err:
        sys.exit("Error while checking file details")

    print("Creating backup...")
    # Create a backup of the current settings file
    backup(LOCALFILE, BACKUPPATH)

    print("Done!")