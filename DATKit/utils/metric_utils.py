import numpy as np

from scipy.signal import find_peaks
from scipy.stats import pearsonr, spearmanr, wasserstein_distance

def datkit_pearsonr(v1, v2):
    """
    Computes a distance based on Pearson correlation.

    Parameters
    ----------
    v1, v2 : array-like
        Input time series.

    Returns
    -------
    float
        Distance metric defined as 1 - abs(Pearson correlation).
    """
    return 1 - abs(pearsonr(v1, v2)[0])

def datkit_spearmanr(v1, v2):
    """
    Computes a distance based on Spearman correlation.

    Parameters
    ----------
    v1, v2 : array-like
        Input time series.

    Returns
    -------
    float
        Distance metric defined as 1 - abs(Spearman correlation).
    """
    return 1 - abs(spearmanr(v1, v2)[0])

def sliding_window_similarity(v1, v2, window_size, step_size, metric = spearmanr, t = None):
    """
    Computes local similarity between two signals using a sliding window.

    Parameters
    ----------
    v1, v2 : array-like
        Input time series.
    t : array-like
        Time axis corresponding to the signals.
    window_size : int
        Size of the sliding window (number of samples).
    step_size : int
        Step size for moving the window.
    metric : callable
        Similarity function returning a correlation and a p-value (e.g., spearmanr, pearsonr).

    Returns
    -------
    positions : ndarray
        Central time points for each window.
    similarities : ndarray
        Similarity values computed for each window.
    """
    if t is None:
        t = np.arange(len(v1))

    similarities = []
    positions = []

    for start in range(0, len(v1) - window_size + 1, step_size):
        end = start + window_size
        segment1 = v1[start:end]
        segment2 = v2[start:end]
        corr = metric(segment1, segment2)
        similarities.append(corr)
        positions.append(t[start + window_size // 2])

    return np.array(positions), np.array(similarities)

def datkit_sliding_window_similarity_mean(v1, v2, window_size, step_size, metric, t = None):
    """
    Computes the mean of sliding window similarities.

    Parameters
    ----------
    v1, v2 : array-like
        Input time series.
    t : array-like
        Time axis.
    window_size : int
        Size of the window.
    step_size : int
        Step between windows.
    metric : callable
        Similarity function.

    Returns
    -------
    float
        Mean similarity value. (Missing in current implementation)
    """
    return np.mean(sliding_window_similarity(v1, v2, window_size, step_size, metric, t)[1])

def weighted_similarity_from_two_derivatives(positions, similarities, v1, v2, window_size, method='mean', t = None):
    """
    Computes a weighted similarity score using the absolute first derivative of two signals.

    Parameters
    ----------
    positions : array-like
        Time points corresponding to the center of each similarity window.
    similarities : array-like
        Similarity values for each window.
    v1, v2 : array-like
        Input time series.
    t : array-like
        Time axis.
    window_size : int
        Size of the window to use around each position for computing derivatives.
    method : str
        Weighting method: 'mean', 'product', 'geometric', 'min', or 'max'.

    Returns
    -------
    weights : ndarray
        Weight values computed from signal derivatives.
    weighted_mean : float
        Weighted mean of similarity values using the computed weights.
    """
    if t is None:
        t = np.arange(len(v1))

    dt = t[1] - t[0]
    d1 = np.abs(np.gradient(v1, dt))
    d2 = np.abs(np.gradient(v2, dt))
    weights = []
    half_w = window_size // 2

    for center in positions:
        idx_center = np.argmin(np.abs(t - center))
        start = max(0, idx_center - half_w)
        end = min(len(t), idx_center + half_w + 1)

        seg1 = d1[start:end]
        seg2 = d2[start:end]

        if method == 'mean':
            w = np.mean((seg1 + seg2) / 2)
        elif method == 'product':
            w = np.mean(seg1 * seg2)
        elif method == 'geometric':
            w = np.mean(np.sqrt(seg1 * seg2))
        elif method == 'min':
            w = np.mean(np.minimum(seg1, seg2))
        elif method == 'max':
            w = np.mean(np.maximum(seg1, seg2))
        else:
            raise ValueError(f"Unknown method: {method}")

        weights.append(w)

    weights = np.array(weights)
    weighted_mean = np.sum(weights * similarities) / np.sum(weights)

    return weights, weighted_mean

def datkit_sliding_window_similarity_derivative_weighted_distance(v1, v2, window_size, step_size, metric, method='mean', t = None):
    """
    Computes a weighted similarity between two signals, where the weights are
    derived from the magnitude of their first derivatives.

    Parameters
    ----------
    v1, v2 : array-like
        Input time series.
    t : array-like
        Time axis.
    window_size : int
        Sliding window size.
    step_size : int
        Step size for sliding the window.
    metric : callable
        Correlation function (e.g., spearmanr, pearsonr).
    method : str
        Weight computation method: 'mean', 'product', 'geometric', 'min', or 'max'.

    Returns
    -------
    float
        Weighted similarity score.
    """
    positions, similarities = sliding_window_similarity(v1, v2, window_size, step_size, metric, t)
    weights, w_mean = weighted_similarity_from_two_derivatives(positions, similarities, v1, v2, window_size, method, t)
    return w_mean

def datkit_wasserstein(v1, v2, height=0.1, distance=10, prominence=1):
    """
    Computes the Wasserstein (Earth Mover's) distance between the peaks of two signals.

    Parameters
    ----------
    v1, v2 : array-like
        Input signals.
    height : float
        Minimum height of peaks to detect.
    distance : int
        Minimum horizontal distance between neighboring peaks.
    prominence : float
        Required prominence of peaks.

    Returns
    -------
    float
        Wasserstein distance between the positions of detected peaks in v1 and v2.
    """
    v1_peaks, _ = find_peaks(v1, height=height, distance=distance, prominence=prominence)
    v2_peaks, _ = find_peaks(v2, height=height, distance=distance, prominence=prominence)

    return float(wasserstein_distance(v1_peaks, v2_peaks))