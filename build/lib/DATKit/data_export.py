import pandas as pd

from DATKit.distance_computing import generate_distance_matrix


def export_matrix(matrix, names, filename="matrix.csv"):
    """
    Exports the matrix to a CSV file with proper formatting.

    Parameters
    ----------
    matrix : ndarray
        The matrix (2D numpy array).
    names : list of str
        The labels for rows and columns.
    filename : str, optional
        The filename for the CSV file.

    Returns
    -------
    None
        Files are saved to disk.
    """
    # Convert matrix to DataFrame with labeled rows and columns
    df = pd.DataFrame(matrix, index=names, columns=names)

    # Export to CSV, leaving the top-left cell blank (handled automatically by pandas)
    df.to_csv(filename, index=True)


def export_distance_matrix(df, metric='correlation', filename='distance_matrix.csv'):
    """
    Generates a CSV document with the distance matrix.

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
    filename : str, optional, default='distance_matrix.svg'
        The filename where the distance matrix will be saved.

    Returns
    ----------
    None
        Saves the distance matrix CSV to the specified file.

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

    export_matrix(distance_matrix, names, filename=filename)


def export_similarity_matrix(df, metric='correlation', filename='similarity_matrix.csv'):
    """
    Generates a CSV document with the similarity matrix.

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
    filename : str, optional, default='similarity_matrix.svg'
        The filename where the similarity matrix will be saved.

    Returns
    ----------
    None
        Saves the similarity matrix CSV to the specified file.

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

    export_matrix(similarity_matrix, names, filename=filename)


def export_distance_matrix_list(df_list, data_groups, metric='correlation', filename='???_distance_matrix.csv'):
    """
    Generates a CSV document with the distance matrix.

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
    filename : str, optional, default='???_distance_matrix.svg'
        The filename where the distance matrices will be saved.

    Returns
    ----------
    None
        Saves the distance matrices CSVs to the specified files.

    Raises
    ------
    ValueError
        If an unsupported metric is specified.
    """
    # Generate the distance matrix using the given metric
    try:
        for data_group, df in zip(data_groups, df_list):

            distance_matrix, names = generate_distance_matrix(df, metric)

            # Export matrix
            export_matrix(distance_matrix, names, filename=filename.replace('???', data_group))

    except ValueError:
        raise ValueError(f"Metric {metric} is not supported.")


def export_similarity_matrix_list(df_list, data_groups, metric='correlation', filename='???_similarity_matrix.csv'):
    """
    Generates a CSV document with the similarity matrix.

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
    filename : str, optional, default='???_similarity_matrix.svg'
        The filename where the similarity matrices will be saved.

    Returns
    ----------
    None
        Saves the similarity matrices CSVs to the specified files.

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

            # Export matrix
            export_matrix(similarity_matrix, names, filename=filename.replace('???', data_group))

    except ValueError:
        raise ValueError(f"Metric {metric} is not supported.")