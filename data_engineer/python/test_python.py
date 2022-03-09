import requests
import json
import pandas as pd


def request_json(url):
    try:
        res = requests.get(
            url
                           )
        data = res.json()
    except Exception as e:
        print("Exception (forecast):", e)
        pass
    return data

post_json = request_json('http://jsonplaceholder.typicode.com/posts')
comments_json = request_json('http://jsonplaceholder.typicode.com/comments')
post_data = [[] for _ in range(len(post_json))]
n=0
for i in post_json:
    post_data[n] = [i['userId'],i['id']]
    n+=1
n=0
comments_data = [[] for _ in range(len(comments_json))]
for i in comments_json:
    comments_data[n] = [i['postId'],i['id']]
    n+=1
post_df =  pd.DataFrame(post_data, columns=['userId', 'id'])
comments_df =  pd.DataFrame(comments_data, columns=['id', 'comment_id'])
result_df = comments_df.merge(post_df, on="id", how="left")
x=result_df.groupby(['userId','id']).size().reset_index(name='counts')