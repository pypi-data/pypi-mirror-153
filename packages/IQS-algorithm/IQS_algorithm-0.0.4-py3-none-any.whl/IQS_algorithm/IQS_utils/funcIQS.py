import os
import random
import re
import string
import timeit
from collections import Counter, defaultdict
from pathlib import Path
import nltk
import tweepy
from dotenv import load_dotenv
# nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet')
# nltk.download('pros_cons')
# nltk.download('reuters')
# nltk.download('maxent_ne_chunker')
# nltk.download('words')
# nltk.download('stopwords')
# nltk.download('universal_tagset')
from nltk.corpus import wordnet, stopwords
import numpy as np
from nltk import pos_tag
from scipy.spatial.distance import cdist
from gensim.models import FastText
import gensim
# import twint
import uuid
import json
from tqdm.auto import tqdm
import requests
from IQS_algorithm.IQS_utils import RelevantFiles
import importlib_resources as pkg_resources


def remove_unprintable_chars(word):
    new_word = word
    for x in word:
        if x not in string.printable:
            new_word = new_word.replace(x, '')
    return new_word


def remove_punctuation_chars(word):
    new_word = remove_unprintable_chars(word)
    if new_word.isdigit():
        return new_word
    else:
        for x in string.punctuation:
            if x != '-' and x in word:
                new_word = new_word.replace(x, '')
        return new_word


def clean_tweet(content):
    content = content.lower()
    exclude = set(string.punctuation)
    content = ''.join(ch for ch in content if ch not in exclude)

    content = content.replace('&amp;', '&')
    content = content.replace(',', '')
    content = content.replace('!', '')
    content = content.replace('-', '')
    content = content.replace('.', '')
    if 'http' in content or 'www' in content:
        content = re.sub(r'http\S+', '', content)
        content = re.sub(r'www\S+', '', content)
    return content


def clean_words_from_stopwords(stopwords, words):
    return [word for word in words if word not in stopwords]


def clean_content_by_nltk_stopwords(topic_content):
    stopWords = set(stopwords.words('english'))
    topic_content = ' '.join(clean_words_from_stopwords(stopWords, topic_content.split(' ')))
    return topic_content


def clean_text(description, remove_stop_words):
    description = " ".join(description.split())
    description = description.replace('"', '').replace("'", '')

    clean_words = []
    for word in description.split():
        new_word = remove_punctuation_chars(word)
        clean_words.append(new_word)

    description = ' '.join(clean_words)

    description = clean_tweet(description)
    if remove_stop_words:
        return clean_content_by_nltk_stopwords(description)
    else:
        return description


class RelevanceEvaluator:

    def __init__(self) -> None:
        super().__init__()
        with pkg_resources.path(RelevantFiles, "glove-wiki-gigaword-50.txt") as p:
            file_path = p
        model = gensim.models.KeyedVectors.load_word2vec_format(file_path, datatype=np.float16)
        self._word_vector_dict = model.wv

    def eval_claim_tweets(self, prototype_text, tweets, use_mean=True):
        prototype_words = clean_text(prototype_text, True).split(' ')
        distances = []
        for tweet in tweets:
            tweet_words = clean_text(tweet['tweet'], True).split(' ')
            distance_with_keywords = self.word_movers_distance(prototype_words, tweet_words)
            distances.append(distance_with_keywords)
        if use_mean:
            if len(distances) > 0:
                return {'distance': float(np.mean(distances)), 'tweet_num': len(tweets)}
            else:
                return {'distance': 2, 'tweet_num': len(tweets)}
        else:
            return distances

    def word_movers_distance(self, claim_description_words, post_words):
        claim_words_vectors = self._get_words_vectors(claim_description_words)
        post_words_vectors = self._get_words_vectors(post_words)
        try:
            return np.mean(cdist(post_words_vectors, claim_words_vectors, metric='cosine').min(axis=1))
        except Exception as e:
            return -1

    def _get_words_vectors(self, words):
        return np.array([self._word_vector_dict[word] for word in words if word in self._word_vector_dict])


class TwitterCrawler:
    def __init__(self, output_path='output/') -> None:
        super().__init__()
        self.output_path = Path(output_path)
        self.iter = 1
        self.id_set = set()
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)


    def retrieve_tweets(self, query_str, consumer_key, consumer_secret, access_token, access_token_secret, max_num_tweets=20, hide_output=True):
        search_id = uuid.uuid3(uuid.NAMESPACE_DNS, query_str)
        output_file_name = str(self.output_path / f"tweets_{search_id}.json")
        
        load_dotenv()

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True)

        text_query = query_str
        if not query_str:
            tweets = []
            return tweets
        count = 50
        try:
            tweets = tweepy.Cursor(api.search_tweets, q=text_query).items(count)

            tweets_list = [{'id':tweet.id,'username': tweet.user.screen_name,'tweet': tweet.text} for tweet in tweets]

            with open(output_file_name, 'w') as f:
                json.dump(tweets_list, f)

        except BaseException as e:
            print('failed on_status,', str(e))
        if os.path.exists(output_file_name):
            tweets = self._read_json_tweets(output_file_name)
            os.remove(output_file_name)
        else:
            tweets = []
        return tweets


    def _read_json_tweets(self, file_path):
        tweets = []
        with open(file_path, encoding="utf8") as f:
            for line in f:
                tweets.append(json.loads(line))
        return tweets[0]


def save_tweets_to_server(fname, tweets):
    with open(fname, 'w') as f:
        for tweet in tweets:
            f.write(f'{json.dumps(tweet)}\n')


class IterativeQuerySelection:
    def __init__(self, relevance_evaluator, twitter_crawler, min_tweet_count=5, max_keywords_size=6,
                 min_keywords_size=2) -> None:
        super().__init__()
        self._min_tweet_count = min_tweet_count
        self._max_keywords_size = max_keywords_size
        self._min_keywords_size = min_keywords_size
        self._relevance_evaluator = relevance_evaluator
        self.twitter_crawler = twitter_crawler

    def hill_climbing(self, prototype_text, search_count, iterations, keywords_start_size, output_keywords_count, search_wmd_updates=None):
        final_queries = []
        self._keywords_score_dict = defaultdict()
        start = timeit.default_timer()
        for j in tqdm(range(search_count), desc='Search run'):
            all_keywords = set()

            self._walked_keywords = Counter()
            self._last_distance = 2
            prune_set = set()

            prototype_words = self.get_claim_words_from_description(prototype_text)
            new_keywords = self._get_keywords_by_pos_tagging_for_claim(prototype_words, keywords_start_size)
            current_keywords = new_keywords
            for iteration in tqdm(range(iterations), desc='iterations'):
                keywords_set = ' '.join(new_keywords)
                all_keywords.add(keywords_set)
                evaluation = self.eval_keywords_for_claim(prototype_text, keywords_set)

                self._add_new_keywords(keywords_set, evaluation['distance'], evaluation['tweet_num'])
                if evaluation['tweet_num'] == 0:
                    prune_set.add(frozenset(new_keywords))

                if self._evaluate_keywords(evaluation, new_keywords):
                    current_keywords = new_keywords

                new_keywords = self._get_next_keywords(prototype_words, current_keywords, prune_set)
                if search_wmd_updates is not None:
                    best_distances, queries = self.get_topn_queries(output_keywords_count)
                    search_wmd_updates.append(np.mean(best_distances) * -1)
                if new_keywords is None:
                    break

            best_distances, queries = self.get_topn_queries(output_keywords_count)

            distances, tweet_counts = list(zip(
                *[self._keywords_score_dict[keywords_set] for keywords_set in queries]))
            self._add_new_keywords('||'.join(queries), np.mean(distances), sum(tweet_counts))

            final_queries.extend(queries)

        keywords_set_score_dict = {frozenset(keywords.split()): self._keywords_score_dict[keywords] for keywords in
                                   self._keywords_score_dict}
        final_queries = self._get_sorted_queries(final_queries, keywords_set_score_dict)
        min_count_queries = []
        other_queries = []
        empty_queries = []
        for query in final_queries:
            if keywords_set_score_dict[query][1] >= self._min_tweet_count:
                min_count_queries.append(query)
            elif keywords_set_score_dict[query][1] > 0:
                other_queries.append(query)
            else:
                empty_queries.append(query)

        final_queries = min_count_queries + other_queries
        final_queries = final_queries if len(final_queries) > 0 else empty_queries
        distances, tweet_counts = list(
            zip(*[keywords_set_score_dict[keywords_set] for keywords_set in final_queries]))

        final_queries = [' '.join(query) for query in final_queries][:output_keywords_count]

        end = timeit.default_timer()
        return final_queries, keywords_set_score_dict

    def get_topn_queries(self, output_keywords_count):
        queries = []
        best_distances = []
        if len(self._walked_keywords) > 0:
            queries, best_distances = list(zip(*self._walked_keywords.most_common(output_keywords_count)))
            queries = list(queries)
            best_distances = list(best_distances)
        if output_keywords_count - len(queries) > 0:
            queries_temp, evals = list(zip(*sorted(self._keywords_score_dict.items(), key=lambda q: q[1][0])[
                       :(output_keywords_count - len(queries))]))
            queries += queries_temp
            best_distances += [-wmd for wmd, tweet_count in evals]
        return best_distances, queries

    def get_claim_words_from_description(self, claim):
        words = self.get_name_entities(claim.rstrip('.').split())
        words = list([x for x in words if x != ''])
        return words

    def get_name_entities(self, claim_description_words):
        '''
        Get name entities from text using ner tagger from nltk
        :param claim_init_query: input text
        :return: list of named entities
        '''
        tagging = nltk.pos_tag(claim_description_words)
        namedEnt = nltk.ne_chunk(tagging, binary=True)
        entities = []
        for chunk in namedEnt:
            if hasattr(chunk, 'label'):
                word = ' '.join(c for c, tag in chunk)
                entities.append(remove_punctuation_chars(word.lower()))
            else:
                word, tag = chunk
                if tag in ['VBG', 'CD', 'JJ', 'VB', 'VBN'] or 'NN' in tag:
                    entities.append(remove_punctuation_chars(word.lower()))
        return entities

    def _get_keywords_by_pos_tagging_for_claim(self, claim_description_words, start_size):
        return self.get_name_entities(claim_description_words)[:start_size]

    def eval_keywords_for_claim(self, prototype_text, keywords_str):
        tweets = self.twitter_crawler.retrieve_tweets(keywords_str, consumer_key, consumer_secret, access_token, access_token_secret)
        evaluation = self._relevance_evaluator.eval_claim_tweets(prototype_text, tweets)
        return evaluation

    def _add_new_keywords(self, keywords_str, score=None, tweet_count=None):
        self._keywords_score_dict[keywords_str] = (score, tweet_count)

    def _evaluate_keywords(self, evaluation, curr_keywords):
        keywords_str = ' '.join(curr_keywords)
        if evaluation['tweet_num'] >= self._min_tweet_count:
            self._walked_keywords[keywords_str] = -1.0 * evaluation['distance']
        if evaluation['distance'] < self._last_distance and evaluation['tweet_num'] >= self._min_tweet_count:
            self._last_distance = evaluation['distance']
            return True
        return False

    def _get_next_keywords(self, claim_description_words, current_keywords, prune_set):
        candidates = list(set(claim_description_words) - set(current_keywords))
        next_keywords = self.generate_next_keywords(candidates, current_keywords)
        tries = 0
        while any([prune.issubset(frozenset(next_keywords)) for prune in prune_set]) \
                or ' '.join(next_keywords) in self._keywords_score_dict or \
                len(next_keywords) > self._max_keywords_size:
            try:
                tries += 1
                if tries == 500:
                    return None
                candidates = list(set(claim_description_words) - set(next_keywords))
                next_keywords = self.generate_next_keywords(candidates, next_keywords)
            except Exception:
                pass
        return next_keywords

    def generate_next_keywords(self, possible_candidates, start_position):
        if len(possible_candidates) == 0:
            next_keywords = self.remove_word(start_position)
        elif len(start_position) == self._min_keywords_size:
            prob = random.random()
            if prob < 0.5:
                next_keywords = self.swap_words(possible_candidates, start_position)
            else:
                next_keywords = self.add_word(possible_candidates, start_position)

        else:
            prob = random.random()
            if prob < 0.33:
                next_keywords = self.add_word(possible_candidates, start_position)
            elif prob < 0.67:
                next_keywords = self.swap_words(possible_candidates, start_position)
            else:
                next_keywords = self.remove_word(start_position)
        return next_keywords

    def swap_words(self, possible_candidates, start_position):
        next_keywords = self.remove_word(start_position)
        possible_candidates = list(set(possible_candidates) - set(start_position))
        next_keywords = self.add_word(possible_candidates, next_keywords)
        return next_keywords

    def add_word(self, possible_candidates, start_position):
        word_pos_tagging_rank_dict = self._get_word_to_prob_by_pos_tagging(possible_candidates)
        candidates, probabilities = list(zip(*iter(word_pos_tagging_rank_dict.items())))
        return start_position + list(np.random.choice(candidates, 1, p=probabilities))

    def remove_word(self, start_position):
        word_pos_tagging_rank_dict = self._get_word_to_prob_by_pos_tagging(start_position)
        candidates, probabilities = list(zip(*iter(word_pos_tagging_rank_dict.items())))
        return list(np.random.choice(candidates, len(start_position) - 1, False, p=probabilities))

    def _get_word_to_prob_by_pos_tagging(self, claim_description_words):
        word_pos_tagging_rank_dict = defaultdict(float)
        pos_to_rank = {}
        pos_to_rank['NOUN'] = 5
        pos_to_rank['ADJ'] = 4
        pos_to_rank['ADV'] = 3
        pos_to_rank['NUM'] = 2
        word_tag_tuples = pos_tag(claim_description_words, tagset='universal')
        for word, tag in word_tag_tuples:
            word_pos_tagging_rank_dict[word.lower()] = pos_to_rank.get(tag, 1)
        total = float(sum(word_pos_tagging_rank_dict.values()))
        word_pos_tagging_rank_dict = {word: rank / total for word, rank in word_pos_tagging_rank_dict.items()}
        return word_pos_tagging_rank_dict

    def _get_sorted_queries(self, final_queries, keywords_set_score_dict):
        final_queries = set([frozenset(query.split()) for query in final_queries])  # remove duplicate queries
        final_queries = sorted(final_queries, key=lambda x: keywords_set_score_dict[x][0])  # sort queries by RME
        return final_queries


def searchIQS(text, user_consumer_key, user_consumer_secret, user_access_token, user_access_token_secret,
            num_return_tweets=12, min_tweet_count=3, search_count=1, iterations=15, keywords_start_size=3,
            max_tweets_per_query=100, output_keywords_count=5):
    global consumer_key, consumer_secret, access_token, access_token_secret
    consumer_key = user_consumer_key
    consumer_secret = user_consumer_secret
    access_token = user_access_token
    access_token_secret = user_access_token_secret

    twitter_crawler = TwitterCrawler(output_path='output/')
    relevance_evaluator = RelevanceEvaluator()

    iqs = IterativeQuerySelection(relevance_evaluator, twitter_crawler, min_tweet_count)

    res, keywords = iqs.hill_climbing(text, search_count, iterations, keywords_start_size, output_keywords_count)

    tweets = []
    for output_query in res:
        tweets.extend(twitter_crawler.retrieve_tweets(output_query, consumer_key, consumer_secret, access_token, access_token_secret, max_tweets_per_query))

    tweets_wmds = relevance_evaluator.eval_claim_tweets(text, tweets, use_mean=False)

    for idx, dict in enumerate(tweets):
        dict['wmd'] = tweets_wmds[idx]

    sorted_tweets = [x for _, x in sorted(zip(tweets_wmds, tweets), key=lambda pair: pair[0])]

    relevant_keywords_set = min(keywords.items(), key=lambda k: k[1][0])[0]
    keywords_list = list(relevant_keywords_set)

    search_id = uuid.uuid4()
    tweet_fname = f'output/tweets_{search_id}.json'
    final_sorted_tweets = sorted_tweets[:num_return_tweets]
    final_sorted_tweets.append(keywords_list)
    save_tweets_to_server(tweet_fname, final_sorted_tweets)

    return final_sorted_tweets




