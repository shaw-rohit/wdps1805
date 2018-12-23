from time import sleep
from requests import post, RequestException


class SparqlSearcher:
    def __init__(self, address: str, count: int, retry_attempts: int, retry_delay: float, mock: bool = False):
        self._address = address
        self._count = count
        self._attempts = retry_attempts
        self._delay = retry_delay
        self._post_request = post if not mock else post_mock

    def search(self, freebase_id: str):
        return self._search_retry(freebase_id, 1)

    def _search_retry(self, freebase_id, attempt) -> map:
        try:
            url = 'http://%s/sparql' % self._address
            query = 'select * where {<http://rdf.freebase.com/ns/%s> ?p ?o} limit %d' % (freebase_id, self._count)
            response = self._post_request(url, data={'print': True, 'query': query}).json()
            bindings = response.get('results').get('bindings')
            return map(lambda binding: binding.get('o').get('value'), bindings)
        except RequestException:
            if attempt == self._attempts:
                raise
            sleep(self._delay)
            return self._search_retry(freebase_id, attempt + 1)


class PostMock:
    def __init__(self, data):
        self._data = data

    def json(self):
        return self._data


def post_mock(_, data):
    freebase_id = data['query'].split('/')[1].split('>')[0]
    mock = {'results': {'bindings': [{
        'o': {'value': 'fb-id-%s->%d' % (freebase_id, x)}
    } for x in range(3)]}}
    return PostMock(mock)
