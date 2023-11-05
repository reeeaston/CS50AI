import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 1000000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    probabilityDist = corpus.copy()
    # A list of strings for all the names of the links we can visit
    links = corpus[page]

    # If no links, just make each probability equal
    if len(links) == 0:
        equalProb = (1 / len(corpus))
        for key in probabilityDist.keys():
            probabilityDist[key] = equalProb
        return probabilityDist

    # 0.15 * 1/4 for four total pages, prob of randomly getting a page weighted 
    # by the non-damping factor
    corpusProb = (1 - damping_factor) * (1 / len(corpus)) 
    # All pages get the same probability
    for key in probabilityDist.keys():
        probabilityDist[key] = corpusProb

    # 0.85 * 1/2 for two total links
    linkProb = (damping_factor) * (1 / len(links))
    # All pages that are linked to that page have the same probability
    for key in links:
        probabilityDist[key] += linkProb

    return probabilityDist


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # pageRank initially has all pages with 0 as their count (update to prob. later)
    pageRank = corpus.copy()
    pageNames = []
    for key in pageRank.keys():
        pageRank[key] = 0
        pageNames.append(key)

    # Initially choose a page at random
    index = random.randint(0, len(pageRank)-1)
    currentPage = pageNames[index]
    pageRank[currentPage] += 1

    # For all the other pages (9999 times)
    for i in range(n-1):
        # Get transition model for page
        distribution = transition_model(corpus, currentPage, damping_factor)
        # Randomly choose the page name
        chosenPage = random.choices(list(distribution.keys()), list(distribution.values()), k=1)[0]
        # Add 1 instance of the page being viewed to the pageRank
        pageRank[chosenPage] += 1
        # Make the chosen page the new current page
        currentPage = chosenPage

    # Divide the amount of times visited by the amount of times run for each key
    for key in pageRank.keys():
        pageRank[key] = pageRank[key] / n
            
    return pageRank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    probabilityDist = corpus.copy()
    newDist = corpus.copy()
    # Assign each page a rank of 1 / N (equal probability of being chosen)
    for key in probabilityDist.keys():
        probabilityDist[key] = 1 / len(corpus)
    # Assign none for each page in the new distribution
    for key in newDist.keys():
        newDist[key] = 0

    # Useful stuff for later
    N = len(corpus)
    equalProb = (1 - damping_factor) / N
    maxDiff = 1 / len(corpus)

    # Run until the values converge
    while maxDiff > 0.001:
        # For each page in probability distribution
        for p in probabilityDist.keys():
            surfProb = 0
            # Find all pages in corpus that links to p
            for i in corpus.keys():
                # If the page has no links, equal probability added
                if len(corpus[i]) == 0:
                    surfProb += probabilityDist[i] / len(corpus)
                # If a page links to p, add prob of getting page / prob of getting p
                if p in corpus[i]:
                    surfProb += probabilityDist[i] / len(corpus[i])
            surfProb *= damping_factor
            # Set the new distribution of that probability to the equality 
            # part plus the damping part where for every page i that links to page 
            # p, the probability of getting to i / number of links in i is added
            newDist[p] = equalProb + surfProb
        
        # Make sure the values add to 1
        total = sum(newDist.values())
        for key in newDist.keys():
            newDist[key] = newDist[key] / total

        # Get the new maximum change
        for key in newDist.keys():
            currentDiff = abs(newDist[key] - probabilityDist[key])
            maxDiff = currentDiff if currentDiff < maxDiff else maxDiff
        # New probability distribution becomes the current one
        probabilityDist = newDist.copy()


    return probabilityDist


if __name__ == "__main__":
    main()
