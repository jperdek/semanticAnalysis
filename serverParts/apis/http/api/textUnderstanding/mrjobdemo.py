from mrjob.job import MRJob
from mrjob.step import MRStep

import re

WORD_RE = re.compile(r"[0-9]+")


class MRBirthCounter(MRJob):
    # def mapper(self, key, record):
    #    yield record[14:20], 1

    # def reducer(self, month, births):
    #    yield month, sum(births)

    def mapper(self, _, line):
        for word in WORD_RE.findall(line):
            yield word.lower(), 1

    def reducer(self, word, counts):
        yield word, sum(counts)

    def steps(self):
        return [MRStep(mapper=self.mapper, reducer=self.reducer)]


if __name__ == '__main__':
    MRBirthCounter.run()