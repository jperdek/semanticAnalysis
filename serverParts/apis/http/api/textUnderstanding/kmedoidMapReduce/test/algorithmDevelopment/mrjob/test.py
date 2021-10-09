"""The classic MapReduce job: count the frequency of words.
"""
from mrjob.job import MRJob
import re



class MRWordFreqCount(MRJob):
    
    def mapper(self, _, line):
        for word in line:
            yield (word.lower(), 1)

    def combiner(self, word, counts):
        yield (word, sum(counts))

    def reducer(self, word, counts):
        yield (word, sum(counts))


if __name__ == '__main__':
     MRWordFreqCount.run()