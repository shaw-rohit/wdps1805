import logging
from collections import defaultdict

from ElasticSearcher import ElasticSearcher
from SparqlSearcher import SparqlSearcher
from TextExtractor import TextExtractor
from WarcRecord import WarcRecord
from pyspark_mock import SparkContext
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
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
    mock=True
)

sparql = SparqlSearcher(
    SPARQL_ADDRESS,
    SPARQL_RESULTS_COUNT,
    SPARQL_RETRY_ATTEMPTS,
    SPARQL_RETRY_DELAY,
    mock=True
)

def get_continuous_chunks(text):
    chunked = ne_chunk(pos_tag(word_tokenize(text)))
    continuous_chunk = []
    current_chunk = []
    for i in chunked:
            if type(i) == Tree:
                    current_chunk.append(" ".join([token for token, pos in i.leaves()]))
            elif current_chunk:
                    named_entity = " ".join(current_chunk)
                    if named_entity not in continuous_chunk:
                            continuous_chunk.append(named_entity)
                            current_chunk = []
            else:
                    continue
    return continuous_chunk


def process_page(row: tuple):
    _, web_arch_record = row
    if not web_arch_record:
        return
    logger.info('Processing a warc record...')
    warc_record = WarcRecord(web_arch_record)
    if warc_record.broken:
        return
    words = TextExtractor.get_all_words(warc_record.payload)
    ners = get_continuous_chunks(warc_record.payload)

    canonical_labels_of_ids = dict()
    related_ids_of_ids = dict()
    ids_of_words = defaultdict(list)
    # Build sets
    for word in words:
        for es_result in es.search(word):
            if canonical_labels_of_ids.get(es_result.id) is not None:
                # We are not interested in labels with repeating freebase ids,
                # so we just skip them
                continue
            ids_of_words[word].append(es_result.id)
            canonical_labels_of_ids[es_result.id] = es_result.label
            related_ids_of_ids[es_result.id] = set(i for i in sparql.search(es_result.id))

    # Calc links
    for word, ids in ids_of_words.items():
        if word in ners:
            max_common = -1
            id_with_max_common = None
            for freebase_id in ids:
                for other_id, related_ids in related_ids_of_ids.items():
                    if freebase_id == other_id:
                        continue
                    common = len(related_ids.intersection(related_ids_of_ids[freebase_id]))
                    if common > max_common:
                        max_common = common
                        id_with_max_common = freebase_id
            if id_with_max_common is None:
                # No label intersects with anything, let's just pick the first one
                id_with_max_common = ids[0]
            label_with_max_common = canonical_labels_of_ids[id_with_max_common]
            yield stringify_reply(warc_record.id, word, id_with_max_common)
    logger.info('Processed record %s', warc_record.id)


def stringify_reply(warc_id, word, label, freebase_id):
    return '%s\t%s\t%s\t%s' % (warc_id, word, freebase_id)


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
