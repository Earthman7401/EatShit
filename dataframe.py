import pandas as pd
import json

def writedf(path: str):
    """
    Args:
        path (str): path of the json file you want to convert into pandas dataframe
    """    
    #how data stores: [{'key1':[value1]}, 'key2':[value2]}, etc]
    df_info = open(path, encoding="utf-8", mode='r')
    df_append = json.load(df_info)
    data = {}
    for i in range(len(df_append)):
        df = df_append[i]
        d = list(df.keys())
        dict_key = d[0]
        dict_value = df[dict_key]
        j = {dict_key:dict_value}
        data.update(j)
    output = pd.DataFrame.from_dict(data, orient='columns')
    return output