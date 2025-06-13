from scipy.spatial.distance import correlation, cosine, jaccard, euclidean, minkowski, hamming
from sklearn.cluster import AgglomerativeClustering

from DATKit.utils.metric_utils import datkit_pearsonr, datkit_spearmanr, datkit_sliding_window_similarity_mean, datkit_sliding_window_similarity_derivative_weighted_distance, datkit_wasserstein
from DATKit.data_integration import generate_spectra

import numpy as np


def compute_distance(vector1, vector2, metric='correlation', **kwargs):
    """
    Compute the distance between two spectra vectors using various distance metrics.

    Parameters
    ----------
    vector1 : np.ndarray
    vector2 : np.ndarray
        Must have the same size as vector1.
    metric : str
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
        Additional arguments for specific metrics (e.g., `p` for Minkowski distance).

    Returns
    -------
    float
        The distance between vector1 and vector2 using the given metric.

    Raises
    ------
    ValueError
        If vector1 and vector2 have different sizes or if an unsupported metric is specified.
    """
    # Validate input vector sizes
    if len(vector1) != len(vector2):
        raise ValueError("Vectors must have the same size to compute distance.")

    # Define supported metrics and map them to functions
    metric_functions = {
        'correlation': correlation,
        'cosine': cosine,
        'euclidean': euclidean,
        'jaccard': jaccard,
        'hamming': hamming,
        'minkowski': lambda v1, v2: minkowski(v1, v2, kwargs.get('p', 2)),  # Default p=2
        'pearson': datkit_pearsonr,
        'spearman': datkit_spearmanr,
        'sws cosine': lambda v1, v2: datkit_sliding_window_similarity_mean(v1, v2, 30, 1, cosine),
        'sws pearson': lambda v1, v2: datkit_sliding_window_similarity_mean(v1, v2, 30, 1, datkit_pearsonr),
        'sws spearman': lambda v1, v2: datkit_sliding_window_similarity_mean(v1, v2, 30, 1, datkit_spearmanr),
        'sws cosine derivative mean': lambda v1, v2: datkit_sliding_window_similarity_derivative_weighted_distance(v1, v2, 30, 1, cosine, 'mean'),
        'sws pearson derivative mean': lambda v1, v2: datkit_sliding_window_similarity_derivative_weighted_distance(v1, v2, 30, 1, datkit_pearsonr, 'mean'),
        'sws spearman derivative mean': lambda v1, v2: datkit_sliding_window_similarity_derivative_weighted_distance(v1, v2, 30, 1, datkit_spearmanr, 'mean'),
        'sws cosine derivative geometric': lambda v1, v2: datkit_sliding_window_similarity_derivative_weighted_distance(v1, v2, 30, 1, cosine, 'geometric'),
        'sws pearson derivative geometric': lambda v1, v2: datkit_sliding_window_similarity_derivative_weighted_distance(v1, v2, 30, 1, datkit_pearsonr, 'geometric'),
        'sws spearman derivative geometric': lambda v1, v2: datkit_sliding_window_similarity_derivative_weighted_distance(v1, v2, 30, 1, datkit_spearmanr, 'geometric'),
        'wasserstein': datkit_wasserstein,
    }

    # Check if the metric is valid
    if metric not in metric_functions:
        raise ValueError(f"Unsupported metric '{metric}'. Supported metrics are: {list(metric_functions.keys())}")

    # Compute and return the distance
    return metric_functions[metric](vector1, vector2)


def generate_distance_matrix(df, metric='correlation', **kwargs):
    """
    Generates the distance matrix of a dataframe using a specified distance metric.

    Parameters
    ----------
    df : pandas.DataFrame
        A DataFrame where each column (except the first) corresponds to a sample,
        and rows contain the measured spectra values.
    metric : str
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
        Additional arguments passed to `compute_distance` (e.g., `p` for Minkowski distance).

    Returns
    -------
    matrix : numpy.ndarray
        A symmetric matrix where entry (i, j) represents the distance between sample i and sample j.
    names : list
        List of sample names corresponding to the columns in the input DataFrame (excluding the first column).

    Raises
    ------
    ValueError
        If an unsupported metric is specified.
    """
    # Extract spectra and sample names from the DataFrame
    spectra, names = generate_spectra(df)
    n_samples = len(names)

    # Initialize an empty distance matrix
    matrix = np.zeros((n_samples, n_samples), dtype='float64')

    # Compute pairwise distances for the upper triangle of the matrix
    for i in range(n_samples):
        for j in range(i + 1, n_samples):
            try:
                distance = compute_distance(spectra[i], spectra[j], metric=metric, **kwargs)
                matrix[i, j] = distance
                matrix[j, i] = distance  # Symmetric assignment
            except ValueError as e:
                raise ValueError(f"Error computing distance for samples {names[i]} and {names[j]}: {e}")

    return matrix, names


def generate_linkage_matrix(distance_matrix, linkage_method='average', distance_threshold=0.0):
    """
    Generates the linkage matrix from a precomputed distance matrix using hierarchical clustering.

    Parameters
    ----------
    distance_matrix : ndarray
        A precomputed distance matrix (n_samples x n_samples).
    linkage_method : string
        The linkage method for building the dendrogram: 'ward', 'complete', 'average', 'single'.
    distance_threshold : float
        The threshold for stopping the clustering process.

    Returns
    ----------
    linkage_matrix : ndarray
        A linkage matrix that can be used to generate the dendrogram.
    """
    # Compute the linkage method
    clustering = AgglomerativeClustering(
        n_clusters=None,
        metric='precomputed',
        linkage=linkage_method,
        distance_threshold=distance_threshold
    )
    clustering.fit(distance_matrix)

    # Build the linkage matrix
    linkage_matrix = np.column_stack([
        clustering.children_,
        clustering.distances_,
        np.arange(2, 2 + len(clustering.children_))
    ]).astype('float64')

    return linkage_matrix
