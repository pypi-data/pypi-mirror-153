from IQS_algorithm.IQS_utils import funcIQS as IQS

def searchIQS(text, user_consumer_key, user_consumer_secret, user_access_token, user_access_token_secret,
            num_return_tweets=12, min_tweet_count=3, search_count=1, iterations=15, keywords_start_size=3,
            max_tweets_per_query=100, output_keywords_count=5):
    return IQS.searchIQS(text, user_consumer_key, user_consumer_secret, user_access_token, user_access_token_secret,
            num_return_tweets, min_tweet_count, search_count, iterations, keywords_start_size, max_tweets_per_query,
            output_keywords_count)

