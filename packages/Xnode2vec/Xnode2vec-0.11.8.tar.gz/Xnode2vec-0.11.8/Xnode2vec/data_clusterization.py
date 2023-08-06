from fastnode2vec import Node2Vec, Graph
from gensim.models import Word2Vec
import numpy as np
import networkx as nx

import warnings
from tqdm import tqdm

from .data_management import nx_to_Graph

# cache global variable
_cache = dict()


def clear_cache():
    """
    Description
    -----------
    Simple warp of dict.clear() function.

    """
    print("\nClearing cache ..\n")
    print(f'removing: {list(_cache.keys())}')
    
    _cache.clear()


def low_limit_network(G, delta : float, remove=False) -> nx.Graph:
    """
    Description
    -----------
    This function performs a **network transformation**. It sets the link weights of the network to 0 if their initial
    value was below a given threshold. The threshold is chosen to be a constant times the average links weight.

    Parameters
    ----------
    G : networkx.Graph()
        Gives the network that will be modified.
    delta :  float
        Set the multiplying constant of the maximum link weight that will define the weight threshold. This number
        should be between 0 and 1.
    Returns
    -------
    output : networkx.Graph()
        Returns the networkx graph() resulting after the transformation.

    Examples
    --------
    >>> print(G)
    Graph with 300 nodes and 45150 edges
    >>> G = xn2v.low_limit_network(G, 0.5, remove=True)
    >>> print(G)
    Graph with 300 nodes and 14702 edges
    """

    link_weights = nx.get_edge_attributes(G, 'weight')
    weights = np.array(list(link_weights.values())).astype(float)
    max_weight = np.amax(weights)

    if remove == True:

        to_remove = []

        for u, v, d in G.edges(data = True):
            if d['weight'] <= delta * max_weight:
                to_remove.append((u, v))

        G.remove_edges_from(to_remove)

    else:

        for u, v, d in G.edges(data = True):
            if d['weight'] <= delta * max_weight:
                d['weight'] = 0.

    return G


def cluster_generation(result, cluster_rigidity=0.7) -> np.array:
    """
    Description
    -----------
    This function takes the nodes that have a similarity higher than the one set by *cluster_rigidity*.
    Parameters
    ----------
    result : list
        This parameter must be a list of two elements: the first is the nodes labels vector, the other is their
        similarities vector.
    cluster_rigidity : float, optional
        Sets the similarity threshold of the nodes. It should be a number between 0 and 1. The default value is
        '0.7'.

    Returns
    -------
    output : numpy ndarray
        The output is a numpy array containing the nodes that satisfy the condition required.
    Examples
    --------
    >>> nodes = np.arange(0,5)
        [0 1 2 3 4]
    >>> similarities = [0.5,0.9,0.91,0.87,0.67]
    >>> xn2v.cluster_generation([nodes,similarities], cluster_rigidity = 0.75)
        ['1' '2' '3']
    """

    cluster = np.array(result[0], dtype = str)
    positions = np.where(np.array(result[1]) >= cluster_rigidity)
    return cluster[positions]


def similar_nodes(G, node=1, picked=10, Epochs=30, Weight=True, model_name=None,
                  graph=None, **kwargs):
    """
    Description
    -----------
    Performs FastNode2Vec algorithm with full control on the crucial parameters.
    In particular, this function allows the user to keep working with networkx objects
    -- that are generally quite user-friendly -- instead of the ones required by the fastnode2vec
    algorithm.

    Parameters
    ----------
    G : networkx.Graph object
        Sets the network that will be analyzed by the algorithm.
    p : float
        Sets the probability '1/p' necessary to perform the fastnode2vec random walk. It affects how often the walk is
        going to immediately revisit the previous node. The smaller it is, the more likely the node will be revisited.
    q : float
        Sets the probability '1/q' necessary to perform the fastnode2vec random walk. It affects how far the walk
        will go into the network. The smaller it is, the larger will be the distance from the initial node.
    graph : fastnode2vec.Graph object, optional
        Tells if the algorithm should perform a **networkx** to **Graph** conversion first, or if it has been already
        done.
        The default value is 'None'.
    node : int, optional
        Sets the node from which to start the analysis. This is a gensim.models.word2vec parameter.
        The default value is '1'.
    walk_length : int
        Sets the number of jumps to perform from node to node.
    save_model : bool, optional
        Saves in the working directory a .wordvectors file that contains the performed training.
        It's important to consider is that the **methods** of the "Word2Vec" model saved can be accessed
        as "model_name.wv". The documentation of ".wv" is found however under
        "gensim.models.keyedvectors.KeyedVectors" istance; they are the same thing, ".wv" is just a rename.
        The default value is 'False'.
    picked : int, optional
        Sets the first 'picked' nodes that are most similar to the node identified with 'node'. This is a
        gensim.models.word2vec parameter.
        The default value is '10'.
    train_time : int, optional
        Sets the number of times we want to apply the algorithm. It is the 'epochs' parameter in Node2Vec.
        The value of this parameter drastically affect the computational time.
        The default value is '5'.
    Weight : bool, optional
        Specifies if the algorithm must also consider the weights of the links. If the networks is unweighted this
        parameter must be 'False', otherwise it receives too many parameters to unpack.
        The default value is 'False'.
    dim : int, optional
        This is the Word2Vec "size" argument. It sets the dimension of the algorithm word vector. The longer it is, the
        more complex is the specification of the word -- object. If a subject has few features, the word length should
        be relatively short.
        The default value is '128'.
    context : int, optional
        This is the Word2Vec `window` parameter. Depending on its value, it manages to obtain words that are
        interchangeable and relatable -- belonging to the same topic. If the value is small, 2-15, then we will likely
        have interchangeable words, while if it is large, >15, we will have relatable words.
        It is namely the maximum distance between the current and predicted word within a `sentence`.
        The default value is '10'

    Returns
    -------
    output : ndarray, ndarray
        The output of the function is a tuple of two numpy arrays. The first contains the top 'picked' most similar
        nodes to the 'node' one, while the second contains their similarities with respect to the 'node' one. The
        similarity is calculated as the `cosine similarity` between the vectors relative to the words themselves.
        Clearly, the dimension of the word vectors is given by `dim` parameter.

    Notes
    -----
    - The node parameter is by default an integer. However, this only depends on the node labels that are given to the
      nodes in the network.
    - The rest of the parameters in **kwargs are the ones in fastnode2vec.Node2Vec constructor, I only specified what I
      considered to be the most important ones.

    Examples
    --------
    >>> G = nx.generators.balanced_tree(r=3, h=4)
    >>> nodes, similarity = xn2v.similar_nodes(G, dim=128, walk_length=30, context=10,
    >>>                                   p=0.1, q=0.9, workers=4)
        nodes: [0 4 5 6 45 40 14 43 13 64]
        similarity: [0.81231129 0.81083304 0.760795 0.7228986 0.66750246 0.64997339
                     0.64365959 0.64236712 0.63170493 0.63144475]
    """
    if graph is None:

        if 'graph' not in _cache:
            print("\nCaching trained graph ..\n")
            _cache['graph'] = nx_to_Graph(G, Weight)

        n2v = Node2Vec(_cache['graph'], **kwargs)

    else:

        n2v = Node2Vec(graph, **kwargs)

    n2v.train(epochs = Epochs, progress_bar = False)

    if model_name is not None:
        n2v.save(model_name)

    nodes = n2v.wv.most_similar(node, topn = picked)
    nodes_id = list(list(zip(*nodes))[0])
    similarity = list(list(zip(*nodes))[1])
    nodes_id = np.array(nodes_id)
    similarity = np.array(similarity)

    return nodes_id, similarity


def clusters_detection(G, cluster_rigidity=0.7, spacing=5, dim_fraction=0.8, **kwargs) -> list:
    """
    Description
    -----------
    This function detects the **clusters** that compose a generic dataset. The dataset must be given as a
    **networkx** graph, using the proper data transformation. The clustering procedure uses Node2Vec algorithm to
    find the most similar nodes in the network.

    Parameters
    ----------
    G : networkx.Graph()
        Gives the network that will be analyzed.
    cluster_rigidity : float, optional
        Sets the similarity threshold of the nodes. It should be a number between 0 and 1. The default value is
        '0.7'.
    spacing : int, optional
        Sets the increment of the position when picking the nodes for the analysis. The nodes are picked every
        *spacing* value between the initial node label and the last one. The default value is '5'.
    dim_fraction : float, optional
        Sets the minumum threshold for choosing when to expand the previously generated cluster. This parameter
        appears when considering the current most similar nodes picked by the Node2Vec algorithm; in particular
        it sets the minumum number of nodes that are already present in the generated clusters family before adding
        the remaining ones to the previous cluster.

    Note
    ----
    - The function returns only the nodes labels from a specific network. In order to go back to the initial points
      it's necessary to use the function **xn2v.recover_points(dataset,Graph,Clusters[i])**. Up to now, you can
      insert only a one-dimensional vector inside **xn2v.recover_points()**, meaning that if you have N clusters
      inside the list obtained by **xn2v.clusters_detection()** you'll have to call **xn2v.recover_points()**
      N times.

    Returns
    -------
    output : list
        The output is list of numpy arrays containing nodes labels from the given network *G*. Each array represents
        a specific cluster.

    Examples
    --------
    >>> df = xn2v.edgelist_from_csv('somefile.csv')
    >>> df = xn2v.generate_edgelist(df)
    >>> xn2v.clusters_detection(G, cluster_rigidity = 0.75, spacing = 5, dim_fraction = 0.8, picked=100,
    >>>                         dim=100,context=5,Weight=True, walk_length=20)
        --------- Clusters Information ---------
        - Number of Clusters:  3
        - Total nodes:  61
        - Clustered nodes:  52
        - Number of unlabeled nodes:  9
        - Nodes in cluster 1: 18
        - Nodes in cluster 2: 17
        - Nodes in cluster 3: 17
        [array(['1', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19',
        '2', '3', '4', '5', '6', '7', '9'], dtype='<U2'),
        array(['21', '23', '24', '26', '27', '28', '29', '30', '31', '32', '33',
        '34', '35', '36', '37', '38', '39'], dtype='<U2'),
        array(['41', '42', '44', '45', '47', '48', '49', '50', '51', '52', '53',
        '54', '55', '56', '57', '58', '59'], dtype='<U2')]
    """
    clusters = []
    nodes_clustered = []
    index = 0
    for node_id in tqdm(list(G.nodes)[::spacing], desc = "Training: "):

        flag = True
        nodes, similarities = similar_nodes(G, node_id, **kwargs)
        current_cluster = cluster_generation([nodes, similarities], cluster_rigidity)  # TESTING THIS OBJECT.
        current_cluster = np.append(current_cluster, node_id)  # Add current node to current_cluster
        dimension = np.size(current_cluster)
        different_nodes_counters = []  # This is used to find the cluster to expand and to decide whether to create a new cluster.

        if len(clusters) != 0:

            copy_current_cluster = current_cluster  # Needs because current cluster GETS FILTERED, so it cant be used in new_nodes_positions.

            for previous_cluster in clusters:
                # True = already in, False = new node. This is inverted, so True = new node.

                # Needs for filtering the current cluster.
                current_positions = np.invert(np.isin(current_cluster, previous_cluster))
                # Needs for comparison with the previous clusters.
                new_nodes_positions = np.invert(np.isin(copy_current_cluster, previous_cluster))
                # Number of DIFFERENT nodes compared to each existing cluster,then we take the MIN.
                different_nodes_counters.append(new_nodes_positions.sum())
                # current_cluster filtering (removing existing nodes).
                current_cluster = current_cluster[~np.in1d(current_cluster, previous_cluster)]

        if dimension == np.size(current_cluster):

            # Creating new cluster if the dimension of cluster remain the same. This means that the nodes in common are none.
            if dimension == 1:  # If the current cluster is empty, skip the process. (empty means with only current node)
                warnings.warn("Warning: The dimension of the cluster is 0. You may want to reduce cluster_rigidity.",
                              RuntimeWarning)
                flag = False

            if flag == True:
                index += 1
                print(f"- Creating new cluster: {index}")
                clusters.append(current_cluster)

        elif dimension - np.size(current_cluster) < int(dimension * dim_fraction):
            # - If all nodes are different, dimension-np.size(current_cluster)==0 => Create new cluster.
            # - If all nodes are the same, dimension-np.size(current_cluster)==dimension => Expand with nothing.
            # - If some nodes are different, dimension-np.size(current_cluster)>0:
            #       if dimension-np.size(current_cluster)<threshold => There are enough SAME nodes to expand the clusters.
            ind = np.where(different_nodes_counters == np.min(different_nodes_counters))

            if ind[0].size != 1:  # Don't expand if there are ambiguities on where put the nodes.
                pass
            
            else:
                # We extend the cluster that had the highest number of nodes in common. The current_cluster array is
                # already filtered with the different nodes in the whole clusters list.
                print(f"- Expand cluster number: {ind[0][0] + 1}")
                clusters[ind[0][0]] = np.append(clusters[ind[0][0]], current_cluster)
        
        else:
            pass

    tot_nodes = [val for sublist in clusters for val in sublist]
    unlabeled = list(set(np.array(list(G.nodes)).astype(str)) - set(tot_nodes))  # Get remaining nodes
    return clusters, unlabeled
