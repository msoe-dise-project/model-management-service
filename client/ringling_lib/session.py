"""
Copyright 2023 MSOE DISE Project

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import os
import requests

BASE_URL_KEY = "RINGLING_BASE_URL"

base_url = os.environ.get(BASE_URL_KEY)
print(base_url)
class Session:
    def __init__(self, url=base_url):
        self.url = url

    def perform_connect_check(self):
        response = requests.get(self.url+"/healthcheck", timeout=0.5)
        response_json = response.json()
        return bool(response_json["database"]["connection"]["healthy"])

