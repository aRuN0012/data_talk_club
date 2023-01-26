#!/usr/bin/env python
# coding: utf-8

import argparse
import pandas as pd
from sqlalchemy import create_engine
from time import time
import sys,os




def ingestion(args):

    host=args.host
    db_name=args.db_name
    user=args.user
    password=args.password
    table_name=args.table_name
    url=args.url
    port=args.port
    if url.endswith('.csv.gz'):
        file_name = 'output.csv.gz'
    else:
        file_name = 'output.csv'
    print(url)
    engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(user,password,host,port,db_name))
    engine.connect()
    os.system("wget {} -O {}".format(url,file_name))
#    df=pd.read_parquet(parq_file_name)
#    df.to_csv(csv_file_name)
    df = pd.read_csv(file_name,iterator=True, chunksize=100000)
    dfi=next(df)
   # dfi.lpep_pickup_datetime = pd.to_datetime(dfi.lpep_pickup_datetime)
    #dfi.lpep_dropoff_datetime = pd.to_datetime(dfi.lpep_dropoff_datetime)
    dfi.head(n=0).to_sql(name=table_name, con=engine,if_exists='replace')
    dfi.to_sql(name=table_name, con=engine, if_exists='append')
    while True:
        s_time=time()
        dfi=next(df)
        #dfi.lpep_pickup_datetime=pd.to_datetime(dfi.lpep_pickup_datetime)
        #dfi.lpep_dropoff_datetime=pd.to_datetime(dfi.lpep_dropoff_datetime)
        dfi.to_sql(name=table_name,con=engine,if_exists='append')
        e_time=time()
        print('chunch inserted time {}'.format(e_time-s_time))


if __name__=='__main__':


#host, user,password,port,url,db_name,table_name,port

    parser = argparse.ArgumentParser(description='Ingestion script.')
    parser.add_argument('--host',help='Host name')
    parser.add_argument('--db_name', help='data base name')
    parser.add_argument('--user', help='user name')
    parser.add_argument('--password', help='password')
    parser.add_argument('--table_name', help='table name')
    parser.add_argument('--url', help='taxi data download url')
    parser.add_argument('--port', help='port')


    args = parser.parse_args()
    ingestion(args)




