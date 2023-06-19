import os, sys, logging, psutil, hashlib, threading, time, datetime, math
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# /usr/share/nginx/html

# Configure register in /var/log/irondome.log
log_path = '/var/log/irondome.log'
log_path_dir = '/var/log/'

# Verify if program is running as root user
def is_root():
    if not os.geteuid() == 0:
        print("Program must be running by the root user.")
        print(os.geteuid())
        
def check_path():
    # Verify if file exists
    if os.path.exists(log_path):
        print(f"The file '{log_path}' already exists.")
        with open(log_path, "w") as f:
            print(f"File '{log_path}' has been created.")
    else:
        path_splited = log_path.split('/')
        os.makedirs(log_path_dir)
        with open(log_path, "w") as f:
            print(f"File '{log_path}' has been created.")

def check_critical_zone(critical_zone_path):
    if not os.path.exists(critical_zone_path):
        os.mkdir(critical_zone_path)
        with open(critical_zone_path + "/readme.txt", "w") as f:
            pass  # Placeholder for further code
    else:
        print("Already exists.")
        
def calculate_entropy(critical_zone_path):
    # Adjust the chunk size as per your requirements
    chunk_size = 64 * 1024 
    total_bytes = 0
    entropy = 0

    with open(critical_zone_path, 'rb') as file:
        while True:
            data = file.read(chunk_size)
            if not data:
                break
            total_bytes += len(data)
            byte_frequencies = [0] * 256
            for byte in data:
                byte_frequencies[byte] += 1
            for frequency in byte_frequencies:
                if frequency == 0:
                    continue
                probability = frequency / chunk_size
                entropy -= probability * math.log2(probability)

    return entropy / math.log2(total_bytes)
     
# Create Lock object
lock = threading.Lock()

# Define critial zone
def critical_zone(critical_zone_path):
    # Actions inside the critical zone
    print("Entering the critical zone")
    observer = Observer()
    # Specify the folder to monitor and the event handler
    path_to_monitorize = critical_zone_path
    event_handler = MyFileSystemEventHandler()
    # Start monitoring
    observer.schedule(event_handler, path_to_monitorize, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    print("Leaving the critical zone.")

class FileEventHandler(FileSystemEventHandler):

    def __init__(self, extensions):
        self.extensions = extensions
        self.previous_entropy = {}

    def calculate_entropy(path_file):
        with open(path_file, 'rb') as file:
            content = file.read()
            byte_count = len(content)
            if byte_count == 0:
                logging.info(f'Skipping entropy check for 0 bytes file {path_file}')
                return 0
            frequencies = [content.count(byte) for byte in range(256)]
            probabilities = [frequency / byte_count for frequency in frequencies]
            entropy = -sum(p * math.log2(p) if p != 0 else 0 for p in probabilities)

        return entropy
    
    def on_any_event(self, event):
        # Actions to take when an event is detected
        file_path = event.src_path
        _, extension = os.path.splitext(file_path)
        print(log_path)
        if extension in self.extensions:
        # Folder has been detected
            try:         
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                size_bytes, size_readable = get_file_size(event.src_path)
                entropy = calculate_entropy(event.src_path)
                log_message = f'[{timestamp}] - Event: {event.event_type} - Path: {event.src_path} - Size: {round(size_bytes/1024,3)} MB - Entropy: {entropy}\n '
                open_message = f'[{timestamp}] - Event: opened - Path: {event.src_path} - Size: {round(size_bytes/1024,3)} MB - Entropy: {entropy}\n '

                if file_path in self.previous_entropy:
                    previous_entropy = self.previous_entropy[file_path]
                    print(previous_entropy)
                    if entropy == previous_entropy:
                        with open("/Users/your_user/log.txt",'r') as file:
                            lines = file.readlines()
                            if lines and lines[-1].strip() == lines[-2].strip():
                                print("Last line unchanged. Skipping write operation.")
                        with open("/Users/your_user/log.txt", "a") as file:
                                    file.write(open_message)
                        self.previous_entropy[file_path]=entropy
                    elif entropy != previous_entropy:
                        print(entropy,previous_entropy)
                        with open("/Users/your_user/log.txt",'r') as file:
                            lines = file.readlines()
                            if lines and lines[-1].strip() == lines[-2].strip():
                                print("Last line unchanged. Skipping write operation.")
                        with open("/Users/your_user/log.txt",'a') as file:
                            file.write(log_message)
                    else:
                        if entropy > 0.26:
                            log_encryption = f"Possible encryption detected: {event.src_path}\n"
                        
                            with open("/Users/your_user/log.txt",'a') as file:
                                file.write(log_encryption)
                        else:
                            with open("/Users/your_user/log.txt",'a') as file:
                                file.write(log_message)
                else:
                    self.previous_entropy[file_path]=entropy
                    print("Something is wrong.")
            except:
                print("Log not detected.")
        else:
            print("Thats not an extension as we wanted.")

    def on_created(self, event):
        if not event.is_directory:
            file_path = event.src_path
            _, extension = os.path.splitext(file_path)
            if extension in self.extensions:
                try:
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    size_bytes, size_readable = get_file_size(event.src_path)
                    entropy = calculate_entropy(event.src_path)
                    log_message = f'[{timestamp}] - Event: {event.event_type} - Path: {event.src_path} - Size: {round(size_bytes/1024,3)} MB - Entropy: {entropy}\n '
                    print(log_message)
                    print(entropy)
                    if entropy > 0.26:
                        log_encryption = f"Possible encryption detected: {event.src_path}\n"
                        with open(log_path,'a') as file:
                            file.write(log_encryption)
                    else:
                        with open(log_path,'a') as file:
                            file.write(log_message)
                except:
                    print("Log not detected.")
                # Perform your desired actions here for the files with matching extensions

# Define a custom event handler
class MyFileSystemEventHandler(FileSystemEventHandler):
    
    def calculate_entropy(path_file):
        with open(path_file, 'rb') as file:
            content = file.read()
            byte_count = len(content)
            if byte_count == 0:
                logging.info(f'Skipping entropy check for 0 bytes file {path_file}')
                return 0
            frequencies = [content.count(byte) for byte in range(256)]
            probabilities = [frequency / byte_count for frequency in frequencies]
            entropy = -sum(p * math.log2(p) if p != 0 else 0 for p in probabilities)

        return entropy

    def on_any_event(self, event):
        # Actions to take when an event is detected 
        if event.is_directory:
        # Folder has been detected
            try:      
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                size_bytes, size_readable = get_file_size(event.src_path)
                entropy = calculate_entropy(event.src_path)
                log_message = f'[{timestamp}] - Event: {event.event_type} - Path: {event.src_path} - Size: {round(size_bytes/1024),3} MB - Entropy: {entropy}\n '
                print(log_message)
                print(entropy)
                if entropy > 0.26:
                    log_encryption = f"Possible encryption detected: {event.src_path}\n"
                    with open(log_path,'a') as file:
                        file.write(log_encryption)
                else:
                    with open(log_path,'a') as file:
                        file.write(log_message)
            except:
                print("Log not detected.")
        else:
            try:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                size_bytes, size_readable = get_file_size(event.src_path)            
                entropy = calculate_entropy(event.src_path)
                print(entropy)
                log_message = f'[{timestamp}] - Event: {event.event_type} - Path: {event.src_path} - Size: {round(size_bytes/1024),3} MB - Entropy: {entropy}\n '
                if entropy > 0.26:
                    log_encryption = f"Possible encryption detected: {event.src_path}\n"
                    with open(log_path,'a') as file:
                        file.write(log_encryption)
                else:
                    with open(log_path,'a') as file:
                        file.write(log_message)
            except:
                print("Log not detected.")

# Function to access the critical zone
def access_critical_zone():
    # Acquire the lock
    lock.acquire()
    try:
        # Call the critical zone function
        critical_zone()
    finally:
        # Release the lock
        lock.release()
        
# Check memory usage
def check_memory_usage():
    process = psutil.Process(os.getpid())
    memory_usage = process.memory_info().rss / 1024 / 1024  # Memory usage in MB
    if memory_usage > 100:
        logging.warning("Memory usage exceeds 100 MB: %f MB", memory_usage)

def get_file_size(critical_zone_path):
    size_bytes = os.path.getsize(critical_zone_path)
    # Convert the size to a human-readable format (e.g., KB, MB, GB)
    size_readable = convert_size(size_bytes)

    return size_bytes, size_readable

def convert_size(size_bytes):
    # Constants for file size units
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    # Determine the appropriate unit based on the file size
    unit_index = 0
    while size_bytes >= 1024 and unit_index < len(units) - 1:
        size_bytes /= 1024
        unit_index += 1
    # Format the size with two decimal places
    size_formatted = "{:.2f} {}".format(size_bytes, units[unit_index])

    return size_formatted

# Usage example
if __name__ == "__main__":
    if not os.geteuid() == 0:
        print("Program must be executed by the root user.")
        print(os.geteuid())
    else:
        if len(sys.argv) < 2:
            print("Please provide the path or files to monitor as arguments.")
            sys.exit(1)
        if len(sys.argv) == 2:
            path = sys.argv[1]
            if os.path.exists(path):
                print("The path exists")
                check_path()
                check_critical_zone(path)
                critical_zone(path)
            else:
                print("The path doesnt exist")
        else:
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
            '.rb', '.rtf', '.sch', '.sldm', '.sldx', '.slk', '.sln', '.sql', '.sqlite', '.ss', '.ssa', '.ssb','.sh', '.sxc', 
            '.sxd', '.sxi', '.sxm', '.sxw', '.tar', '.tbk', '.tgz', '.tif', '.tiff', '.txt', '.uop', '.uot', '.vb', 
            '.vbs', '.vcd', '.vdi', '.vmdk', '.vmx', '.vob', '.vsd', '.vsdx', '.wav', '.wb2', '.wk1', '.wks', '.wma', 
            '.wmv', '.xlc', '.xlm', '.xls', '.xlsb', '.xlsm', '.xlsx', '.xlt', '.xltm', '.xltx', '.xlw', '.xml', '.zip']
            
            print("We are working with extensions")
            
            extensions = sys.argv[1:]
            event_handler = FileEventHandler(extensions)
            observer = Observer()
            observer.schedule(event_handler, path='.', recursive=True)
            print(f"Monitoring file extensions: {', '.join(extensions)}")
            observer.start()
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                observer.stop()
            observer.join()