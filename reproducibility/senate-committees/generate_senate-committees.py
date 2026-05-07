from hypergraphx import Hypergraph


def load_hyperedges(name):
    path = "{}/hyperedges-{}.txt".format(name, name)
    hyperedges = {}
    weighted = False
    with open(path) as f:
        for line in f:
            h = tuple(sorted(map(int, line.strip().split(','))))
            if h not in hyperedges:
                hyperedges[h] = 0
            hyperedges[h] += 1
            if hyperedges[h] > 1:
                weighted = True
    
    return hyperedges, weighted

def load_nodes(name):
    path1 = "{}/label-names-{}.txt".format(name, name)
    path2 = "{}/node-labels-{}.txt".format(name, name)
    path3 = "{}/node-names-{}.txt".format(name, name)

    f = open(path1, "r")
    labels = f.readlines()
    f.close()
    f = open(path2, "r")
    node_labels = f.readlines()
    f.close()
    f = open(path3, "r")
    node_names = f.readlines()
    f.close()

    id2label = {}
    for i in range(len(labels)):
        id2label[i+1] = labels[i].strip()

    nodes = {}

    for i in range(len(node_names)):
        nodes[i+1] = {
            "name": node_names[i].strip(),
            "label": id2label[int(node_labels[i].strip())]
        }

    return nodes


from hypergraphx.readwrite import save_hypergraph

if __name__ == "__main__":
    dataset_name = "senate-committees"
    h, w = load_hyperedges(dataset_name)
    n = load_nodes(dataset_name)

    H = Hypergraph(weighted=w)

    for node in n:
        H.add_node(node, metadata=n[node])

    for hyperedge in h:
        if w:
            H.add_edge(hyperedge, weight=h[hyperedge])
        else:
            H.add_edge(hyperedge)

    H.set_attr_to_hypergraph_metadata("name", dataset_name)
    H.set_attr_to_hypergraph_metadata("version", "1.0.0")
    save_hypergraph(H, "{}.json".format(dataset_name))
    save_hypergraph(H, "{}.hgx".format(dataset_name), binary=True)

    from hypergraphx.readwrite import load_hypergraph
    a = load_hypergraph("{}.json".format(dataset_name))
    print(a.get_hypergraph_metadata())
    print(len(a.get_nodes()))
    print(len(a.get_edges()))
    print(sum(a.get_weights()))
    b = load_hypergraph("{}.hgx".format(dataset_name))
    print(b.get_hypergraph_metadata())
    print(len(b.get_nodes()))
    print(len(b.get_edges()))
    print(sum(a.get_weights()))

