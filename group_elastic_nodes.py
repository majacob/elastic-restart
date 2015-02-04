import argparse
import networkx
from elasticsearch import Elasticsearch
import elasticsearch

parser = argparse.ArgumentParser()
parser.add_argument('--es_server', action='store', type=str, required=True)
parser.add_argument('--port', action='store', type=int, required=True)
parser.add_argument('--debug', action='store', type=bool, required=False)

args=parser.parse_args()


server=args.es_server;
pt=args.port;

if args.debug:
	debug=args.debug;
else:
	debug=False;

client=Elasticsearch(server, port=pt);
catClient=elasticsearch.client.CatClient(client);

data=catClient.shards(h='index,shard,node');
if debug:
	print data;

nl=[l.encode('ascii', 'ignore').strip() for l in data.split('\n') if len(l.encode('ascii', 'ignore').strip()) > 0];
G=networkx.Graph();


shard_nodes={};# dict that stores shard id --> (index_name, node) pairs
for line in nl:
	
	shards_nodes=line.strip().split();
	
	node=shards_nodes[2];
	shard=int(shards_nodes[1].strip());
	index=shards_nodes[0];

	if not node in G.nodes():
		G.add_node(node);


	if shard in shard_nodes:
		nodes_with_same_index_shard = [ n_with_same_shard[1] for n_with_same_shard in shard_nodes[shard] if n_with_same_shard[0]==index]
		for n_with_same_ishard in nodes_with_same_index_shard:
			G.add_edge(n_with_same_ishard, node);
		shard_nodes[shard].append((index, node))
	else:
		shard_nodes[shard]=[(index,node)];

	
if debug:
	print "Graph has "+str(len(G.nodes()))+ " nodes and "+str(len(G.edges()))+" edges"

#-----------------------------------------------------------
# Find maximum independent set using min vertex heuristic...

print "Random maximal set:"+str(networkx.maximal_independent_set(G));


def heuristic_approx(G):
	sorted_nodes=sorted(G.nodes(), key=lambda n: G.neighbors(n))
	
	iset=[];
	for n in sorted_nodes:
		if n in G.nodes():
			iset.append(n);
			G.remove_nodes_from(G.neighbors(n));
			G.remove_node(n);
	return iset;
print "Approx maximum Independent set:"+str(heuristic_approx(G));
