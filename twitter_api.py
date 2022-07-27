import requests
import time
import pandas as pd


def send_request(access_token, keyword, start_date, end_date):
    base = "https://api.twitter.com/2/tweets/search/all"
    query = f"?query=" + keyword + "-is:retweet lang:en"
    max_results = "&max_results=100"
    time_duration = f"&start_time=" + start_date + "T00%3A00%3A00Z&end_time=" + end_date + "T11%3A59%3A59Z"
    expansions = "&expansions=author_id"
    tweet_fields = "&tweet.fields=created_at"
    url = base + query + max_results + time_duration + expansions + tweet_fields
    twitter_search(url, access_token)
    return (url)


# To find the next token from the response file
def has_next_page(response_json):
    if "next_token" in response_json["meta"]:
        return True
    return False


def twitter_search(url, access_token):
    token = access_token
    headers = {"Authorization": f"Bearer {token}"}
    response_json = requests.get(url, headers=headers).json()
    df = pd.DataFrame(response_json['data'])
    while (has_next_page(response_json)):
        data = response_json["meta"]["next_token"]
        main_url = url
        url = url + f"&next_token={data}"
        time.sleep(4)
        response_json = requests.get(url, headers=headers).json()
        df = df.append(response_json['data'])
        print(len(df))
        url = main_url
    df.reset_index(drop=True, inplace=True)
    return (df)
