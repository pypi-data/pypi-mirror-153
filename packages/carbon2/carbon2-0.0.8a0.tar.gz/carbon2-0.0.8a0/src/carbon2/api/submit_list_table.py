import hashlib
import os

from quick_crawler.browser import *
import uuid
from carbon2.api.submit import Carbon2Api
from tqdm import tqdm
from trafilatura import bare_extraction

def upload_to_server_with_table(server_url,table, user_id,target_url,driver_path="",save_folder="html_data",use_md5url_as_id=False,tag="",language="",publishtime="",
                     not_check_exists=False,
                     no_submit=False,no_submit_file=False,use_trafilatura=False,delete_after_uploaded=False):
    print("==========Begin Upload===============")
    print("UserId: "+user_id, ", Target Url:"+target_url)

    if driver_path=="" or not os.path.exists(driver_path):
        print("Chromedriver.exe is not set due to the invalid driver path; use conventional crawler instead. ")

    # carbon2system's url
    root_url = f"{server_url}/api"
    c2api = Carbon2Api(root_url)

    # the page url that you want to upload
    # target_url="http://xinhuanet.com/"

    # 1. Generate an unique ID
    page_id=""
    if use_md5url_as_id:
        unique_id=hashlib.md5(target_url.encode())
        page_id=str(unique_id.hexdigest())
    else:
        unique_id = uuid.uuid4()
        page_id=str(unique_id)

    print(f"Using ID: {page_id}...")

    # check if exists
    if not not_check_exists:
        if c2api.exists_url(target_url)==1:
            print(f"Url exists: {target_url}, skip the url.")
            return

    # 2. quick obtain an HTML page
    if driver_path=="" or not os.path.exists(driver_path):
        html_str=quick_html_page(target_url)
    else:
        html_str=get_html_str_with_browser(url=target_url,driver_path=driver_path,silent=True)
    if html_str=="":
        print("getting html page occurs error, empty html string, skip uploading")
        return

    if not os.path.exists(save_folder):
        print("Creating the folder: ", save_folder)
        os.mkdir(save_folder)
    saved_file_path=f"{save_folder}/{page_id}.txt"
    print("Saved file path: ", saved_file_path)
    f_out=open(saved_file_path,"w",encoding="utf-8")
    f_out.write(html_str)
    f_out.close()
    publisher=""
    remark=""
    # 2.1 get meta info
    if not use_trafilatura:
        meta_model = get_page_meta(html_str)
    else:
        meta_model={}
        content=bare_extraction(html_str)
        print("extracted content: ", content)
        # print(content.keys())
        meta_model["title"]=content["title"]
        if len(content["tags"])>0:
            meta_model["keywords"]=content["tags"][0]
        else:
            meta_model["keywords"]=""
        meta_model["description"]=content["description"]
        publishtime=content["date"]
        publisher=content["author"]
        # remark=content["categories"]


    # 3. submit the meta data

    r=c2api.submit_metadata_for_table(table,target_url,meta_model["title"],
                                      user_id,controller='NewsData', keywords=meta_model["keywords"],
                                      description=meta_model["description"], file_id=page_id,tag=tag,
                                      language=language,publishtime=publishtime,no_submit=no_submit,publisher=publisher)


    if r==1:
        # 4. submit the file with same unique id
        if not no_submit_file:
            r=c2api.submit_file(f"{save_folder}/{page_id}.txt")
        # 5. Verify if upload success
        download_url=f"{server_url}/WebData/{page_id}.txt"
        if not no_submit_file:
            if check_url_ok(download_url):
                print("Upload successfully")
        if os.path.exists(f"{save_folder}/{page_id}.txt"):
            os.remove(f"{save_folder}/{page_id}.txt")
    elif type(r)==dict:
        r["save_path"]=saved_file_path
        return r
    else:
        print("Upload error: the url may be repeated!")
    print("==========End Upload===============")



# the csv file must contain fields real_url, title.
def submit_page_list_with_table(server_url, table, user_id,csv_file,save_html_folder, use_md5url_as_id=False, driver_path="browsers/chromedriver.exe",tag="",language="",
                     url_field_name="real_url",publishtime="",try_raise_error=False,skip_rows=-1,
                    not_check_exists=False,
                     no_submit=False,
                     no_submit_file=False,
                            delete_after_uploaded=False,
                                use_trafilatura=True
                     ):
    list_model = quick_read_csv_model(csv_file, encoding='utf-8')
    list_result=[]
    for idx,model in enumerate(list_model):
        print(f"{idx + 1}/{len(list_model)}")
        if skip_rows!=-1:
            if idx<skip_rows:
                continue
        url = model[url_field_name]
        if try_raise_error:
            r=upload_to_server_with_table(server_url,table, user_id, url, use_md5url_as_id=use_md5url_as_id, driver_path=driver_path,use_trafilatura=use_trafilatura,
                                          delete_after_uploaded=delete_after_uploaded,
                             tag=tag, language=language, save_folder=save_html_folder, publishtime=publishtime,not_check_exists=not_check_exists,no_submit=no_submit,no_submit_file=no_submit_file)
            if no_submit:
                if r!=None:
                    list_result.append(r)
        else:
            try:
                r=upload_to_server_with_table(server_url,table,user_id, url,use_md5url_as_id=use_md5url_as_id,
                                              driver_path=driver_path,tag=tag,use_trafilatura=use_trafilatura,
                                              language=language,save_folder=save_html_folder,
                                              publishtime=publishtime,not_check_exists=not_check_exists,
                                              no_submit=no_submit,no_submit_file=no_submit_file,
                                                delete_after_uploaded = delete_after_uploaded
                                              )
                if no_submit:
                    if r!=None:
                        list_result.append(r)
                print()
            except Exception as err:
                print("【ERROR】")
                print("Error Info: ",err)
                print()
    return list_result