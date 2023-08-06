import numpy as np
import networkx as nx
import pandas as pd

from scipy.spatial import distance

def generate_edgelist(df):
    """
    Description
    -----------
    Read a pandas DataFrame and generates an edge list vector to eventually build a networkx graph. The syntax of the
    file header is rigidly controlled and can't be changed. The header format must be: (node1, node2, weight).
    
    Parameters
    ----------
    df : pandas.DataFrame
        Pandas DataFrame edge list of the wanted network.
    
    Raises
    ------
    ValueError : An error is raised if the values of the DataFrame headers is not the required one.
    
    Returns
    -------
    output : list
        The output of the function is a list of tuples of the form (node_1, node_2, weight).
        
    Note
    ----
    - In order to generate a **networkx** object it's only required to give the list to the Graph() constructor
    >>> edgelist = xn2v.generate_edgelist(DataFrame)
    >>> G = nx.Graph()
    >>> G.add_weighted_edges_from(edgelist)
    - The data types of the 'node1' and 'node2' columns must be strings, otherwise they will be converted as strings.
    
    Examples
    --------
    >>> import pandas as pd
    >>> df = pd.DataFrame(np.array([[1, 2, 3.7], [1, 3, 0.33], [2, 7, 12]]), columns=['node1', 'node2', 'weight'])
    >>> edgelist = xn2v.generate_edgelist(df)
        [('1.0', '2.0', 3.7), ('1.0', '3.0', 0.33), ('2.0', '7.0', 12.0)]
    """
    # Check header:
    header_names = list(df.columns.values)
    if header_names[0] != 'node1' or header_names[1] != 'node2' or header_names[2] != 'weight':
        raise ValueError('The header format is different from the required one.')
    # Forcing values type
    df = df.astype({'node1': str, 'node2': str, 'weight': np.float64})
    return list(df.itertuples(index = False, name = None))

def edgelist_from_csv(path, **kwargs):
    """
    Description
    -----------
    Read a .csv file using pandas dataframes and generates an edge list vector to eventually build a networkx graph.
    The syntax of the file header is rigidly controlled and can't be changed.
    
    Parameters
    ----------
    path : string
        Path or name of the .csv file to be loaded.
    **kwargs :  pandas.read_csv() arguments
    
    Raises
    ------
    ValueError : An error is raised if the values of the DataFrame headers is not the required one.
    
    Returns
    -------
    output : list
        The output of the function is a list of tuples of the form (node_1, node_2, weight).
        
    Note
    ----
    - In order to generate a **networkx** object it's only required to give the list to the Graph() constructor
    >>> edgelist = xn2v.edgelist_from_csv('some_edgelist.csv')
    >>> G = nx.Graph()
    >>> G.add_weighted_edges_from(edgelist)
    - The data types of the 'node1' and 'node2' columns must be strings, otherwise they will be converted as strings.
    
    Examples
    --------
    >>> edgelist = xn2v.edgelist_from_csv('somefile.csv')
        [('a','1',3.4),('a','2',0.6),('a','b',10)]
    """
    df_csv = pd.read_csv(path, dtype = {'node1': str, 'node2': str, 'weight': np.float64}, **kwargs)
    # Check header:
    header_names = list(df_csv.columns.values)
    if header_names[0] != 'node1' or header_names[1] != 'node2' or header_names[2] != 'weight':
        raise ValueError('The header format is different from the required one.')
    return list(df_csv.itertuples(index = False, name = None))

def complete_edgelist(Z, metric='euclidean', **kwargs):
    """
    Description
    -----------
    This function performs a **data transformation** from the space points to a network. It generates links between
    specific points and gives them weights according to the specified metric.
    
    Parameters
    ----------
    Z : numpy ndarray
        Numpy array containing as columns the i-th coordinate of the k-th point. The rows are the points, the columns
        are the coordinates.
    metric : string, optional
        Specifies the metric in which the dataset Z is defined. The metric will determine the values of the weights
        between the links.
        
    Returns
    -------
    output : pandas DataFrame
        Edge list created from the given dataset expressed as a Pandas DataFrame.
        
    Examples
    --------
    >>> x1 = np.random.normal(7, 1, 3)
    >>> y1 = np.random.normal(9, 1, 3)
    >>> points = np.column_stack((x1, y1))
    >>> df = xn2v.complete_edgelist(points)
          node1 node2    weight
        0     0     0  1.000000
        1     0     1  0.015445
        2     0     2  0.018235
        3     1     0  0.015445
        4     1     1  1.000000
        5     1     2  0.834821
        6     2     0  0.018235
        7     2     1  0.834821
        8     2     2  1.000000
    """
    dimension = Z[0].size # Number of coordinates per point
    NPoints = Z[:, 0].size # Number of points
    weights = np.exp(-distance.cdist(Z, Z, metric)) # Distance between all points
    np.fill_diagonal(weights, 0) # Zero weight on self loops
    weights = weights.flatten() # Weights coulumn
    nodes_id = np.arange(NPoints).astype(str)
    node1 = np.repeat(nodes_id,NPoints)
    node2 = np.tile(nodes_id,NPoints)
    df = pd.DataFrame({'node1': node1, 'node2': node2, 'weight': weights}, **kwargs)
    return df

def stellar_edgelist(Z, **kwargs):
    """
    Description
    -----------
    This function performs a **data transformation** from the space points to a network. It generates links between
    specific points and gives them weights according to specific conditions.
    
    Parameters
    ----------
    Z : numpy ndarray
        Numpy array containing as columns the i-th coordinate of the k-th point. The rows are the points, the columns
        are the coordinates.
        
    Returns
    -------
    output : pandas DataFrame
        Edge list created from the given dataset expressed as a Pandas DataFrame.
        
    Examples
    --------
    >>> x1 = np.random.normal(7, 1, 6)
    >>> y1 = np.random.normal(9, 1, 6)
    >>> points_1 = np.column_stack((x1, y1))
    >>> df = xn2v.stellar_edgelist(points_1)
          node1      node2     weight
        0     origin     0  12.571278
        1     origin     1  11.765633
        2     origin     2   9.735974
        3     origin     3  12.181443
        4     origin     4  11.027584
        5     origin     5  12.755861
    >>> x2 = np.random.normal(107, 2, 3)
    >>> y2 = np.random.normal(101, 1, 3)
    >>> points_2 = np.column_stack((x2, y2))
    >>> tot = np.concatenate((points_1,points_2),axis=0)
    >>> df = xn2v.stellar_edgelist(tot)
          node1      node2     weight
        0     origin     0  12.571278
        1     origin     1  11.765633
        2     origin     2   9.735974
        3     origin     3  12.181443
        4     origin     4  11.027584
        5     origin     5  12.755861
        6     origin     6  146.229997
        7     origin     7  146.952899
        8     origin     8  146.595700
    """
    dimension = Z[0].size  # Number of coordinates per point
    NPoints = Z[:, 0].size  # Number of points
    dimension = Z[0].size  # Number of coordinates per point
    NPoints = Z[:, 0].size  # Number of points
    weights = np.exp(-np.linalg.norm(Z, axis = 1))
    node2 = np.arange(NPoints).astype(str)
    df = pd.DataFrame({'node1': 'origin', 'node2': node2, 'weight': weights}, **kwargs)
    return df
  
