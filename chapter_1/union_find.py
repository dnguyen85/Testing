import fileinput

class UnionFind:
    def __init__(self, N):
        self._id = list(range(N))   # id[i] is the component id for site i, initialized to itself
        self._sz = [1] * N          # node count for the component rooted at site index i 
        self._count = N             # number of components

    def count(self):
        """Returns number of components in the Union-Find data struct"""
        return self._count

    def connected(self, p, q):
        """return true if p is connected to q"""
        return self.find(p) == self.find(q)

    def find(self, p):
        """return component identifier for p"""
        while p != self._id[p]:
            p = self._id[p]
        return p

    def union(self, p, q):
        """add a connection btw p and q"""
        # Find roots for p and q
        i = self.find(p)
        j = self.find(q)

        # If same root
        if i == j: return

        # Make smaller root point to larger one
        if self._sz[i] < self._sz[j]:
            # Update root for i node to point to j
            self._id[i] = j
            self._sz[j] += self._sz[i]
        else:
            # Update root for j to point to i
            self._id[j] = i
            self._sz[i] += self._sz[j]

        self._count -= 1
            

def main():
    # Open the file stated on command line
    with fileinput.input() as f:
        n_sites = int(next(f))      # Get the number of sites
        uf = UnionFind(n_sites)     # Initialize UF data struct
        for line in f:
            p, q = [int(x) for x in line.split()]   # Get the pair of sites
            if uf.connected(p, q):                  # Ignore if already connected
                continue
            uf.union(p, q)                          # Connect the 2 sites
            print(p, q)                             # Print them out

    print(uf.count(), "components")


if __name__ == "__main__":
    main()

        
