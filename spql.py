import requests, json
import keyboard

def sparql(domain, fb_id):
    url = 'http://%s/sparql' % domain
    #
    response = requests.post(url, data={'print': True, 'query': "select * where {<http://rdf.freebase.com/ns/" + fb_id + "> ?p ?o} limit 100"})
    if response:
        try:
            response = response.json()
            return response
        except Exception as e:
            print(response + '\n')
            print("----Restart ES and PRESS # TO CONTINUE----")
            while (True):
                a = keyboard.read_key()
                if a == '#':
                    break

if __name__ == '__main__':
    import sys
    try:
        _, DOMAIN = sys.argv
    except Exception as e:
        print('Usage: python spql.py DOMAIN')
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
                    # sparql for fb IDs entities + labels for the given entry
                    id = line.split(' ')[0]
                    out.write(id + ':' + line.split(' ')[1] + '\n')
                    resp = sparql(domain, id.split(':')[1])
                    resp = resp.get('results').get('bindings')
                    for binding in resp:
                        out.write(binding.get('o').get('value') + '\n')



sparql_main(DOMAIN)
