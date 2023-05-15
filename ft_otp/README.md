# 🔑 FT_OTP

## 📝 Description
ft_otp.py is a Python script that generates a One-Time Password (OTP) based on the Time-Based One-Time Password (TOTP) algorithm. The script can generate a new key and store it encrypted or generate a time-based OTP using a stored key.

## 🔍 Requeriments
* Python 3.x
* Libraries: hmac, base64, hashlib, struct, time, re, argparse, cryptography

## 🛠️ Usage
**To generate a new key and store it encrypted, run the command:** <br>
* ./ft_otp.py -g [file_name] 

**To generate a time-based OTP using a stored key, run the following command:** <br>
* ./ft_otp.py -k [file_name] 

**You can also provide the file name as an argument, like this:** <br>
* ./ft_otp.py [file_name]

## 💡 Examples
**Generating a new key and storing it encrypted:**<br>
* ./ft_otp.py -g my_key.hex <br>
* Enter the key encoded in hexadecimal: [enter your key here] <br>
* b'gAAAAABh5ArRbfCtBdOGcC8_kdeG8UOL7o67cQVWQ8J3lnj8g96b8N5msFzT9CJx7dIvMwhUa7-9KQsPlEYKZVbhKt6nVQKhw==' <br>
* Encrypted key and master encrypted key successfully created.

**Generating a time-based OTP using a stored key:**<br>
* ./ft_otp.py -k ft_otp.key <br>
* Enter the decryption key: [enter your decryption key here]<br>
* jfvbhl4y7d3c <br>
* 040775 <br>

**Generating a time-based OTP using a stored key with a provided file name:**
* ./ft_otp.py my_key.hex <br>
* fql5hk3i4a5v <br>
* 965901 <br>