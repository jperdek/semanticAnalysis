"""The classic MapReduce job: count the frequency of words.
"""
from mrjob.job import MRJob
import re
import sys
WORD_RE = re.compile(r"[\w']+")


class MRWordFreqCount(MRJob):

    FILES = ["clusteronly.txt"]
	
    def __init__(self, *args, **kwargs):
        MRJob.__init__(self, *args, **kwargs)
        for index, ar in enumerate(sys.argv):
            if ar == '--config-file':
                path = sys.argv[index + 1]
                path = path[path.rfind('/') + 1:]
        self.lines = [line for line in open(path, "r", encoding="utf-8")]

    def configure_args(self):
        super(MRWordFreqCount, self).configure_args()
        self.add_file_arg('--config-file', dest='config_file', default=None, help='file with labels', action="append")

    aa = dict()
    def mapper(self, _, line):
        for word in WORD_RE.findall(line):
            yield (word.lower(), 1)

    def combiner(self, word, counts):
        yield (word, sum(counts))

    def reducer(self, word, counts):
        yield (word, sum(counts))

    def reducer_final(self):
        for line in self.lines:
            yield (line, 1)
        yield('a', 1)


if __name__ == '__main__':
     MRWordFreqCount.run()

# python3 test.py README.rst -r hadoop --jobconf mapreduce.job.reducers=1 --config-file hdfs://localhost:9000/clusteronly.txt >  count2
# python3 test.py README.rst -r hadoop --jobconf mapreduce.job.reducers=1 --config-file hdfs://localhost:9000/clusteronly.txt >  count2
