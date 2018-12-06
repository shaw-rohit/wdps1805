import requests, json

def sparql(domain, fb_id):
    url = 'http://%s/sparql' % domain
    #
    response = requests.post(url, data={'print': True, 'query': "select * where {<http://rdf.freebase.com/ns/" + fb_id + "> ?p ?o} limit 10"})
    if response:
        try:
            response = response.json()
            return response
        except Exception as e:
            print(response)
            raise e

if __name__ == '__main__':
    import sys
    try:
        _, DOMAIN = sys.argv
    except Exception as e:
        print('Usage: python sparql.py DOMAIN')
        sys.exit(0)

# will work correctly if a single html page is given to it
def sparql_main(domain):
    with open("labels_one_page.txt") as f:
        with open("values_one_page.txt", "w") as out:
            out.write(f.readline())
            for line in f:
                if 'ES-Response-For-Entry: ' in line:
                    out.write(line)
                else:
                    # sparql for fb IDs entities for the given entry
                    id = line.split(' ')[0]
                    out.write(id + '\n')
                    resp = sparql(domain, id.split(':')[1])
                    resp = resp.get('results').get('bindings')
                    for binding in resp:
                        out.write(binding.get('o').get('value'))



sparql_main(DOMAIN)
