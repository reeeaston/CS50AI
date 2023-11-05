import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])
    
    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]

# Find the number of genes a person has
def findNumGenes(person, one_gene, two_genes):
    if person in one_gene:
        return 1
    if person in two_genes:
        return 2
    return 0

# Find probability that person passes down the trait based on number of genes they have
def probPassTrait(num):
    if num == 1:
        return 0.5 * (1 - PROBS["mutation"]) + 0.5 * PROBS["mutation"]
    elif num == 2:
        return 1 - PROBS["mutation"]
    elif num == 0:
        return PROBS["mutation"]

def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    probabilities = []
    for person in people:
        # If a person doesn't have parents
        if people[person]['mother'] == None:
            # Identify num genes and trait status we want this person to have
            numGenes = findNumGenes(person, one_gene=one_gene, two_genes=two_genes)
            hasTrait = True if (person in have_trait) else False
            # Add probability that person has desired number of genes and trait
            probabilities.append(PROBS["gene"][numGenes] * PROBS["trait"][numGenes][hasTrait])
        else:
            # Identify num genes of parents and child
            numMom = findNumGenes(people[person]['mother'], one_gene=one_gene, two_genes=two_genes)
            numDad = findNumGenes(people[person]['father'], one_gene=one_gene, two_genes=two_genes)
            probMom = probPassTrait(numMom)
            probDad = probPassTrait(numDad)

            numGenes = findNumGenes(person, one_gene=one_gene, two_genes=two_genes)
            hasTrait = True if (person in have_trait) else False

            probTrait = 0
            if numGenes == 0:
                # Prob neither father nor mother passes down gene
                probTrait = (1-probDad) * (1-probMom)
            if numGenes == 2:
                # Prob both father and mother passes down gene
                probTrait = (probDad * probMom)
            if numGenes == 1:
                # Prob one passes down gene but other doesn't
                probTrait = ((probDad) * (1-probMom)) + (1-probDad) * (probMom)
            # Add probability that person has desired number of genes and trait
            probabilities.append(probTrait * PROBS["trait"][numGenes][hasTrait])

    finalProb = 1
    for probability in probabilities:
        finalProb *= probability
    return finalProb



def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        # Identify number of genes and if that person has the trait or not
        numGenes = findNumGenes(person, one_gene=one_gene, two_genes=two_genes)
        hasTrait = True if (person in have_trait) else False
        probabilities[person]["gene"][numGenes] += p
        probabilities[person]["trait"][hasTrait] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        total = 0
        # Get what the total amount adds up to
        for value in probabilities[person]["gene"].values():
            total += value
        for key in probabilities[person]["gene"].keys():
            probabilities[person]["gene"][key] = probabilities[person]["gene"][key] / total
        total = 0
        # Get what the total amount adds up to
        for value in probabilities[person]["trait"].values():
            total += value
        for key in probabilities[person]["trait"].keys():
            probabilities[person]["trait"][key] = probabilities[person]["trait"][key] / total


if __name__ == "__main__":
    main()
