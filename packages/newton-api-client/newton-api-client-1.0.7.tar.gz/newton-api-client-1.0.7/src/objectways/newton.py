import os
import json
import requests


class Newton:
    def __init__(self, api_key, api_url="https://api.objectways.com/v1"):
        #self.api_base = "https://api.objectways.com/v1"

        self.api_base = api_url

        self.__headers = {"Content-Type": "application/json", "api_key": api_key}

    @staticmethod
    def create_body(project_id: str, file_name: str, file_type: str, source: str, meta_data: dict=None, **kwargs):
        body = {
            'project_id': project_id,
            'file_name': file_name,
            'file_type': file_type,
            'source': source
        }
        if meta_data is not None:
            body['meta-data'] = meta_data
        body.update(kwargs)
        return body

    def add_task(self, body: dict):
        api_url = f"{self.api_base}/task"

        # request_body = self.__create_body(**body)
        res = requests.post(api_url, json=body, headers=self.__headers)
        if res.ok:
            return res.json()
        else:
            return res.text

    def add_bulk_tasks(self, body: dict):
        api_url = f"{self.api_base}/task_bulk"

        res = requests.post(api_url, json=body, headers=self.__headers)
        if res.ok:
            return res.json()
        else:
            return res.text

    def add_labels_to_task(self, task_id: str, body: dict):
        api_url = f"{self.api_base}/task/{task_id}"
        res = requests.put(api_url, json=body, headers=self.__headers)
        if res.ok:
            return res.json()
        else:
            return res.text

    def add_task_file(self, project_id: str, file_path: str, mime_type: str, annotations: str = None):
        api_url = f"{self.api_base}/task/file"
        if not os.path.isfile(file_path):
            print(f"ERROR: file not found {file_path}")
            return

        file_name = os.path.basename(file_path)
        files = dict(project_id=(None, project_id), upfile=(file_name, open(file_path, 'rb'), mime_type))
        if annotations is not None:
            files.update(annotations=(None, annotations))

        headers = self.__headers.copy()
        del headers['Content-Type']

        res = requests.post(api_url, files=files, headers=headers)
        if res.ok:
            return res.json()
        else:
            return res.text

    def get_task(self, task_id: str=None):
        api_url = f"{self.api_base}/task/{task_id}"

        res = requests.get(api_url, headers=self.__headers)       
        if res.ok:
            return res.json()
        else:
            return res.text

    def delete_task(self, task_id: str=None):
        api_url = f"{self.api_base}/task/{task_id}"

        res = requests.delete(api_url, headers=self.__headers)       
        if res.ok:
            return res.json()
        else:
            return res.text

    def get_tasks(self, project_id, task_id: str=None, file_name: str=None, file_type: str=None, trail: bool=False):
        api_url = f"{self.api_base}/task/list/{project_id}"

        params = {}
        if task_id is not None:
            params["task_id"] = task_id
        if file_name is not None:
            params["file_name"] = file_name
        if file_type is not None:
            params["file_type"] = file_type
        if trail == True:    
            params["trail"] = "true" 

        res = requests.get(api_url, params=params, headers=self.__headers)
        if res.ok:
            return res.json()
        else:
            return res.text

    def export_tasks(self, project_id: str=None):
        api_url = f"{self.api_base}/project/list/{project_id}"

        res = requests.get(api_url, headers=self.__headers)
        if res.ok:
            return res.json()
        else:
            return res.text
 
    def add_project(self, body: dict):
        api_url = f"{self.api_base}/project"

        # request_body = self.__create_body(**body)
        res = requests.post(api_url, json=body, headers=self.__headers)
        if res.ok:
            return res.json()
        else:
            return res.text

    def get_project(self, project_id):
        api_url = f"{self.api_base}/project/{project_id}"

        res = requests.get(api_url, headers=self.__headers)
        if res.ok:
            return res.json()
        else:
            return res.text

    def update_project(self, project_id, body: dict):
        api_url = f"{self.api_base}/project/{project_id}"

        res = requests.put(api_url, json=body, headers=self.__headers)
        if res.ok:
            return res.json()
        else:
            return res.text

    def delete_project(self, project_id):
        api_url = f"{self.api_base}/project/{project_id}"

        res = requests.delete(api_url, headers=self.__headers)
        if res.ok:
            return res.json()
        else:
            return res.text

    def get_projects(self, project_id: str=None, project_name: str=None, active: bool=None):
        api_url = f"{self.api_base}/project/list"

        params = {}
        if project_id is not None:
            params["project_id"] = project_id
        if project_name is not None:
            params["project_name"] = project_name
        if active is not None:
            params["active"] = json.dumps(active)

        res = requests.get(api_url, params=params, headers=self.__headers)
        if res.ok:
            return res.json()
        else:
            return res.text

    def add_team_member(self, project_id, email: str, role: str="annotator"):
        api_url = f"{self.api_base}/team/{project_id}"

        # request_body = self.__create_body(**body)
        params = {}
        if email is not None:
            params["email"]= email
        if role is not None:
            params["role"] = role

        res = requests.post(api_url, params=params, headers=self.__headers)
        if res.ok:
            return res.json()
        else:
            return res.text

    def get_project_team_members(self, project_id):
        api_url = f"{self.api_base}/team/{project_id}"

        # request_body = self.__create_body(**body)
        res = requests.get(api_url, headers=self.__headers)
        if res.ok:
            return res.json()
        else:
            return res.text

    def remove_project_team_member(self, project_id, email):
        api_url = f"{self.api_base}/team/{project_id}/{email}"

        res = requests.delete(api_url, headers=self.__headers)
        if res.ok:
            return res.json()
        else:
            return res.text