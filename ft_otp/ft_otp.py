# Libraries
import hmac, base64, hashlib, struct, time, re, argparse
from cryptography.fernet import Fernet, InvalidToken

# Program
# Globals var
key = None
file = None
secret = None

def input_(key):
    global secret
    if not re.match(r'^[0-9a-fA-F]{64,}$', key):
        print("\n\033[31mThe key encoded in hexadecimal is no longer than 64 characters. You should enter a longer string.\033[39m\n")
        exit()
    hex2bytes = bytes(key, 'utf-8')
    bytes2b32 = base64.b32encode(hex2bytes)
    secret = bytes2b32.decode('utf-8')
    return secret

def get_hotp_token(decrypt, intervals_no):
    key = base64.b85decode(decrypt)
    #decoding our key
    msg = struct.pack(">Q", intervals_no)
    #conversions between Python values and C structs represente
    h = hmac.new(key, msg, hashlib.sha1).digest()
    o = h[19] & 15
    #Generate a hash using both of these. Hashing algorithm is HMAC
    h = (struct.unpack(">I", h[o:o+4])[0] & 0x7fffffff) % 1000000
    #unpacking
    return h

def get_totp_token(decrypt):
    #ensuring to give the same otp for 30 seconds
    x =str(get_hotp_token(decrypt,intervals_no=int(time.time())//30))
    #adding 0 in the beginning till OTP has 6 digits
    while len(x)!=6:
        x+='0'
    return x
#base64 encoded key

def encrypt_data(secret):
    print(secret)
    with open ("master.key", "wb") as k:
        master_key = Fernet.generate_key()
        f = Fernet(master_key)
        k.write(master_key)
        token = f.encrypt(bytes(secret, 'utf-8'))
    with open ("ft_otp.key", "wb") as f:
        f.write(token)
        return token      
        
def decrypt_data(file):
    try:
        with open("master.key", "rb") as fa:
            file_data = fa.read()
            with open(file,"rb") as e:
                file_data2 = e.read()
                f = Fernet(file_data)
            token_decrypt = f.decrypt(file_data2)
            token_decoded = base64.b32decode(token_decrypt)
            # print(token_decoded)
            token_decoded = token_decoded.decode('utf-8')
            # print(token_decoded)
            return token_decoded
    except (FileNotFoundError, InvalidToken, IsADirectoryError):
        print("\n\033[31mInvalid file. You should enter a valid file.key.(1)\033[39m\n")
        exit()
            
def main():
    parser = argparse.ArgumentParser(
        prog="./ft_otp",
        description="One-Time Password generator.",)
    parser.add_argument(
        "-g",
        help="Generate a new key and store it encrypted",
        action='store_true')
    parser.add_argument(
        "-k",
        help="Generate a time-based One-time Password using a file 'ft_otp.key'.",
        action='store_true')
    parser.add_argument("file", help="Provide a valid file" , type=str, default="key.hex")     
    return parser.parse_args()

def obtain_hash(file):
    global key
    with open(file, "r") as e:
        key=e.read()


if __name__ == "__main__":
    args = main()
    gen_key = args.g
    k_key = args.k
    file=args.file

    if gen_key == True:
        try:
            obtain_hash(file)
            secret = input_(key)
            token = encrypt_data(secret)
            print(token)
            print("\n\033[32mEncrypted key and master encrypted key successfully created.\033[39m\n")
        except:
            FileNotFoundError(print("\n\033[31mInvalid file. You should enter a valid file.key.(2)\033[39m\n"))
            
        
    elif k_key == True:
        try:        
            decrypt = decrypt_data(file)
            print(decrypt)
            print(get_totp_token(decrypt))
            # time.sleep(30)
            # print(get_totp_token(token_decrypt))
        except(FileNotFoundError, InvalidToken, IsADirectoryError):
            print("\n\033[31mInvalid file. You should enter a valid file.key.(1)\033[39m\n")

