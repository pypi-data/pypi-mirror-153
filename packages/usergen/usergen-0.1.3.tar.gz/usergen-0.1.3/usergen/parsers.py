import io
import pandas as pd

def parse_json(response):
    response_json = response.json()
    return response_json['results'][0]

def parse_csv(response):
    response_csv = response.text
    df = pd.read_csv(io.StringIO(response_csv), header=0)
    df.columns = df.columns.str.replace('.', '_', regex=False)
    return df
