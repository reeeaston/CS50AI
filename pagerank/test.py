import random
from pagerank import transition_model, sample_pagerank, iterate_pagerank

DAMPING = 0.85
SAMPLES = 1000000

dampAmnt = 0
corpusAmnt = 0

corpus = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}
p = "1.html"
damping_factor = 0.85

print(sample_pagerank(corpus, damping_factor, SAMPLES))
print(iterate_pagerank(corpus, damping_factor))




