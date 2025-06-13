from DATKit.distance_computing import generate_distance_matrix


def exclude_elements(df, element_names=None):
    """
    Excludes the specified elements (columns) from the DataFrame, retaining the 'points' column.

    Parameters
    ----------
    df : pandas.DataFrame
        A DataFrame where each column corresponds to a sample.
    element_names : list
        A list of column names to exclude from the DataFrame.

    Returns
    -------
    filtered_df : pandas.DataFrame
        A new DataFrame without the excluded columns (but retaining 'points').
    filtered_names : list
        The list of remaining column names in the filtered DataFrame (excluding 'points').
    """
    if element_names is None:
        element_names = []
    filtered_names = [col for col in df.columns if col not in element_names and col != 'points']
    filtered_columns = ['points'] + filtered_names

    filtered_df = df[filtered_columns]

    return filtered_df, filtered_names


def exclude_elements_except(df, element_names=None):
    """
    Keeps only the specified elements (columns) in the DataFrame, retaining the 'points' column.

    Parameters
    ----------
    df : pandas.DataFrame
        A DataFrame where each column corresponds to a sample.
    element_names : list
        A list of column names to keep in the DataFrame.

    Returns
    -------
    filtered_df : pandas.DataFrame
        A new DataFrame with only the specified columns and 'points'.
    filtered_names : list
        The list of column names retained in the filtered DataFrame (excluding 'points').
    """
    if element_names is None:
        element_names = []
    filtered_names = [col for col in df.columns if col in element_names]
    filtered_columns = ['points'] + filtered_names

    filtered_df = df[filtered_columns]

    return filtered_df, filtered_names


def filter_elements_by_distance(distance_matrix, names, element_name, threshold=0.1):
    """
    Filters elements based on their distance to a given element, only keeping those with
    distance <= threshold.

    Parameters
    ----------
    distance_matrix : numpy.ndarray
        A 2D array containing pairwise distances between elements.
    names : pd.Series
        A list of element names corresponding to the rows and columns of the distance matrix.
    element_name : str
        The name of the element to compare against.
    threshold : float
        The distance threshold. Only elements with distance <= threshold to the given element will be returned.

    Returns
    -------
    filtered_names : list
        A list of names of elements that have distance <= threshold to the given element.
    """
    if element_name not in names:
        raise ValueError(f"The element '{element_name}' is not found in the names list.")

    # Get the index of the element in the names list
    element_idx = names.get_loc(element_name)

    filtered_names = []

    # Compare distances to the specified element
    for i in range(len(names)):
        if i != element_idx:  # Exclude the element itself
            if distance_matrix[element_idx, i] <= threshold:
                filtered_names.append(names[i])

    return filtered_names


def filter_columns_by_distance(df, element_name, threshold=0.1, metric='correlation', **kwargs):
    """
    Filters columns of the DataFrame based on their distance to a given reference column.
    Only columns with distance <= threshold from the reference element will be kept.

    Parameters
    ----------
    df : pandas.DataFrame
        A DataFrame where each column (except the first) corresponds to a sample.
    element_name : str
        The name of the reference element (column) to compare against.
    threshold : float
        The distance threshold. Only columns with distance <= threshold to the given element will be returned.
    metric : str
        The metric to use for computing the distance. Supported metrics are:
        - 'correlation': Correlation distance.
        - 'cosine': Cosine distance.
        - 'euclidean': Euclidean distance.
        - 'jaccard': Jaccard distance.
        - 'hamming': Hamming distance.
        - 'minkowski': Minkowski distance (requires parameter 'p' in kwargs).
        - 'pearson': Pearson correlation distance, defined as 1 - absolute Pearson correlation.
        - 'spearman': Spearman correlation distance, defined as 1 - absolute Spearman correlation.
        - 'sws cosine': Mean cosine similarity computed over sliding windows of fixed size.
        - 'sws pearson': Mean Pearson correlation similarity computed over sliding windows.
        - 'sws spearman': Mean Spearman correlation similarity computed over sliding windows.
        - 'sws cosine derivative mean': Weighted mean cosine similarity over sliding windows, where weights derive from the mean absolute derivatives of the signals.
        - 'sws pearson derivative mean': Weighted mean Pearson similarity with derivative weights.
        - 'sws spearman derivative mean': Weighted mean Spearman similarity with derivative weights.
        - 'sws cosine derivative geometric': Weighted mean cosine similarity with geometric mean weighting of derivatives.
        - 'sws pearson derivative geometric': Weighted mean Pearson similarity with geometric mean weighting.
        - 'sws spearman derivative geometric': Weighted mean Spearman similarity with geometric mean weighting.
        - 'wasserstein': Wasserstein (Earth Mover's) distance between peaks detected in both signals.
    **kwargs : dict
        Additional arguments passed to `generate_distance_matrix`.

    Returns
    -------
    filtered_df : pandas.DataFrame
        A new DataFrame containing only the columns that have distance <= threshold to the given reference column.
    """
    # Generate the distance matrix and get the column names
    distance_matrix, names = generate_distance_matrix(df, metric=metric, **kwargs)

    # Filter names by distance using the filter_elements_by_distance function
    filtered_names = filter_elements_by_distance(distance_matrix, names, element_name, threshold)

    # Ensure that the reference element is included in the filtered names list
    if element_name not in filtered_names:
        filtered_names.append(element_name)

    # Use exclude_elements_except to filter the DataFrame
    filtered_df, final_filtered_names = exclude_elements_except(df, filtered_names)

    return filtered_df, filtered_names
