from typing import Union, Optional
from datetime import datetime
from dateutil import tz

def kst_time(
    dt: Optional[Union[datetime, str]] = None, 
    format: Optional[str] = '%Y-%m-%dT%H:%M:%S',
    is_utc: Optional[bool] = False
  ) -> str:
  if (not dt):
    dt = datetime.now()
  
  if isinstance(dt, str):
    if format:
      dt = datetime.strptime(dt, format)
    else:
      raise ValueError("If dt is a string, format must be provided")
    
    if is_utc:
      dt = dt.replace(tzinfo=tz.tzutc()).astimezone(tz.gettz('Asia/Seoul'))
  
  return dt.strftime('%Y-%m-%dT%H:%M:%S+09:00')
  # return f"{'T'.join(str(dt).split('.')[0].split(' '))}+09:00"
