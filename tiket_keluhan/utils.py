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
    