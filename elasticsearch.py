import requests

N_RESULTS = 10

def get_ids_from_es(domain, query):
    url = 'http://%s/freebase/label/_search' % domain
    response = requests.get(url, params={'q': query, 'size': N_RESULTS})
    results = []
    if response:
        response = response.json()
        for hit in response.get('hits', {}).get('hits', []):
            freebase_label = hit.get('_source', {}).get('label')
            freebase_id = hit.get('_source', {}).get('resource')
            score = hit.get('_score')
            results.append((query, freebase_id, freebase_label, score))
    return results
    
if __name__ == '__main__':
    import sys
    try:
        _, DOMAIN = sys.argv
    except Exception as e:
        print('Usage: python elasticsearch.py DOMAIN')
        sys.exit(0)

    with open('entries.txt') as f:
        with open('labels.txt', 'w') as out:
            for query in f:
                results = get_ids_from_es(DOMAIN, query.strip())
                for query, id, label, score in results:
                    out.write(str(query) + ": " + str(id) + " " + str(label) + " " + str(score) + "\n")
