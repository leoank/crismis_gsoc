import multiprocessing as mp
from multiprocessing import Pool, Process, Queue, freeze_support
import logging
import requests
from bs4 import BeautifulSoup
import os
import json
import time

# fetch messenger data page
messenger_data_page_url = "https://pdsimage2.wr.usgs.gov/archive/mess-e_v_h-mdis-2-edr-rawdata-v1.0/MSGRMDS_1001/DATA/"
messenger_data_page = requests.get(messenger_data_page_url)
messenger_data_page_soup = BeautifulSoup(messenger_data_page.content, features="html.parser")


import re


def create_year_doy_dict(messenger_data_page_soup):
    
    # extarct all links from the page
    links = [element.contents[0] for element in messenger_data_page_soup.find_all('a')]
    year_doy_dict = dict()
    for link in links:
        # filter out links with pattern {YEAR}_{DOY}
        if re.search(r'\d{4}_\d{3}/', link):
            key, value = link.replace('/','').split('_')
            # Add key to dict if not already exist
            if key not in year_doy_dict:
                year_doy_dict[key] = []
            year_doy_dict[key].append(value)
    return year_doy_dict

def generate_doy_data_page_url(YEAR, DOY):
    # check if YEAR and DOY are available
    year_doy_dict = create_year_doy_dict(messenger_data_page_soup)
    url = f"https://pdsimage2.wr.usgs.gov/archive/mess-e_v_h-mdis-2-edr-rawdata-v1.0/MSGRMDS_1001/DATA/{YEAR}_{DOY}/"
    return url

def create_year_doy_images_dict(year_doy_dict):
    path = os.path.join(os.path.dirname(__file__), "year_doy_images.json")
    print(path)
    # Check and return if a previously fetched year_doy_images_dict exist on disk
    if os.path.exists(path):
        fp = open(path)
        year_doy_images_dict = json.load(fp)
        return year_doy_images_dict
    # Start fetching
    print("This will take time. Have patience...")
    year_doy_images_dict = dict()
    for year in year_doy_dict:
        year_doy_images_dict[year] = {}
        for doy in year_doy_dict[year]:
            print(f'fetching links for year: {year} and DOY: {doy}')
            year_doy_images_dict[year][doy] = []
            # fetch image data page
            url = generate_doy_data_page_url(year, doy)
            try:
                year_doy_page = requests.get(url)
            except:
                print(f"Encountered error while fetching url: {url}")
                print("Sleeping for 10 secs...")
                time.sleep(10)
                print("Resuming fetching...")
                year_doy_page = requests.get(url)
            year_doy_page_soup = BeautifulSoup(year_doy_page.content, 'html.parser')
            links = [element.contents[0] for element in year_doy_page_soup.find_all('a')]
            
            for link in links:
                # filter out links with pattern .IMG$
                if re.search(r'.IMG$', link):
                    year_doy_images_dict[year][doy].append(link)
    print('done!')
    # Save year_doy_images_dict to disk as a json file
    json.dumps(year_doy_images_dict, open(path))
    return year_doy_images_dict

def download_image(year, doy, image):
    # Create download url
    url = f"https://pdsimage2.wr.usgs.gov/archive/mess-e_v_h-mdis-2-edr-rawdata-v1.0/MSGRMDS_1001/DATA/{year}_{doy}/{image}"
    try:
        img = requests.get(url)
    except:
        print(f"Encountered error while Downloading url: {url}")
        print("Sleeping for 10 secs...")
        # Wait a little before retrying
        time.sleep(10)
        print("Resuming Download...")
        img = requests.get(url)
    # Create dirs if not already present
    path = os.path.realpath(os.path.join(os.path.realpath(os.path.dirname(__file__)), os.path.realpath(f"../../notebooks/data/{year}/{doy}/{image}")))
    if not os.path.exists(path):
        os.makedirs(path)
    # Save file to disk
    open(path,"wb").write(img.content)
    
def threaded_download_image_with_check(download_queue):
    while not download_queue.empty():
        (image, year, doy) = download_queue.get()
        # continue loop to next iter if file already present on disk
        path = os.path.realpath(os.path.join(os.path.realpath(os.path.dirname(__file__)), os.path.realpath(f"../../notebooks/data/{year}/{doy}/{image}")))
        print('Path is: '+ path)
        if os.path.exists(path):
            continue
        # Create download url    
        url = f"https://pdsimage2.wr.usgs.gov/archive/mess-e_v_h-mdis-2-edr-rawdata-v1.0/MSGRMDS_1001/DATA/{year}_{doy}/{image}"
        try:
            # Add some logging
            logger = mp.get_logger()
            proc = os.getpid()
            logger.warning(f"Proc: {proc} Downloading image: {image} year: {year} doy: {doy}")
            # Download image
            img = requests.get(url)
        except:
            print(f"Encountered error while Downloading url: {url}")
            print("Sleeping for 10 secs...")
            # Wait a little before retrying
            time.sleep(10)
            print("Resuming Download...")
            # Retry to download image
            img = requests.get(url)
        # Create dirs if not already present
        if not os.path.exists(path):
            os.makedirs(path)
        # Save file to disk
        open(path,"wb").write(img.content)
    return True
    
def download_image_all(year_doy_image_dict):
    print("This will take a lot of time\n\nKeep lots of coffee handy!!")
    print("You can resume your downloads by running this function again.")
    print("So don't panic if download gets interrupted.")
    
    # After few attempts to download the dataset, it is clear we need threading for speed
    # Using a single connection at a time for downloading is too slow
    
    #Construct a inversed list with image links at root
    # this will help in easily distributing worload evenly with threading
    inversed_year_doy_image_dict = dict()
    for year in year_doy_image_dict:
        for doy in year_doy_image_dict[year]:
            for image in year_doy_image_dict[year][doy]:
                # Only download images if they are not already downloaded
                inversed_year_doy_image_dict[image] = [year, doy]
    
    # Create a task queue to share among processes
    download_queue = Queue()
    for key in inversed_year_doy_image_dict:
        download_queue.put((key, inversed_year_doy_image_dict[key][0], inversed_year_doy_image_dict[key][1]))
    
    # with Pool(2) as pool:
    #     for n_proc_i in range(2):
    #         result = pool.apply_async(threaded_download_image_with_check, download_queue)
    download_processes = []
    for n_proc_i in range(int(mp.cpu_count())/2):
        download_process = Process(target=threaded_download_image_with_check, args=(download_queue,))
        download_processes.append(download_process)
        download_process.start()
    print(download_processes)
    for download_process in download_processes:
        download_process.join()

if __name__ == "__main__":
    mp.set_start_method('spawn')
    year_doy_dict = create_year_doy_dict(messenger_data_page_soup)
    year_doy_images_dict = create_year_doy_images_dict(year_doy_dict)
    download_image_all(year_doy_images_dict)