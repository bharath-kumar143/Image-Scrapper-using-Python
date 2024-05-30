import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def fetch_images(url, output_folder="images"):
    # It Also Creates the folder named with Image if it even doesn't Exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Here these is for webpage content
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Soup helps in finding all the tags
    img_tags = soup.find_all("img")

    # Download each image
    for img in img_tags:
        img_url = img.get("src")
        if not img_url:
            continue

        # Accepts only URl Structure
        img_url = urljoin(url, img_url)

        # Get the image file name
        img_name = os.path.basename(img_url)

        # Save the image in Images Directory
        img_response = requests.get(img_url, stream=True)
        if img_response.status_code == 200:
            img_path = os.path.join(output_folder, img_name)
            with open(img_path, "wb") as f:
                for chunk in img_response.iter_content(1024):
                    f.write(chunk)
            print(f"Successfully downloaded {img_name}")
        else:
            print(f"Failed to retrieve image from {img_url}")


# Given the website url
fetch_images("https://hamaredr.com")
