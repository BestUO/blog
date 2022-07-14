import requests
import os
from pathlib import Path

if __name__ == "__main__":
    f = Path("./public/img/47d3cdd3176aa318be61d578c5347adab.jpg")
    uploadfile = {
        # 'filename': (None, '123.jpg'),
        # "file":(("123.jpg",open(path,"rb")),"image/jpg")
        "file": ("123.jpg", f.read_bytes(), "image/jpg")
    }
    requests.post(url="http://127.0.0.1:9999/api/uploadfile",files=uploadfile)