# Libraries
import argparse, os, datetime
from PIL import Image
from PIL.ExifTags import TAGS

# Program
def analyzer():
    parser = argparse.ArgumentParser(prog="./scorpion", description="Download image metadata.")
    parser.add_argument("IMAGE", help="Image to analyze", type=str)
    parser.add_argument("IMAGES", help="Images to analyze.", nargs="*")

    # Obtains arguments
    return parser.parse_args()

# Extract metadata
def scorpion(paths):
    for path in paths:
        try:
            # Open image
            image = Image.open(path)
        except:
            print(f"Could not open {path}.")
        else:
            # Show metadata
            print(f"{'Name':15}: {image.filename.split('/')[-1]}")
            print(f"{'Dimensions':15}: {image.size[0]}, {image.size[1]}")
            print(f"{'Format':15}: {image.format}")
            print(f"{'Mode':15}: {image.mode}")
            print(f"{'Palette':15}: {image.palette}")
            print(f"{'Exif':15}: {image.getexif()}")
            print(f"{'ImageWidth':15}: {image.width}")
            print(f"{'ImageLength':15}: {image.height}")

            # Extract metadata
            data = image.getexif()

            if data:
                # Show metadata
                for id in data:
                    try:
                        name = TAGS.get(id)
                        value = data.get(id)
                        print(f"{name:32}: {value}")
                    except Exception:
                        print(f"Label {id} not found.")

            # Show file timestamps
            created = datetime.datetime.fromtimestamp(os.path.getctime(path))
            modified = datetime.datetime.fromtimestamp(os.path.getmtime(path))
            created_formatted = created.strftime("%d/%m/%Y %H:%M:%S")
            modified_formatted = modified.strftime("%d/%m/%Y %H:%M:%S")
            print(f"{'Created':15}: {created_formatted}")
            print(f"{'Modified':15}: {modified_formatted}")

            print("-" * 80)

if __name__ == "__main__":
    args = analyzer()

    locations = list()
    locations.append(args.IMAGE)
    locations += args.IMAGES

    # Add all images in folder to locations list
    if os.path.isdir(args.IMAGE):
        for filename in os.listdir(args.IMAGE):
            file_path = os.path.join(args.IMAGE, filename)
            if os.path.isfile(file_path):
                locations.append(file_path)

    scorpion(locations)
