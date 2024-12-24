class KnowledgeBase:
    """Class representing a Knowledge Base (KB)."""
    def __init__(self):
        self.clauses = set()

    def add_clause(self, clause):
        """Add a clause to the KB."""
        self.clauses.add(clause)

    def __str__(self):
        return '\n'.join(map(str, self.clauses))


def pl_resolve(ci, cj):
    """Perform resolution on two clauses."""
    resolved = set()
    for literal in ci:
        if -literal in cj:
            resolvent = (ci - {literal}) | (cj - {-literal})
            resolved.add(frozenset(resolvent))
    return resolved


def resolution(kb, query):
    """Apply the resolution algorithm to check if the query is entailed by the KB."""
    # Add negated query to the KB
    negated_query = {-q for q in query}
    kb.add_clause(frozenset(negated_query))

    new = set()

    while True:
        pairs = [(ci, cj) for ci in kb.clauses for cj in kb.clauses if ci != cj]
        for (ci, cj) in pairs:
            resolvents = pl_resolve(ci, cj)
            if frozenset() in resolvents:  # Empty clause found
                return True
            new.update(resolvents)

        if new.issubset(kb.clauses):
            return False

        kb.clauses.update(new)


# Example Usage
if __name__ == "__main__":
    kb = KnowledgeBase()

    # Represent clauses as sets of literals (positive integers for literals, negative for negated literals)
    # Example: Clause (A or not B) -> {1, -2}
    kb.add_clause(frozenset({1, -2}))
    kb.add_clause(frozenset({2}))
    kb.add_clause(frozenset({-1, 3}))

    # Query to test: Can we derive ~C (represented as {-3})
    query = {3}

    print("Knowledge Base:")
    print(kb)

    result = resolution(kb, query)
    print("Query is", "entailed" if result else "not entailed", "by the KB.")
