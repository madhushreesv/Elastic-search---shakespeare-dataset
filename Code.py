##################################################
## Author: {Madhushree}
## Copyright: Copyright {2024}
##################################################

# import necessary libraries

from elasticsearch import Elasticsearch
import json

# Connect to Elasticsearch
es_client = Elasticsearch("localhost:9200")


def create_shakespeare_index(index_name):
    """
    Creates an index in Elasticsearch called 'shakespeare' with custom analyzers and mappings.

    Args:
        index_name (str): The name of the index to be created.

    Returns:
        NA
    """

    # Define the settings and mappings for the index
    settings = {
        "settings": {
            "analysis": {
                "analyzer": {
                    # Creating a Custom analyzer using the standard tokenizer and synonyms filter.
                    "my_custom_analyzer": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": ["lowercase"],
                    },
                    # Creating a Custom analyzer using the standard tokenizer, lowercase filter, and English stop words.
                    "my_stop_words_analyzer": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": ["lowercase", "english_stop"],
                    },
                    # Creating a Custom analyzer using the whitespace tokenizer and stemming filter.
                    "my_stemmer_analyzer": {
                        "type": "custom",
                        "tokenizer": "whitespace",
                        "filter": ["stemmer"],
                    },
                    "my_synonym_analyzer": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": ["lowercase", "my_synonym_filter"],
                    },
                    "my_ngram_analyzer": {
                        "type": "custom",
                        "tokenizer": "my_ngram_tokenizer",
                        "filter": ["lowercase"],
                    },
                },
                "tokenizer": {
                    "my_ngram_tokenizer": {
                        "type": "ngram",
                        "min_gram": 3,
                        "max_gram": 3,
                        "token_chars": ["letter", "digit"],
                    }
                },
                "filter": {
                    # Creating a filter to remove English stop words.
                    "english_stop": {"type": "stop", "stopwords": "_english_"},
                    "my_synonym_filter": {
                        "type": "synonym",
                        "synonyms": ["fight, quarrel", "people, public"],
                    },
                },
                "normalizer": {
                    # Creating a Custom normalizer with lowercase filter.
                    "my_custom_normalizer": {"type": "custom", "filter": ["lowercase"]}
                },
            }
        }
    }

    # Create the index 'shakespeare' and mappings.
    es_client.indices.create(index=index_name, body=settings)


def upload_shakespeare_collection(file_path, batch_size=1000):
    """
    This fuction posts the entire shakespeare collection into Elasticsearch in batches since the data is more than 200,000 lines.

    Args:
        file_path (str): The name of the index to be created.
        batch_size (int): The number of documents to process in each batch.
    Returns:
        NA
    """

    # Reading the JSON file
    with open(file_path, "r") as file:
        lines = file.readlines()

    # Adding a new line at the end of each content.
    lines.append("\n")

    # Processing the documents in batches.
    total_docs = len(lines)
    current_batch = []
    for index, line in enumerate(lines):
        current_batch.append(line)

        # Checking if the batch size is reached or it is the last document.
        if len(current_batch) == batch_size or index == total_docs - 1:
            bulk_data = "".join(current_batch)
            es_client.bulk(bulk_data, index="shakespeare")  # calling the bulk API.

            # Reseting the batch to empty.
            current_batch = []


def view_shakespeare_documents(index_name):
    """
    This fuction retrieves and prints the first 10 documents from the 'shakespeare' index.

    Args:
        index_name (str): The name of the index to retrieve documents from.

    Returns:
        NA
    """
    # Search query to retrieve the first 10 documents in the collection
    query = {"size": 10, "query": {"match_all": {}}}
    response = es_client.search(index=index_name, body=query)
    print(response)


def tokenize_text_case_folding(index_name, analyzer_name, text):
    """
    This function tokenizes the text_entry field using a custom analyzer called 'my_synonym_analyzer'.

    Args:
        index_name (str): The name of the index to analyze the text in.
        analyzer_name (str): The name of the custom analyzer.
        text (str): The text to be analyzed.

    Returns:
        list: Returns a list of tokens extracted from the analyzed text.
    """
    # Creating the request body.
    body = {"analyzer": analyzer_name, "text": text}

    # Calling the Analyze API
    response = es_client.indices.analyze(index=index_name, body=body)

    # Extract and return the list of tokens.
    tokens = [token["token"] for token in response["tokens"]]
    return tokens


def tokenize_text_synonyms(index_name, analyzer_name, text):
    """
    This function tokenizes the text_entry field using a custom analyzer called 'my_custom_analyzer'.

    Args:
        index_name (str): The name of the index to analyze the text in.
        analyzer_name (str): The name of the custom analyzer.
        text (str): The text to be analyzed.

    Returns:
        list: Returns a list of tokens extracted from the analyzed text.
    """
    # Creating the request body.
    body = {"analyzer": analyzer_name, "text": text}

    # Calling the Analyze API
    response = es_client.indices.analyze(index=index_name, body=body)

    # Extract and return the list of tokens.
    tokens = [token["token"] for token in response["tokens"]]
    return tokens


def normalize_text(index_name, normalizer_name, text):
    """
    This function normalizes the text_entry field using a custom normalizer called 'my_custom_normalizer'.

    Args:
        index_name (str): The name of the index to normalize the text in.
        normalizer_name (str): The name of the custom normalizer.
        text (str): The text_entry field.

    Returns:
        list: Returns a list of tokens extracted from the normalized text.
    """

    # Creating the request body.
    body = {"text": text, "normalizer": normalizer_name}

    # Calling the Analyze API
    response = es_client.indices.analyze(index=index_name, body=body)

    # Extract and return the list of tokens.
    tokens = [token["token"] for token in response["tokens"]]
    return tokens


def remove_stopwords(index_name, analyzer_name, text):
    """
    This function removes the stopwords from the text_entry field using a custom analyzer and filter.

    Args:
        index_name (str): The name of the index.
        analyzer_name (str): The name of the custom analyzer.
        text (str): The text_entry field.

    Returns:
        list: Returns a list of tokens extracted from the text.
    """

    # Creating the request body with the analyzer and filter
    body = {
        "analyzer": analyzer_name,
        "text": text,
        "filter": ["lowercase", "english_stop"],
    }

    # Calling the Analyze API
    response = es_client.indices.analyze(index=index_name, body=body)

    # Extract and return the tokens
    tokens = [token["token"] for token in response["tokens"]]
    return tokens


def ngram_text(index_name, analyzer_name, text):
    """
    This function configures the ngram tokenizer to treat letters and digits as tokens.

    Args:
        index_name (str): The name of the index to normalize the text in.
        normalizer_name (str): The name of the custom normalizer.
        text (str): The text_entry field.

    Returns:
        list: Returns a list of tokens extracted from the normalized text.
    """

    # Creating the request body.
    body = {"analyzer": analyzer_name, "text": text}

    # Calling the Analyze API
    response = es_client.indices.analyze(index=index_name, body=body)

    # Extract and return the list of tokens.
    tokens = [token["token"] for token in response["tokens"]]
    return tokens


def find_similar_documents(index_name, analyzer_name, text):
    """
    This function is used to finds similar documents in the 'shakespeare' index for the text_entry.

    Args:
        index_name (str): The name of the index.
        analyzer_name (str): The name of the analyzer..
        text (str): The text_entry field.
    Returns:
        list: A list of tuples containing the score and n-gram tokens of the similar documents.
    """
    # Analyze the input text using the specified analyzer
    analyzed_text = tokenize_text_case_folding(index_name, analyzer_name, text)

    # Create the More Like This Query
    query = {
        "query": {
            "more_like_this": {
                "fields": ["text_entry"],
                "like": analyzed_text,
                "min_term_freq": 1,
                "max_query_terms": 12,
                "min_doc_freq": 1,
                "minimum_should_match": "1%",
            }
        }
    }

    # Execute the search query
    response = es_client.search(index=index_name, body=query)

    # Extract and return the scores along with n-gram tokens
    results = []
    for hit in response["hits"]["hits"]:
        score = hit["_score"]
        tokens = ngram_text(
            index_name, "my_ngram_analyzer", hit["_source"]["text_entry"]
        )
        results.append((score, tokens))
    return results


def analyze_text_with_stemmer(index_name, analyzer_name, text):
    """
    This function analyzes the text_entry field using the custom analyzer with stemmer.

    Args:
        index_name (str): The name of the index.
        analyzer_name (str): The name of the analyzer.
        text (str): The text_entry field.

    Returns:
        list: A list of tokens extracted from the analyzed text.
    """
    # Creating the request body
    body = {"analyzer": analyzer_name, "text": text}

    # Calling the Analyze API
    response = es_client.indices.analyze(index=index_name, body=body)

    # Extract and return the list of stemmed tokens
    tokens = [token["token"] for token in response["tokens"]]
    return tokens


def search_queries(queries):
    """
    This function performs 3 textural queries that the user might come up.

    Args:
        queries (list): 3 textural queries.

    Returns:
        list: A list of search results for each textural query.
    """

    results = []
    for query in queries:
        response = es_client.search(index=index_name, body=query)
        results.append(response)

    return results


# declare variables
index_name = "shakespeare"
shakespeare_json_file_path = (
    "/ufs/serve02/users/ms22749/Desktop/M-Drive/CE706_Assignment/shakespeare.json"
)
analyzer_name = "my_custom_analyzer"
normalizer_name = "my_custom_normalizer"
stemmer_name = "my_stemmer_analyzer"
synonym_analyzer = "my_synonym_analyzer"
stopwords_analyser_name = "my_stop_words_analyzer"

# calling create index function
create_shakespeare_index(index_name)
print("Shakespeare index created successfully!")
print(
    "---------------------------------------------------------------------------------"
)

# calling bulk upload function
upload_shakespeare_collection(shakespeare_json_file_path, batch_size=1000)
print("Shakespeare collection posted into Elastic search successfully!")
print(
    "---------------------------------------------------------------------------------"
)

print("Viewing first 10 documents in the shakespeare index.")
view_shakespeare_documents(index_name)
print(
    "---------------------------------------------------------------------------------"
)

es_client = Elasticsearch("localhost:9200")
response_data = es_client.search(index=index_name, size=10)

# Tokenize the text_entry field.
print("Tokenization - Lowercasing")
for hit in response_data["hits"]["hits"]:
    text_entry = hit["_source"]["text_entry"]
    tokens = tokenize_text_case_folding(index_name, analyzer_name, text_entry)
    print(tokens)
print(
    "---------------------------------------------------------------------------------"
)

print("Tokenization with Synonyms")
for hit in response_data["hits"]["hits"]:
    text_entry = hit["_source"]["text_entry"]
    tokens = tokenize_text_synonyms(index_name, synonym_analyzer, text_entry)
    print(tokens)
print(
    "---------------------------------------------------------------------------------"
)

# Normalized the text_entry field.
print("Normalization")
for hit in response_data["hits"]["hits"]:
    text_entry = hit["_source"]["text_entry"]
    tokens = normalize_text(index_name, normalizer_name, text_entry)
    print(tokens)
print(
    "---------------------------------------------------------------------------------"
)

# Analyze the text with the stemmer analyzer
print("Stemming")
for hit in response_data["hits"]["hits"]:
    text_entry = hit["_source"]["text_entry"]
    tokens = analyze_text_with_stemmer(index_name, stemmer_name, text_entry)
    # Print the tokens after stemming
    print(tokens)
print(
    "---------------------------------------------------------------------------------"
)

# Removing stopwords from the text_entry field.
print("Removing stop words")
for hit in response_data["hits"]["hits"]:
    text_entry = hit["_source"]["text_entry"]
    tokens = remove_stopwords(index_name, stopwords_analyser_name, text_entry)
    print(tokens)
print(
    "---------------------------------------------------------------------------------"
)

# Finding similar documents using n-grams and retrieving scores and n-gram tokens
print("Similar documents")
for hit in response_data["hits"]["hits"]:
    text_entry = hit["_source"]["text_entry"]
    similar_docs = find_similar_documents(index_name, analyzer_name, text_entry)
    for score, tokens in similar_docs:
        print(f"Similarity Score: {score}")
        print(f"n-gram tokens:", tokens)
print(
    "---------------------------------------------------------------------------------"
)


query1 = {"query": {"match": {"play_name": "Henry IV"}}}

query2 = {"query": {"match": {"speaker": "KING HENRY IV"}}}

query3 = {"query": {"match_phrase": {"text_entry": "shall daub her lips"}}}

queries = [query1, query2, query3]
search_results = search_queries(queries)
for i, result in enumerate(search_results):
    print(f"Search Result {i+1}:")
    print(result)
    print()
