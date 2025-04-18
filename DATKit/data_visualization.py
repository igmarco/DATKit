from DATKit.tools.chart_tools import plot_linechart, plot_heatmap, plot_dendrogram
from DATKit.data_integration import generate_spectra
from DATKit.distance_computing import generate_distance_matrix, generate_linkage_matrix


def generate_linechart(df, filename='linechart.svg'):
    """
    Generates a linechart based on the interpolated data from the given DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame
        A DataFrame where each row corresponds to a sample and columns contain features.
    filename : str, optional, default='linechart.svg'
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
    plot_linechart(spectra, x, names, filename=filename)


def generate_heatmap(df, metric='correlation', filename='heatmap.svg', decimals=1):
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
    filename : str, optional, default='heatmap.svg'
        The filename where the heatmap image will be saved.
    decimals: int, optional
        The number of decimals to be displayed.

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
        distance_matrix, names = generate_distance_matrix(df, metric)
    except ValueError:
        raise ValueError(f"Metric {metric} is not supported.")

    # Create the similarity matrix
    similarity_matrix = 1 - distance_matrix

    # Plot the heatmap
    plot_heatmap(similarity_matrix, names, metric=metric, filename=filename, decimals=decimals)


def generate_dendrogram(df, linkage_method='average', metric='correlation', threshold=0, filename='dendrogram.svg'):
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
    filename : str, optional, default='dendrogram.svg'
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
        filename=filename,
        linkage_method=linkage_method,
        metric=metric
    )


def generate_linechart_list(df_list, data_groups, filename='???_linechart.svg'):
    """
    Generates linecharts based on the interpolated data from the given list of DataFrames.

    Parameters
    ----------
    df_list : list of pandas.DataFrame
        A list of DataFrames where each row corresponds to a sample and columns contain features.
    data_groups : list of str
        A list of names for each DataFrame in df_list.
    filename : str, optional, default='???_linechart.svg'
        The filename where each linechart image will be saved. '???' is replced with the name in data_groups for each element.

    Returns
    ----------
    None
        Saves the linechart images to the specified files.
    """
    for data_group, df in zip(data_groups, df_list):

      # Obtain the spectra
      spectra, names = generate_spectra(df)
      x = df['points'].values

      # Plot the linechart
      plot_linechart(spectra, x, names, filename=filename.replace('???', data_group), title=data_group+' Interpolated Data Plot')

      print()


def generate_heatmap_list(df_list, data_groups, metric='correlation', filename='???_heatmap.svg', decimals=1):
    """
    Generates heatmaps based on the distance matrix computed from the given list of DataFrames.

    Parameters
    ----------
    df_list : list of pandas.DataFrame
        A list of DataFrames where each row corresponds to a sample and columns contain features.
    data_groups : list of str
        A list of names for each DataFrame in df_list.
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
    filename : str, optional, default='???_heatmap.svg'
        The filename where each heatmap image will be saved. '???' is replced with the name in data_groups for each element.
    decimals: int, optional
        The number of decimals to be displayed.

    Returns
    ----------
    None
        Saves the heatmap images to the specified files.

    Raises
    ------
    ValueError
        If an unsupported metric is specified.
    """
    # Generate the distance matrix using the given metric
    try:
        for data_group, df in zip(data_groups, df_list):

            distance_matrix, names = generate_distance_matrix(df, metric)

            # Create the similarity matrix
            similarity_matrix = 1 - distance_matrix

            # Plot the heatmap
            plot_heatmap(similarity_matrix, names, metric=metric, filename=filename.replace('???', data_group), title=data_group+' Heatmap', decimals=decimals)

            print()

    except ValueError:
        raise ValueError(f"Metric {metric} is not supported.")


def generate_dendrogram_list(df_list, data_groups, linkage_method='average', metric='correlation', threshold=0, filename='???_dendrogram.svg'):
    """
    Generates dendrograms based on hierarchical clustering for a list of DataFrames.

    Parameters
    ----------
    df_list : list of pandas.DataFrame
        A list of DataFrames where each row corresponds to a sample and columns contain features.
    data_groups : list of str
        A list of names for each DataFrame in df_list.
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
    filename : str, optional, default='???_dendrogram.svg'
        The filename where each dendrogram image will be saved. '???' is replced with the name in data_groups for each element.

    Returns
    ----------
    None
        Saves the dendrogram images to the specified files.

    Raises
    ------
    ValueError
        If an unsupported metric is specified.
    """

    try:
        for data_group, df in zip(data_groups, df_list):
            # Compute the distance matrix and sample names
            distance_matrix, names = generate_distance_matrix(df, metric)

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
                filename=filename.replace('???', data_group),
                title=data_group+' Dendrogram',
                linkage_method=linkage_method,
                metric=metric
            )

            print()
    except ValueError:
        raise ValueError(f"Metric {metric} is not supported.")