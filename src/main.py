# from utilsimport UPBIT_REST_API_BASE
# from forecast import DataLoader, Trainer, RandomForestModel, Dataset
# import numpy as np
import asyncio
from app import App

async def main():
    _app = App()
    await _app.initialize()
    app = _app.app
  
    @app.get('/predict/betsProfitRate')
    async def predict_betsProfitRate():
        # return _app.predict()
        return {'message': 'Hello World'}


if __name__ == '__main__':
    # import os
    # from dotenv import load_dotenv
    # import pandas as pd
    # from datetime import datetime
    

    asyncio.run(main())
    # main()
    # from utils.backup_to_file import save_parquet, load_parquet

    # load_dotenv(verbose=True)

    # # Load data
    # df = load_parquet('upbit_btc_krw_1m_2021_06_01_2021_06_30', 'data')
    # print(df)
    # print(df.info())

    # # Save data
    # save_parquet(df, 'upbit_btc_krw_1m_2021_06_01_2021_06_30', 'data', attach_timestamp=True, postfix='test')