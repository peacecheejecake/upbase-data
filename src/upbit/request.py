from utils.Request import Request
from utils.env import UPBIT_REST_API_BASE

if (UPBIT_REST_API_BASE):
  request = Request(UPBIT_REST_API_BASE)
