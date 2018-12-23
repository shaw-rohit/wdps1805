from collections import namedtuple
from requests import get

ElasticSearchResult = namedtuple('ElasticSearchResult', ['id', 'label', 'score'])


class ElasticSearcher:
    def __init__(self, address: str, default_count: int, mock: bool = False):
        self._address = address
        self._default_count = default_count
        self._request_get = get if not mock else get_mock

    def search(self, query: str, count: int = None) -> list:
        if count is None:
            count = self._default_count
        url = 'http://%s/freebase/label/_search' % self._address
        response = self._request_get(url, params={'q': query, 'size': count}).json()
        results = []
        for hit in response.get('hits', {}).get('hits', []):
            freebase_label = hit.get('_source', {}).get('label')
            freebase_id = hit.get('_source', {}).get('resource').split(':')[1]
            score = hit.get('_score')
            results.append(ElasticSearchResult(freebase_id, freebase_label, score))

        results.sort(key=lambda result: result.score)
        return results


class GetMock:
    def __init__(self, data):
        self._data = data

    def json(self):
        return self._data


def get_mock(_, params):
    mock = {'hits': {'hits': [{
        '_score': x,
        '_source': {
            'label': params['q'],
            'resource': 'fbase:fb-id-%s' % (hash(str(params['q'])) % 10000 + x)
        }
    } for x in range(3)]}}
    return GetMock(mock)
