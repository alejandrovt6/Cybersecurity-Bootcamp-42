# Libraries
import argparse, os, requests, validators, shutill
from bs4 import BeautifulSoup 
from urllib.parse import urljoin, urlparse

# Program
soup = None

IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]

def local_f(url, path):
    with open(url, "rb") as f:
        contents = f.read()
    soup = BeautifulSoup(contents, features="html.parser")
    # Download found images
    for img in soup.find_all("img"):

        img_url = img.attrs.get("src")
        print(img_url)
        if img_url.startswith("http"):
            print("This is not a local image.")
        else:
            try:
                shutil.copy(img_url, path)
            except(FileNotFoundError):
                print("File not found")
        
        if not img_url:
            continue
        
        # Ignore images that do not have a known extension  
        if not any(img_url.lower().endswith(ext) for ext in IMAGE_EXTENSIONS):
            continue
    
    print(img_url)

def download_image(url, filename):
    if url.startswith("http") or url.startswith("https"):
        with open(filename, "wb") as f:
            print(url)
            response = requests.get(url)
            f.write(response.content)
    else:
        with open(url,"rb") as f:
            with open(filename, "wb") as out_file:
                out_file.write(f.read())

def scrape_images(url, path, recursive, max_depth, current_depth=0):
    if current_depth >= max_depth:
        return

    # Obtain page HTML
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Download found images
    for img in soup.find_all("img"):
        img_url = img.attrs.get("src")
        if not img_url:
            continue

        # Ignore images that do not have known extension
        if not any(img_url.lower().endswith(ext) for ext in IMAGE_EXTENSIONS):
            continue

        # Download image in specified path
        img_url = urljoin(url, img_url)
        filename = os.path.join(path, os.path.basename(img_url))
        download_image(img_url, filename)
        print(f"Downloaded image {img_url} en {filename}")

    # Recursively traverse the found URLs if the -r option was specified
    if recursive:
        for link in soup.find_all("a"):
            link_url = link.attrs.get("href")
            if not link_url:
                continue
            if link_url.startswith("#"):
                continue

            link_url = urljoin(url, link_url)
            if not link_url.startswith("http"):
                # Ignore links which not is HTTP
                continue
            if any(link_url.lower().endswith(ext) for ext in IMAGE_EXTENSIONS):
                # Ignore links that point directly to an image
                continue

            # Download images recursively
            scrape_images(link_url, path, recursive, max_depth, current_depth + 1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Spider: Dowlonload all images in website.")
    parser.add_argument("url", type=str, help="The UR.")
    parser.add_argument("-r", "--recursive", action="store_true", help="Recursively traverse.")
    parser.add_argument("-l", "--depth", type=int, default=5, help="Maximum depth level in recursive download.")
    parser.add_argument("-p", "--path", type=str, default="./data/", help="Path where the downloaded files will be saved.")

    args = parser.parse_args()

    url = args.url
    recursive = args.recursive
    max_depth = args.depth
    path = args.path

    if not os.path.exists(path):
        scrape_images(url, path ,recursive, max_depth)
        os.makedirs(path)
        
    if validators.url(url)== True:
        print("")
    elif os.path.exists(url):
        if not url.endswith(".html"):
            print("Format no valid")
            exit()
        local_f(url, path)
    else:
        print("Not is URL or path valid.")
        exit()

