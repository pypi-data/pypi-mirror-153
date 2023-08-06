# please install multipledispatch 0.6.0
from io import TextIOWrapper
import requests
from urllib.parse import urljoin
import json
import polling2
import subprocess


class Error():
    def __init__(self, res = None, proc_msg = None):
        self.status_code = None
        self.packaging_msg = None
        self.program_msg = proc_msg
        self.res = res

        if self.res is not None:
            self.status_code = res.status_code
            self.packaging_msg = res.content
            print(self.packaging_msg)
    
    @property
    def status_msg(self):
        # 4xx error -> client error, 5xx error -> server error
        if self.status_code == 400:
            return f"Bad Request({self.status_code})! Try again."
        elif self.status_code == 401:
            return f"Unauthorized({self.status_code})! Try again."
        elif self.status_code == 403:
            return f"Forbidden({self.status_code})! Try again."
        elif self.status_code == 404:
            return f"Not Found({self.status_code})! Try again."
        elif self.status_code == 500:
            return f"Internal Server Error({self.status_code})! - {self.packaging_msg}"
        else:
            return f"Unknown Error. Original error message - {self.packaging_msg}"

class PackagingServer():
    def __init__(self, addr, port, network_request_time_out=5):
        self.address = f"http://{addr}:{port}/"
        self.timeout = network_request_time_out

    def _check_status(self, res):
        if res.status_code >= 400: # More than 400 is seen as an issue on the device farm side.
            return False
        else:
            return True

    def _poll(self, add_str, method, files=None, data=None, params=None, headers=None):
        headers = {'Authorization' : 'nota_devtest'}
        res = None
        try:
            if method == "get":
                res = requests.get(
                        headers=headers,
                        url=urljoin(self.address, add_str),
                        files=files,
                        data=data,
                        params=params
                    )
            else:
                res = requests.post(
                        headers=headers,
                        url=urljoin(self.address, add_str),
                        files=files,
                        data=data,
                        params=params
                    )
                    
            if res.status_code != 200:
                raise Exception
        except:
            return res, Error(res, res.content.decode('utf-8'))
        return res, None
    
    def get_list(self, folder_name: str = None):
        params = {
            "folder": folder_name
        }
        res, error = self._poll(add_str=f"list", method="get", params=params)
        if error is not None:
            return None, error
        res = json.loads(res.content.decode('utf-8'))
        lists = []
        [lists.append(res["objects"][i]) for i in range(0, len(res["objects"]))]
        return lists, None

    def build_package(self, data: dict, source: TextIOWrapper, model_file: TextIOWrapper = None):
        file_list = [("source", source), ("model_file", model_file)]
        res, error = self._poll(add_str=f"build", method="post", data=data, files=file_list)
        if error is not None:
            return error
        return None

    def download_package(self, file_name: str, get_url: bool):
        params = {
            "file_name": file_name,
            "get_url": get_url
        }
        res, error = self._poll(add_str=f"download", method="get", params=params)
        if get_url is False:
            # file_name = file_name.split('/')
            # link = res.content.decode('utf-8')
            # print(link)
            # command = f"curl \"{link}\" --output {file_name[1]}"
            # print(command)
            # build_result = subprocess.check_output(command, shell=True, universal_newlines=True, timeout=60*60)

            # save binary to file
            file_name = file_name.split('/')
            with open(f'{file_name[1]}', 'wb+') as out_file:
                out_file.write(res.content)

        if error is not None:
            return None, error
        return res.content, None