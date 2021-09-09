import math


# n - how many times sentence with words x and y appear in corpus - record
# dist - number terms between x and y in sentence
def evaluate_frequency_typed_terms(n: float, dist: int) -> float:
    return n * pow(math.e, -dist)


# fxy - all evaluated frequencies from all sentences with x, y using above equation
# fxz - sum of all evaluated frequencies from all sentences (including x and y - but mainly all)
# n - number of all typed terms
def get_graph_weight(fxy: float, fxz: float, n: float, nein: float) -> float:
    return (fxy / fxz) / math.log10(n / nein)
