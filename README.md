
Elasticsearch script to compute a set of nodes that do not overlap in shard placements.

# Description

To do a rolling restart of an elasticsearch cluster (for whatever reason - maintenance, upgrades etc), you'll need to take down a set of nodes each time, without causing downtime for any particular shard. The script 'group_elastic_nodes.py' gets the shard placements from your es server, and computes a set of nodes that you can shut off without causing your cluster to go into the red state (i.e. the primary of each shard should still be available).


# Required python libraries:

- elasticsearch python client (http://elasticsearch-py.rtfd.org/)
- networkx (https://networkx.github.io/)

