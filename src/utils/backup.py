import os
from datetime import datetime
import pandas as pd

def save_parquet(df, file_name, file_dir, attach_timestamp=True, postfix=""):
    file_name = '.parquet'.join([chunk for chunk in file_name.split('.parquet')])

    if attach_timestamp:
        timestamp = ''.join(str(datetime.now()).split('.')[:-1]).replace('-', '_').replace(':', '_').replace('.', '_').replace(' ', '_').replace('_', '')
        file_name += f"_{timestamp}"

    if postfix:
        file_name += f"_{postfix}"

    path = os.path.join(file_dir, f"{file_name}.parquet")
    df.to_parquet(path)
    print(f"Saved parquet file on: {path}")


def load_parquet(file_name, file_dir):
    path = os.path.join(file_dir, file_name)

    if not os.path.exists(path) or file_name.split('.')[-1] != 'parquet':
        return

    return pd.read_parquet(path)
