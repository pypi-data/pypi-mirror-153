# __all__ = ('dfapi')
import pandas as pd
import requests

def dfapi(tbname, ind_col_name = ""):
  """ 
  call to api endpoint on regression.fit database to access datasets
  :param str tbname: table name that exist on the server 
  :param str ind_col_name: optional, name of index column 
  :return: pandas.Dataframe
  """
  
  df = None # set a global variable to store the dataframe
  apikey = 'K35wHcKuwXuhHTaz7zY42rCje'
  parameters = {"apikey": apikey, 'table': tbname }
  heads = { "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0" } # server has ModSecurity check if it is a browser request. 
  js = {'error': 'Initialize' }

  try:
    response = requests.get("http://api.regression.fit/endpt.json", params=parameters, headers=heads)
    js = response.json()
  except BaseException as err: print(f'Error while connecting to regession.fit API. Please contact the administrator. {err=}, {type(err)=}')

  if ('error' in js) : 
    print(f'Error: {js["error"]} Please contact the administrator.') # The json object will have a key named "error" if not successful
    return df
  
  # json object seems okay at this point
  try: df = pd.DataFrame(js) 
  except ValueError: print(f'Value Error while converting json into dataframe. Please contact the administrator.')
  except BaseException as err: print(f'Error while converting json into dataframe. Please contact the administrator. {err=}, {type(err)=}')
  
  # df seems load okay at this point. Default values is object/string everywhere.
  # try to convert all possible ones to numeric
  for col in df.columns:
    try: df[col]=pd.to_numeric(df[col])
    except ValueError: pass
    except: pass

  # set index if given
  # if (ind_col_name and ind_col_name in df): df.set_index(ind_col_name, inplace=True)  # if given col_name exist, make it the index.
  try: df.set_index(ind_col_name, inplace=True)
  except ValueError: pass
  except TypeError: pass
  except: pass
  
  print(f'Dataframe from Regression.Fit API is loaded.')
  return df

# print("\nFunction api_rfit loaded. Ready to continue.")

