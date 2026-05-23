import os, uuid
from datetime import date, datetime, timedelta, time
from typing import Union

def show_toast(ctx:dict, title:str, mesg:str) -> dict:
    if not ctx:
        ctx = {}
        
    toast = {
        "title": title,
        "mesg": mesg
    }
    ctx["toast"] = toast    
    
    return ctx

def show_toast_2(title:str, mesg:str) -> dict:
    return {
        "toast":{
            "title": title,
            "mesg": mesg
        }
    }
    

def context_modal_delete(ctx:dict, title:str, mesg:str,delete_url:str,back_url:str) -> dict:
    if not ctx:
        ctx = {}
        
    ctx["is_delete"] = True
    ctx["delete_url"] = delete_url
    ctx["title"] = title
    ctx["mesg"] = mesg
    ctx["back_url"] = back_url
    
    return ctx


def custom_upload_path(instance, filename):
    ext = os.path.splitext(filename)[1]
    today = date.today().strftime("%Y%m%d")
    new_name = f"{today}-{uuid.uuid4().hex}{ext}"
    return os.path.join("attachments/", new_name)


def validate_file(file, form):
    pass


def str_into_date(*, date_str, dt_format="%Y-%m-%d %H:%M:%S.%f0", is_end=False) -> date:
    if not date_str:
        return None
    
    try:
        dt_obj = datetime.strptime(date_str, dt_format)
        if is_end:
            pass
    except Exception as e:
        print("Failed to parse string into date")
        print(e)
        return None
    
    return dt_obj.date()

def str_into_datetime(date_str, dt_format="%Y-%m-%d %H:%M:%S.%f0", is_end=False) -> Union[datetime, None]:
    if not date_str:
        return None
    
    try:
        str_datetime = datetime.strptime(date_str, dt_format)
        if is_end:
            str_datetime = datetime.combine(str_datetime, time(23,59,59))
    except Exception:
        print("Failed to convert str -> datetime, invalid input format")
        return None
    
    return str_datetime