import msprime
import pyslim

ts = msprime.simulate(10, recombination_rate=0.01, length=100, mutation_rate=0.1)
new_ts = pyslim.mutate(ts, mutation_rate=0.2)

for h in new_ts.haplotypes():
    print(h)
