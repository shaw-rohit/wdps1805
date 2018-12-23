from io import StringIO


class WarcRecord:
    def __init__(self, web_arch_record: str):
        self.id = None
        self.payload = None
        self.broken = None
        self._parse(web_arch_record)

    def _parse(self, web_arch_record):
        buffer = StringIO(web_arch_record.strip())
        # Parsing headers
        while True:
            line = buffer.readline().strip()
            if line == '':
                break
            if self.id is None and 'WARC-TREC-ID' in line:
                self.id = line.split('WARC-TREC-ID:')[1].strip()
        if self.id is None:
            self.broken = True
            return None
        # Maybe skip another set of headers
        line = buffer.readline().strip()
        if line.startswith('HTTP/'):
            line = ''
            while True:
                if buffer.readline().strip() == '':
                    break
        # Rest is payload
        self.payload = line + buffer.read().strip()
        self.broken = False
