#!/usr/bin/env bash

echo "================================"
## Start sparql ##
KB_PORT=9090
KB_BIN=/home/bbkruit/scratch/trident/build/trident
KB_PATH=/home/jurbani/data/motherkb-trident
prun -o .kb_log -v -np 1 ${KB_BIN} server -i ${KB_PATH} --port ${KB_PORT} </dev/null 2> .kb_node &
echo "Waiting 5 seconds for trident to set up..."
until [[ -n "$KB_NODE" ]]; do KB_NODE=$(cat .kb_node | grep '^:' | grep -oP '(node...)'); done
sleep 5
KB_PID=$!
echo "Trident should be running now on node $KB_NODE:$KB_PORT (connected to process $KB_PID)"
echo "================================"
## Start elasticsearch ##
ES_PORT=9200
ES_BIN=$(realpath ~/scratch/wdps/elasticsearch-2.4.1/bin/elasticsearch)
prun -o .es_log -v -np 1 ESPORT=$ES_PORT $ES_BIN </dev/null 2> .es_node &
echo "Waiting for 15 seconds elasticsearch to set up..."
sleep 15
ES_NODE=$(cat .es_node | grep '^:' | grep -oP '(node...)')
ES_PID=$!
echo "Elasticsearch should be running now on node $ES_NODE:$ES_PORT (connected to process $ES_PID)"
echo "================================"
## Prepare app ##
zip -r app.zip ElasticSearcher.py SparqlSearcher.py TextExtractor.py WarcRecord.py config.py pyspark_mock.py
echo "================================"
## Prepare venv ##
echo "Preparing venv, may ignore errors"
source venv/bin/activate
virtualenv --relocatable venv
## WARNING! ##
## Zipping is not performed here, you have to manually re-archive venv
## in case you change the environment to save up time and logs.
# zip -r venv.zip venv
echo "================================"
## Spark job params ##
SCRIPT=${1:-"main.py"}
INFILE=${2:-"hdfs:///user/bbkruit/sample.warc.gz"}
OUTFILE=${3:-"sample-result"}
PYTHON_BIN=$(readlink -f $(which python))
## Run spark ##
PYSPARK_PYTHON=$PYTHON_BIN \
  ~/spark-2.1.2-bin-without-hadoop/bin/spark-submit \
  --conf spark.yarn.appMasterEnv.PYSPARK_PYTHON=./VENV/venv/bin/python \
  --master yarn-cluster \
  --archives venv.zip#VENV \
  --py-files app.zip \
  $SCRIPT $INFILE $OUTFILE $ES_NODE:$ES_PORT $KB_NODE:$KB_PORT
echo "================================"
## Download results ##
echo "Downloading output of job to $OUTFILE"
hdfs dfs -cat $OUTFILE"/*" > $OUTFILE
echo "================================"
## Clean up ##
echo "Killing elasticsearch/trident"
# hadoop fs -rm -r "$OUTFILE"
kill $ES_PID
kill $KB_PID
echo "================================"
