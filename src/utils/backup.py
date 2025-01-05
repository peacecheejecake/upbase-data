from typing import Optional
import os
from pathlib import Path
from datetime import datetime
import pandas as pd

default_path = os.path.join(Path(__file__).parent.parent.parent, 'data')

def save_parquet(df: pd.DataFrame, file_name: str, file_dir: Optional[str] = None, attach_timestamp: Optional[bool] = True, postfix: Optional[str] = ""):
    file_name = '.parquet'.join([chunk for chunk in file_name.split('.parquet')])
    
    if attach_timestamp:
        timestamp = ''.join(str(datetime.now()).split('.')[:-1]).replace('-', '_').replace(':', '_').replace('.', '_').replace(' ', '_').replace('_', '')
        file_name += f"_{timestamp}"

    if postfix:
        file_name += f"_{postfix}"
        
    if not file_dir:
        file_dir = default_path

    path = os.path.join(file_dir, f"{file_name}.parquet")
    df.to_parquet(path)
    print(f"Saved parquet file on: {path}")


def load_parquet(file_name: str, file_dir: Optional[str] = None):
    if not file_dir:
        file_dir = default_path
        
    path = os.path.join(file_dir, file_name)

    if not os.path.exists(path) or file_name.split('.')[-1] != 'parquet':
        return

    print(f'Loading parquet file from: {path}')

    return pd.read_parquet(path)
