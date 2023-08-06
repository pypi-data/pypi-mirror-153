import time

from autobr.baidu import BaiduNewsSearch
from carbon2.api.submit_list_table import *

def fetch_news(config_path):
    f_in=open(config_path,"r",encoding='utf-8')
    lines=f_in.readlines()
    config={}
    for line in lines:
        line=line.strip()
        index=line.index(":")
        key=line[:index].strip()
        value=line[index+1:].strip()
        config[key]=value
        print(f"{key}\t{value}")
    while True:
        save_path=config["save_path"]
        baidu_news = BaiduNewsSearch(
            webdriver_path=config["browser_path"]
        )

        list_keywords=config["keywords"].split(";")
        for k in list_keywords:
            try:
                # fetch news
                new_save_path=save_path.replace("{keyword}",k)
                baidu_news.fetch(raw_keywords=k,
                                 max_pages=int(config["max_page"]),
                                 silent=config["silent"],
                                 save_path=new_save_path)
                # upload data
                server_url = config["server_url"]
                user_id = config["uploader"]
                csv_file = new_save_path
                save_folder =config["html_data_path"]
                submit_page_list_with_table(server_url, "dc", user_id, csv_file, save_html_folder=save_folder,
                                            use_md5url_as_id=True,
                                            driver_path=config["browser_path"], tag=config["tag"], language="zh",
                                            url_field_name='real_url', try_raise_error=True,delete_after_uploaded=bool(config["delete"]))
            except Exception as err:
                print(err)

        print("waiting for next fetch...")
        time.sleep(int(config["wait"]))

