from typing import Optional
import requests
from .dict import dict_union

class Request:

  def __init__(self, base_url: str):
    self.base_url = base_url

  def default_headers(self):
    return {"accept": "application/json"}

  def full_url(self, path):
    return f"{self.base_url}{path}"

  def get(self, url, params: Optional[dict] = {}, headers: Optional[dict] = {}):
    # print(f'GET {self.full_url(url)}')
    response = requests.get(
      url=self.full_url(url),
      params=params,
      headers=dict_union(self.default_headers(), headers),
    )
    # print(f'GET RESPONSE {response.status_code}, {response.json()}')

    if (response.status_code != 200):
      raise Exception(f"GET {self.full_url(url)} failed: {response.status_code}, {response.json()}")
    
    return response.json()

  def post(self, url, body: Optional[dict] = {}, headers: Optional[dict] = {}):
    response = requests.post(
      url=self.full_url(url),
      headers=dict_union(self.default_headers(), headers),
      data=body
    )
    return response.json()
    