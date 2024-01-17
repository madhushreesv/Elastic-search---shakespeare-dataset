**Instructions for running your system**
**Architecture:**

The overall architecture of the system includes:
1. **Elasticsearch**: Used to index and search the Shakespeare collection.
2. **Python code base**: To carry out tasks including index generation, data input, querying, text analysis, and similarity matching, the Python code interfaces with Elasticsearch.
To run the system, I followed these instructions:
I first started Elasticsearch on my local machine by navigating to the folder where I have the elastic search tar file and executed the below commands in the Linux command terminal as shown below to start the elastic search.
cd elasticsearch-6.5.1/bin
./elasticsearch
 
Then I accessed Elasticsearch in the web browser by navigating to ‘http://localhost:9200’ to make sure it is running.
 
Then I used the below command to install the python API:
pip install elasticsearch==6.8.2
(I used 6.8.2 version because I worked with the horizon client)
 
To make sure the python client is running and to connect to Elasticsearch, I created a ‘test.py’ file to print a dummy
output.
 
The test.py file contained the below piece of code.
from elasticsearch import Elasticsearch
es = Elasticsearch("http://localhost:9200")
print(“Hello Search Superhero!”)
To run the test.py file I ran the below command in the terminal.
python test.py

 
I added my codes  for the rest of the tasks in the same file. Renamed to ‘code.py’ for submission.
The script can be run as in the Python Environment. Make sure Elasticsearch is running before running the code and update the file_path.
Output : The code will create index, upload the collection into Elastic search, performs tokenization, normalization, stemming, stop word removal, similarity matching, n-gram and search queries. The outputs will be displayed in the console.
I executed the following tasks in stages.

**Indexing**
For indexing, the Shakespeare dataset was downloaded from the provided source (https://www.elastic.co/guide/en/kibana/5.5/tutorial-load-dataset.html). I have used the entire collection for the experiments.
Description of the document collection:
The collection contains various Shakespearean documents of type act, scene and line.. 
I took a sneek peek inside the shakespeare.json  file. The file contains one JSON object per line indicating metadata and a second JSON object containing the document.
There is an index line that specifies the id of the document, followed by the document itself. The document contains contains line ID, play name, speech number, speaker, and text entry.
{"index":{"_index":"shakespeare","_id":0}}
{"type":"act","line_id":1,"play_name":"HenryIV", "speech_number":"","line_number":"","speaker":"","text_entry":"ACT I"}
{"index":{"_index":"shakespeare","_id":1}}
The Shakespeare data set is organized in the following schema:
{
    "line_id": INT,
    "play_name": "String",
    "speech_number": INT,
    "line_number": "String",
    "speaker": "String",
    "text_entry": "String",
}
For indexing the collection into Elasticsearch, I followed the below steps:
1.	I created a function called create_shakespeare_index () for indexing the documents. 
2.	An index named "shakespeare".  I monitored the indexing process to ensure it completes successfully.
3.	To see if the index is present in the Elasticsearch, I used the below command.
 curl 'localhost:9200/_cat/indices?v'. Please see the below output.
health status index               pri rep docs.count docs.deleted 
yellow open   shakespeare           5   1     111396            0     17.6mb         17.6mb

4.	I also created a function called upload_shakespeare_collection() which uses the bulk API to upload the json file in specified batches and view_shakespeare_documents() to view first 10 documents.
 
There were no indexing-related issues because I had ensured that the Elasticsearch service was running.There was proper connection to Elasticsearch and correct usage of the Elasticsearch Python API.
I have considered only the first 10 documents for analysis of the below tasks.
Tokenization and Normalisation
For this task, I  created custom analyzers, settings and mappings while I created the create_shakespeare_index () function for indexing.
The built-in standard analyzer, was also utilized.
The system performs tokenization by lowercasing the text_entry field. I also used a custom filter ‘my_custom_analyzer’ to process the text_entry field further with the synonym filter ‘my_synonym_analyzer’ and normalization was also done using custom normalizer ‘my_custom_normalizer’.
 
The texts have been lowercased by the ‘standard tokenizer’ and ‘Lowercase’ filter in the first and synonyms have been added like ‘fight’, ‘quarrel’  and tokens have been generated. 
By using synonym filters, the documents containing any synonym terms can be retrieved with relevant results while searching.
By creating custom analyzers we can define our own way of tokenization. We can even combine the filters and tokenizers. More advanced python libraries like NLTK can also be used for Tokenization like using regex (Regular Expressions), word tokenization etc..
 
The texts have been normalized to a standard form i.e, lowercased.
Challenges encountered during this step are:
1. When I tried to change the mappings and settings after indexing, I ran into an error as shown below. The error was because once the document is added we will not be able to change the mappings, and we will have to delete the old index, define the new mapping and import all the documents again.(Learning from Lab2)
 
So I deleted the index as shown below. And then called the function create_shakespeare_index ()  with custom analyzers and mappings. 

2. Also when I had specified the normalizer before the tokenizer I got the below error. So I specified the normalizer at the end. From this I learnt that if normalizer is used on a specific field first, the tokenizer must be disabled or set to null.
 

Separate functions are created for tokenization like tokenize_text_case_folding() and tokenize_text_synonyms() and for normalization normalize_text() is created respectively. These functions provides a simple and reusable way to tokenize,normalize the text using a custom analyzer and normalize.
Selecting Keywords
For this task, I used the the stopword removal filter, n-gram extraction and incorporated the similarity module.
 
In the above screen shots we can see how the stop words like in , a, that, the etc.. have been removed from the texts.
This was done using ‘my_stop_words_analyzer’ custom analyzer with standard tokenizer, lowercase filter, and English stop words.
I implemented the Similarity module in a function  find_similar_documents()  which uses a specified analyzer to analyze the text_entry field and then perform More Like This Query (MLT) query to find similarity. We can also customize the parameters to this query for similarity matching.
By default, Elasticsearch uses the BM25 (Best Matching 25) similarity model for predicting scores of the  search results. However, if we want to customise the similarity model, it can be configured during indexing. 
The n-gram tokens were generated using the custom n-gram tokenizer called ‘’ which treats letters in the text_entry field as tokens based on the min and max grams length.

**Similarity score and the n-gram tokens:** 
We can see that 3 letter words from the texts are created as individual tokens.
 
find_similar_documents() fuction was created to achieve this task.
No challenges were encountered during this step.

Stemming or Morphological Analysis 
The custom analyzer ‘my_stemmer_analyzer’ includes a stemmer filter for English language stemming. It tokenizes the text_entry field, applies case folding (lowercasing), and performs stemming. 
I have created a function called analyze_text_with_stemmer() for stemming.
 
The words have been reduced to it’s base form like lately has been reduced to late, blessed to bless etc..
When the user searches for blessing, documents containing bless or blessed are also retrieved. This can help to improve recall or the search methodology.
We can notice that noble,people in the last sentence, is stemmed to nobl,peopl.  This shows that the algorithm is not always perfect. 
Several stemming algorithms are provided by NLTK, such as the Porter stemmer, Lancaster stemmer and Snowball stemmer. They can also be considered.
No challenges were encountered during this step.

**Searching**
For this task, three textural queries were created from User’s point of view based on some criteria. The queries are:

1.	query1 = {"query": {"match": {"play_name": "Henry IV"}}}

2.	query2 = {"query": {"match": {"speaker": "KING HENRY IV"}}}

3.	query3 = {"query": {"match_phrase": {"text_entry": "shall daub her lips"}}}

To achieve this task, the search method of the Elasticsearch client was used. I have created a separate function search_queries() to process the search queries.  These queries are Elasticsearch DSL queries, which are very flexible. The queries can also be fine-tuned like to find the exact phrase as done in query 3.  We can also  include analyzers and add additional information to narrow down the search.

By executing search_queries(), the search results will be printed on the console.

I did not face any challenges were encountered while performing this task.

All tasks were achieved through the Python Elastic search API.
General issues I encountered were network-related issues and while trying to configure Elastic search in mac os. Issues were related to Authentication and TSL because I had downloaded the latest version of elastic search (v8.8.1)


And that's a wrap! Thank you 
