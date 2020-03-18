import multiprocessing as mp
from .download import create_year_doy_dict, create_year_doy_images_dict, download_image_all
from bs4 import BeautifulSoup


def start_download():
    # fetch messenger data page
    messenger_data_page_url = "https://pdsimage2.wr.usgs.gov/archive/mess-e_v_h-mdis-2-edr-rawdata-v1.0/MSGRMDS_1001/DATA/"
    messenger_data_page = requests.get(messenger_data_page_url)
    messenger_data_page_soup = BeautifulSoup(messenger_data_page.content, features="html.parser")
    mp.set_start_method('spawn')
    year_doy_dict = create_year_doy_dict(messenger_data_page_soup)
    year_doy_images_dict = create_year_doy_images_dict(year_doy_dict)
    download_image_all(year_doy_images_dict)