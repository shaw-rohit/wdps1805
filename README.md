# WDPS1805 - Large Scale Entity Linking
The goal of this assignment was to perform Entity Linking on a collection of web pages. The solution takes gzipped WARC files from Freebase as input which is then processed.

The assigment was divided into the following steps:

## 1) Reading the WARC file from the HDFS
To read the WARC files from HDFS, we used the function newAPIHadoopFile together with a custom delimiter which we set to: "WARC/1.0". This gives us as an RDD containing single records from WARC as elements as a result, which can then be parsed and cleaned. 

## 2) Parsing the HTML content to make it useable
Since we parsed the WARC records using a dedicated library, we were able to remove all the WARC related overhead from the files whilst keeping the HTML tags intact.

## 3) Extract Named Entities from the text


## 4) Link entities to Freebase


  
## RUNNING THE SOLUTION

The final solution is in the prototype_with_ner folder.

For all the paths in the program to be correct, the content of this folder must be located in scratch/wdps/ subfolder in wdps1805 folder on the cluster (this is not done yet, because the cluster has been down for two days by the moment this readme was written).

Everything can be run with `./run.sh` command, which starts Sparql, ElasticSearch and runs main.py.

The resulting data will reside in sample-result file.

If Spark is down, the solution still can be ran on our mock:
1. Change ``import pyspark`` to ``import pyspark_mock`` in main.py 
2. Run from the command line:
```
python main.py sample.warc sample-result “elastic search address” “sparql address”
```
The program can also be run without ES or Sparql, for that change corresponding flags in main.py (lines 27 and 35) to True and run it from the command line (replace corresponding addresses with any string).

We also have main_intervals.py which implements the solution with performance improvement based on collocational word properties. It can be used instead of main.py in run.sh or the above commands.

