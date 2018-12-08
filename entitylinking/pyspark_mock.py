import logging


# noinspection PyPep8Naming
class SynchronousRDD:
    def __init__(self, rows):
        self._rows = rows

    def flatMap(self, mapper):
        mapped = [value for row in self._rows for value in mapper(row)]
        return SynchronousRDD(mapped)

    def map(self, mapper):
        mapped = [mapper(row) for row in self._rows]
        return SynchronousRDD(mapped)

    def saveAsTextFile(self, file_path: str):
        with open(file_path, 'w', encoding='utf-8') as file:
            for row in self._rows:
                file.write(str(row) + '\n')


# noinspection PyPep8Naming
class SparkContext:
    def __init__(self, _1, _2):
        pass

    @staticmethod
    def newAPIHadoopFile(file_path: str, *_1, conf: dict) -> SynchronousRDD:
        delimiter = conf['textinputformat.record.delimiter']
        logging.debug('Reading file from disk...')
        with open(file_path, 'rb') as file:
            rows = [record for record in file_split(file, delimiter, 4096)]
            logging.debug('Read file from disk complete, total pages: %d', len(rows))
            return SynchronousRDD(rows)


# https://stackoverflow.com/questions/10183784/
def file_split(f, delimiter=',', buffer_size=1024):
    prev = ''
    while True:
        s = f.read(buffer_size).decode('utf-8', 'ignore')
        if not s:
            break
        split = s.split(delimiter)
        if len(split) > 1:
            if prev + split[0]:
                yield prev + split[0]
            prev = split[-1]
            for x in split[1:-1]:
                yield x
        else:
            prev += s
    if prev:
        yield prev
