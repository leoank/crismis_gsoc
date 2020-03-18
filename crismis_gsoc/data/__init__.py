import multiprocessing as mp
from .download import create_year_doy_dict, create_year_doy_images_dict, download_image_all


def start_download():
    mp.set_start_method('spawn')
    year_doy_dict = create_year_doy_dict(messenger_data_page_soup)
    year_doy_images_dict = create_year_doy_images_dict(year_doy_dict)
    download_image_all(year_doy_images_dict)