# Stockholm
## Description
Rasomware program that will encrypt the files in /home/user/infection and decrypt them in this or another one that is mentioned.

The program will rename all files in mentioned folder adding the ".ft" extension. If already have that extension, they will not be renamed.

The program was created in Python. Files will encrypt with Fernet library. (Simmetric encryption).

## How to use
stockholm.py [-h] [-r key] [-v] [-s]

| Valid arguments for stokholm.py: | 
|-----------------------------------|
|   -r key    | Revert infection using the encryption key     |
|   -s    | Disable screen output      |
| -v, --version      | Show the version of the program     |
| -h, --help      | Show help message     |
