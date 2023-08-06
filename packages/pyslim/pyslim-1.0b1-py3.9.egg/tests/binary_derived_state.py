import msprime

tabs = msprime.TableCollection(sequence_length=1.0)
tabs.nodes.add_row()
tabs.nodes.add_row(time=1.0)
tabs.edges.add_row(left=0.0, right=1.0, parent=1, child=0)
tabs.sites.add_row(position=0.5, ancestral_state='')
tabs.mutations.add_row(site=0, node=0, derived_state=b'\x96\x00\x00\x00\x00\x00\x00\x00')

ts = msprime.load_tables(**tabs.asdict())

for m in ts.mutations():
    pass

