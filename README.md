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
