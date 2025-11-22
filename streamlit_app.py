import streamlit as st
import pandas as pd
import boto3
import io

AWS_ACCESS_KEY_ID = st.secrets['aws']["aws_access_key_id"]
AWS_SECRET_ACCESS_KEY = st.secrets['aws']["aws_secret_access_key"]

region_name = 'us-west-2'

bucket_name = 'algo-ai-data-bucket'
s3_file_name = 'day_trades/box_method_entries_running.csv'
s3 = boto3.client('s3',
                        aws_access_key_id=AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                        region_name=region_name)

@st.cache_data(ttl=60)  # caches for 1 minute
def load_csv_from_s3():
    obj = s3.get_object(Bucket=bucket_name, Key=s3_file_name)
    return pd.read_csv(io.BytesIO(obj['Body'].read()))

df = load_csv_from_s3()

cols = [
    'Ticker', 'Signal Type', 'Entry Date', 'Entry Time PST', 'Daily Close', 
    'Box Min', 'Box Max', 'Gap Pct', 
]
df = df[cols]
#sort df by entry date and entry time descending
df = df.sort_values(by=['Entry Date', 'Entry Time PST'], ascending=[False, False])

st.title('Box method entries')
#st.dataframe(df)

#in streamlit, stretch dataframe to full width
st.dataframe(df.reset_index(drop=True), use_container_width=True, height=800)
