import numpy as np
import networkx as nx

from skspatial.objects import Line

def best_line_projection(Z):
    """
    Description
    -----------
    Performs a linear best fit of the dataset points and projects them on the line itself.
    
    Parameters
    ----------
    Z : numpy ndarray
        Numpy array containing as columns the i-th coordinate of the k-th point. The rows are the points, the columns
        are the coordinates.
        
    Returns
    -------
    output : numpy ndarray
        The output of the function is a numpy ndarray containing the transformed points of the dataset.
        
    Examples
    --------
    >>> x1 = np.random.normal(7, 1, 6)
    >>> y1 = np.random.normal(9, 1, 6)
    >>> points = np.column_stack((x1, y1))
    >>> xn2v.best_line_projection(points)
        [[-0.15079291  1.12774076]
         [ 2.65759595  4.44293266]
         [ 3.49319696  5.42932658]]
    """
    a = Line.best_fit(Z)
    NPoints = Z[:, 0].size
    dimension = Z[0].size
    projections = []
    for i in range(0, NPoints):
        projections.extend(np.array(a.project_point(Z[i])))
    projections = np.reshape(projections, (NPoints, dimension))
    return projections
  
def recover_points(Z, G, nodes):
    """
    Description
    -----------
    Recovers the spatial points from the analyzed network. It uses the fact that the order of the nodes that build
    the network is the same as the dataset one, therefore there is a one-to-one correspondence between nodes and
    points.
    
    Parameters
    ----------
    Z : numpy ndarray
        Numpy array containing as columns the i-th coordinate of the k-th point. The rows are the points, the columns
        are the coordinates.
    G : networkx.Graph()
        Gives the network that has been analyzed.
    nodes : list
        List of the *most similar nodes* obtained after the analysis on the network G. The type is forced to be a
        string.
        
    Returns
    -------
    output : numpy ndarray
        The output of the function is a numpy ndarray containing the required points from the dataset.
        
    Examples
    --------
    >>> x1 = np.random.normal(16, 2, 30)
    >>> y1 = np.random.normal(9, 2, 30)
    >>> x2 = np.random.normal(100, 2, 30)
    >>> y2 = np.random.normal(100, 2, 30)
    >>> family1 = np.column_stack((x1, y1)) # REQUIRED ARRAY FORMAT
    >>> family2 = np.column_stack((x2, y2)) # REQUIRED ARRAY FORMAT
    >>> dataset = np.concatenate((family1,family2),axis=0) # Generic dataset
    >>> df = xn2v.complete_edgelist(dataset) # Pandas edge list generation
    >>> df = xn2v.generate_edgelist(df)
    >>> G = nx.Graph()
    >>> G.add_weighted_edges_from(df)
    >>> nodes, similarity = xn2v.similar_nodes(G,node='1',picked=10,walk_length=20,dim=100,context=5,Weight=True)
    >>> cluseter = xn2v.recover_points(dataset,G,nodes)
    [[17.98575878  8.99318017]
     [18.03438744  9.46128979]
     [15.83803679 10.39565391]
     [15.95210332 10.4135796 ]
     [19.44550252 12.7551321 ]
     [18.62321691 10.7604561 ]
     [16.30640697 12.15702448]
     [18.73718742 13.99351914]
     [18.7817838   7.92318885]
     [16.15456589 10.72636297]]
    """
    # Check dimensionality
    if np.array(G.nodes)[0] == 'origin':
        if Z[:,0].size+1 != np.array(G.nodes).size:
            raise ValueError(f"Error: the dataset dimension dim={Z[:, 0].size} is different from the one expected for the network dim={np.array(G.nodes).size}.")
        else: Z = np.insert(Z, 0, np.zeros(Z[0].size), axis=0) # Adding origin
    elif Z[:,0].size != np.array(G.nodes).size:
            raise ValueError(f"Error: the dataset dimension dim={Z[:, 0].size} is different from the one of the network dim={np.array(G.nodes).size}.")
    # Force string type
    nodes = [str(s) for s in nodes]
    picked_nodes = []
    pos = 0
    for n in G:
        if n in nodes:
            picked_nodes.append(Z[pos])
        pos += 1
    return np.array(picked_nodes)
  
