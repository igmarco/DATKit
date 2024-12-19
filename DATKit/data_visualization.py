from DATKit.tools.chart_tools import plot_linechart, plot_heatmap, plot_dendrogram
from DATKit.data_integration import generate_spectra
from DATKit.distance_computing import generate_distance_matrix, generate_linkage_matrix


def generate_linechart(df, name='linechart.svg'):
    """
    Generates a linechart based on the interpolated data from the given DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame
        A DataFrame where each row corresponds to a sample and columns contain features.
    name : str, optional, default='heatmap.svg'
        The filename where the linechart image will be saved.

    Returns
    ----------
    None
        Saves the linechart image to the specified file.
    """
    # Obtain the spectra
    spectra, names = generate_spectra(df)
    x = df['points'].values

    # Plot the linechart
    plot_linechart(spectra, x, names, name=name)


def generate_heatmap(df, metric='correlation', name='heatmap.svg'):
    """
    Generates a heatmap based on the distance matrix computed from the given dataframe.

    Parameters
    ----------
    df : pandas.DataFrame
        A DataFrame where each row corresponds to a sample and columns contain features.
    metric : str, optional, default='correlation'
        The distance metric to use when computing the distance matrix. Supported metrics are:
        - 'correlation': Correlation distance.
        - 'cosine': Cosine distance.
        - 'euclidean': Euclidean distance.
        - 'jaccard': Jaccard distance.
        - 'hamming': Hamming distance.
        - 'minkowski': Minkowski distance (requires p in kwargs).
        - 'pearson': Pearson correlation (returns 1 - absolute correlation).
        - 'spearman': Spearman correlation (returns 1 - absolute correlation).
    name : str, optional, default='heatmap.svg'
        The filename where the heatmap image will be saved.

    Returns
    ----------
    None
        Saves the heatmap image to the specified file.

    Raises
    ------
    ValueError
        If an unsupported metric is specified.
    """
    # Generate the distance matrix using the given metric
    try:
        distance_matrix, names = generate_distance_matrix(df, metric)  # Convertimos las filas en muestras
    except ValueError:
        raise ValueError(f"Metric {metric} is not supported.")

    # Create the similarity matrix
    similarity_matrix = 1 - distance_matrix

    # Plot the heatmap
    plot_heatmap(similarity_matrix, names, metric=metric, name=name)


def generate_dendrogram(df, linkage_method='average', metric='correlation', threshold=0, name='dendrogram.svg'):
    """
    Generates a dendrogram based on hierarchical clustering.

    Parameters
    ----------
    df : dataframe
        A dataframe where each row corresponds to a sample and columns contain features.
    linkage_method : string
        The linkage method for building the dendrogram: 'ward', 'complete', 'average', 'single'.
    metric : str
        The distance metric to use when computing the distance matrix. Supported metrics are:
        - 'correlation': Correlation distance.
        - 'cosine': Cosine distance.
        - 'euclidean': Euclidean distance.
        - 'jaccard': Jaccard distance.
        - 'hamming': Hamming distance.
        - 'minkowski': Minkowski distance (requires p in kwargs).
        - 'pearson': Pearson correlation (returns 1 - absolute correlation).
        - 'spearman': Spearman correlation (returns 1 - absolute correlation).
    threshold : float
        The threshold to form clusters.
    name : string
        The filename where the dendrogram image will be saved.

    Returns
    ----------
    None
        Saves the dendrogram image to the specified file.

    Raises
    ------
    ValueError
        If an unsupported metric is specified.
    """

    try:
        # Compute the distance matrix and sample names
        distance_matrix, names = generate_distance_matrix(df, metric)
    except ValueError:
        raise ValueError(f"Metric {metric} is not supported.")

    # Generate the linkage matrix
    linkage_matrix = generate_linkage_matrix(
        distance_matrix=distance_matrix,
        linkage_method=linkage_method,
        distance_threshold=0.0
    )

    # Plot the dendrogram
    plot_dendrogram(
        linkage_matrix=linkage_matrix,
        threshold=threshold,
        labels=df.columns[1:],  # Exclude the first column (assumed to contain sample identifiers)
        name=name,
        linkage_method=linkage_method,
        metric=metric
    )
