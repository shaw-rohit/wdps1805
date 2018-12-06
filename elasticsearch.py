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
            score = hit.get('score')
            results.add((freebase_id, freebase_label, score))
    return results
    
if __name__ == '__main__':
    import sys
    try:
        _, DOMAIN = sys.argv
    except Exception as e:
        print('Usage: python elasticsearch.py DOMAIN')
        sys.exit(0)

    with open('entities_one_page.txt') as f:
        with open('labels_one_page.txt', 'w') as out:
            # write page id
            out.write(f.readline())
            # process queries
            for query in f:
                results = get_ids_from_es(DOMAIN, query.strip())
                out.write('ES-Response-For-Entry: ' + query.strip() + '\n')
                for id, label, score in results:
                    out.write(str(id) + ' ' + str(label) + ' ' + str(score) + '\n')
