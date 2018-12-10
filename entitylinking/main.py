import logging
from collections import defaultdict

from ElasticSearcher import ElasticSearcher
from SparqlSearcher import SparqlSearcher
from TextExtractor import TextExtractor
from WarcRecord import WarcRecord
from pyspark import SparkContext
import sys
from config import ES_RESULTS_COUNT, SPARQL_RETRY_DELAY, SPARQL_RETRY_ATTEMPTS, SPARQL_RESULTS_COUNT

logger = logging.root
logger.setLevel(logging.INFO)

INFILE = sys.argv[1]
OUTFILE = sys.argv[2]
ES_ADDRESS = sys.argv[3]
SPARQL_ADDRESS = sys.argv[4]

es = ElasticSearcher(
    ES_ADDRESS,
    ES_RESULTS_COUNT,
    mock=False
)

sparql = SparqlSearcher(
    SPARQL_ADDRESS,
    SPARQL_RESULTS_COUNT,
    SPARQL_RETRY_ATTEMPTS,
    SPARQL_RETRY_DELAY,
    mock=False
)


def process_page(row: tuple):
    _, web_arch_record = row
    if not web_arch_record:
        return
    logger.info('Processing a warc record...')
    warc_record = WarcRecord(web_arch_record)
    if warc_record.broken:
        return
    words = TextExtractor.get_all_words(warc_record.payload)

    context_size = 10;
    canonical_labels_of_ids = dict()
    related_ids_of_ids = dict()
    ids_of_words = defaultdict(list)
    words_wo_repititions = []
    # Build sets
    for word in words:
        for es_result in es.search(word):
            if canonical_labels_of_ids.get(es_result.id) is not None:
                # We are not interested in labels with repeating freebase ids,
                # so we just skip them
                continue
            words_wo_repititions.append(word)
            ids_of_words[word].append(es_result.id)
            canonical_labels_of_ids[es_result.id] = es_result.label
            related_ids_of_ids[es_result.id] = set(i for i in sparql.search(es_result.id))

    # Calc links

    for i, word in enumerate(words_wo_repititions):
        max_common = -1
        id_with_max_common = None
        for j in range(i - context_size, i + context_size + 1):
            if j != i and j in range(0, len(words_wo_repititions)):
                for freebase_id in ids_of_words[word]:
                    for other_id in ids_of_words[words_wo_repititions[j]]:
                        common = len(related_ids_of_ids[other_id].intersection(related_ids_of_ids[freebase_id]))
                        if common > max_common:
                            max_common = common
                            id_with_max_common = freebase_id
        if id_with_max_common is None:
            # No label intersects with anything, let's just pick the first one
            id_with_max_common = ids_of_words[word][0]
        label_with_max_common = canonical_labels_of_ids[id_with_max_common]
        yield stringify_reply(warc_record.id, label_with_max_common, id_with_max_common)
    logger.info('Processed record %s', warc_record.id)


def stringify_reply(warc_id, label, freebase_id):
    return '%s\t%s\t%s' % (warc_id, label, freebase_id)


#########################
# Run function on spark #
#########################

sc = SparkContext("yarn", "wdps17XX")

rdd = sc.newAPIHadoopFile(
    INFILE,
    "org.apache.hadoop.mapreduce.lib.input.TextInputFormat",
    "org.apache.hadoop.io.LongWritable",
    "org.apache.hadoop.io.Text",
    conf={"textinputformat.record.delimiter": "WARC/1.0"})

rdd = rdd.flatMap(process_page)

rdd = rdd.saveAsTextFile(OUTFILE)
