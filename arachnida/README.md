# SPIDER and SCORPION

## 🕷️ SPIDER - Download All Images in Website

### 📝 Description
Spider is a Python program that downloads all images from a website. It uses the BeautifulSoup library to parse the HTML of the website and locate all the image tags. Then, it downloads each image to a specified directory recursively.

### 🛠️ Usage
To run Spider, navigate to the directory where the spider.py file is located and run the following command in your terminal:

python spider.py [-h] [-r] [-l DEPTH] [-p PATH] url

The available options are:

* -r: download images recursively from the URL received as a parameter.
* -r -l [N]: indicates the maximum depth level of the recursive download. If not specified, the default level will be 5.
* -p [PATH]: indicates the path where the downloaded files will be saved. If not specified, the default path will be ./data/.

The program will download the following file extensions by default:

* .jpg/jpeg
* .png
* .gif
* .bmp

### 💡 Examples

Download all images from a website:
```
python3 spider.py https://example.com -p ./images/
```
Download all images from a website and its linked pages:
```
python3 spider.py https://example.com -r -l 3 -p ./images/
```
Download all images from a local HTML file:
```
python3 spider.py ./index.html -p ./images/
```
### 📋 Notes
Spider will only download images with the extensions ".jpg", ".jpeg", ".png", ".gif", and ".bmp".
If an image is not downloaded, it may be due to incorrect file paths or permission issues.

-----------------------------------------------
## 🦂 SCORPION - Image Metadata Downloader

### 📝 Description
Scorpion is a Python program that downloads metadata from images. It uses the argparse and Pillow libraries to obtain image metadata and display it in a user-friendly way.

### 🛠️ Usage

To run Scorpion, simply execute the script followed by the path to the image you want to analyze. You can also provide additional paths to analyze multiple images.
```
python3 scorpion.py image1.jpg image2.png
```
```
python3 scorpion.py ./folder
```
### 💡 Example
Here is an example output from running Scorpion on an image:

Name           : test.jpg\n <br>
Dimensions     : 373, 373 <br>
Format         : PNG <br>
Mode           : RGBA <br>
Palette        : None <br>
Exif           : {} <br>
ImageWidth     : 373 <br>
ImageLength    : 373 <br>
Created        : 12/05/2023 18:44:22 <br>
Modified       : 12/05/2023 18:44:22 