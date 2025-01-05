# from utilsimport UPBIT_REST_API_BASE
from forecast import DataLoader, Trainer, RandomForestModel, Dataset
import numpy as np
import asyncio

async def main():
    model = RandomForestModel()
    
    data = await DataLoader.load_candles(
        market='KRW-IOTA', 
        unit='second', 
        count=200000
    )
    X, y = DataLoader.make_input_output(
        DataLoader.preprocess(data), 
        columns_X=[
            'variance', 
            'worst_profit_rate_before', 
            'opening_price', 
            'high_price', 
            'mid_price', 
            'low_price', 
            'candle_acc_trade_volume', 
            'timedelta_after'
        ], 
        columns_y=['best_profit_rate'],
    )

    trainer = Trainer(model, Dataset(X, y), valid_ratio=0.15)
    
    trainer.train()
    trainer.validate()


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