import pandas as pd
import json
import random
from datetime import datetime, time, timedelta
from random import randrange


#%%
linked_in=pd.read_json('',orient='records')
#%%
users_df=pd.read_csv('/Users/sw08/Downloads/user_interactions.csv')

user=users_df['USER_ID'].to_list()

#%%
def random_date(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    date = start + timedelta(seconds=random_second)
    return datetime.timestamp(date)

def get_random_timestamp():
    d1 = datetime.strptime('1/1/2021 1:30 PM', '%m/%d/%Y %I:%M %p')
    d2 = datetime.strptime('1/1/2022 4:50 AM', '%m/%d/%Y %I:%M %p')
    return random_date(d1,d2)
#%%
time=[]
for i in range(5000):
    time.append(int(get_random_timestamp()))
#%%
job_id_list=final_df['Job ID'].to_list()

interactions=[]
for i in user:
  job_id=random.choices(job_id_list,k=5000)

final = pd.DataFrame(list(zip(user,job_id,time)),columns =['USER_ID','ITEM_ID','TIMESTAMP'])

#%%
final.to_csv('/Users/sw08/Downloads/user_interactions2.csv')
#%%

with open('/Users/sw08/Desktop/AWS/push_to_dynamodb/final.json', 'r') as f:
        data = json.load(f)
#%%
country=[]
desc=[]
exp=[]
job_id=[]
location=[]
title=[]
url=[]
for i in range(len(data['Jobs_data'])):
    country.append(data['Jobs_data'][i]['PutRequest']['Item']['country']['S'])
    desc.append(data['Jobs_data'][i]['PutRequest']['Item']['description']['S'])
    exp.append(data['Jobs_data'][i]['PutRequest']['Item']['experience_level']['S'])
    job_id.append(data['Jobs_data'][i]['PutRequest']['Item']['job_id']['S'])
    location.append(data['Jobs_data'][i]['PutRequest']['Item']['location']['S'])
    title.append(data['Jobs_data'][i]['PutRequest']['Item']['title']['S'])
    url.append(data['Jobs_data'][i]['PutRequest']['Item']['url']['S'])
#%%

final_df = pd.DataFrame(list(zip(job_id,title,exp,desc,location,country,url)),columns =['Job_ID','Title','Experience_level','Description','Location','Country','url'])
#%%
print(final_df['Job_ID']=='3053421576')
#%%
val=final_df[final_df.eq("3053421576'").any(1)]
#%%
users_df=pd.read_csv('/Users/sw08/Downloads/user_interactions.csv')

user=users_df['USER_ID'].to_list()

job_id_list=final_df['Job_ID'].to_list()

interactions=[]
for i in user:
    job_id=random.choices(job_id_list,k=5000)
#%%
with open('/Users/sw08/Desktop/AWS/untitled folder/companies.json', 'r') as f:
        data = json.load(f)
#%%
companies=[]
job_id=[]
for k,v in data.items():
    companies.append(v)
    job_id.append(k)
#%%
comp_df=pd.DataFrame(list(zip(job_id,companies)),columns =['Job_ID','Company'])
#%%
res_df=pd.merge(final_df,comp_df,on='Job_ID')

#%%
res_df.to_csv('/Users/sw08/Downloads/linkedin.csv')