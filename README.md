# WDPS1805 - Large Scale Entity Linking
The goal of this assignment is to perform Entity Linking on a collection of web pages. The solution takes gzipped WARC files as input which is then processed.

The assigment was divided into the following steps:

## Parsing the HTML content
WARC record sent to a node as an item is stripped of all HTML tags, split into words and then processed. This conversion is done by a custom utility based on python's `html.parser`.

## Extracting Named Entities from the text
Named entities are extracted from the payload using NLTK's `ne_chunk`. The output is a list of all the named entities from the payload text.

## Linking entities to Freebase
Possible entities for each word are extracted with Elasticsearch. Each Freebase entity's tuples are then extracted from Freebase RDF with Sparql and the values of returned objects are put into sets. The best entity is then chosen as the one that has the highest connectiveness with some other word from the context, where connectiveness is size of intersection of sets of Sparql results.

  
## RUNNING THE SOLUTION

The final solution is in the prototype_with_ner folder.

For all the paths in the program to be correct, the content of this folder must be located in scratch/wdps/ subfolder in wdps1805 folder on the cluster (this is not done yet, because the cluster has been down for two days by the moment this readme was written).

Everything can be run with `./run.sh` command, which starts Sparql, ElasticSearch, prepares an archive of necessary python files and runs main.py (after which it kills both Elasticserch and Sparql).

The resulting data will reside in sample-result file.

If Spark is down, the solution still can be run with our simple Spark mock:
1. Change ``import pyspark`` to ``import pyspark_mock`` in main.py 
2. Run from the command line:
```
python main.py sample.warc sample-result “elastic search address” “sparql address”
```
The program can also be run without ES or Sparql, for that change corresponding `mock` arguments in main.py (lines 27 and 35) to True and run it from the command line (replace corresponding addresses with any string).

We also have main_intervals.py which implements the solution with performance improvement based on collocational word properties. It can be used instead of main.py in run.sh or the above commands.

Several settings of the app can be changed in config.py file. For example, сhanging values of `SPARQL_RESULTS_COUNT` and `ES_RESULTS_COUNT` to larger ones will improve the recall.
