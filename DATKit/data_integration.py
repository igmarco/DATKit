from scipy.interpolate import interp1d, CubicSpline

from scipy.spatial.distance import correlation, cosine, jaccard, euclidean, minkowski, hamming
from scipy.stats import pearsonr, spearmanr

import numpy as np
import pandas as pd

from DATKit.utils.interpolation_utils import zeros, nearest


def build_dataframe(df_list, df_names, interp_function='interp1d', extrap_function='nearest',
                    kDa_range='auto', kDa_range_start=2.0, kDa_range_end=40.0, step=0.1, **interp_kwargs):
    """
    Construct a DataFrame with homogeneous interpolated data from multiple DataFrames.

    Parameters
    ----------
    df_list : list
        List of DataFrames, each containing a 'kDa' column and multiple value columns.
    df_names : list
        List of names to identify each DataFrame.
    interp_function : string, optional
        Interpolation function: 'interp1d', 'CubicSpline' (default is 'interp1d').
    extrap_function : string, optional
        Extrapolation function: 'zeros', 'nearest', 'interp1d', 'CubicSpline' (default is 'nearest').
    kDa_range : str
        Interpolation range: 'auto', 'manual' (default is 'auto').
    kDa_range_start : float, optional
        If kDa_range='manual': Start of the interpolation range (default is 2.0).
    kDa_range_end : float, optional
        If kDa_range='manual': End of the interpolation range (default is 40.0).
    step : float, optional
        Step size between points in the interpolated range (default is 0.01).
    interp_kwargs : dict, optional
        Additional arguments to pass to the interpolation function.

    Returns
    ----------
    DataFrame
        A DataFrame with the interpolated data.
    """
    # Definir kDa_range_start y kDa_range_end
    if kDa_range == 'auto':
        kDa_range_start = np.max([df['kDa'].min() for df in df_list])
        kDa_range_end = np.min([df['kDa'].max() for df in df_list])

    # Crear el rango homogéneo de puntos para todas las muestras
    interpolation_points = np.arange(kDa_range_start, kDa_range_end, step)

    # Inicializar listas para las muestras y los nombres
    interpolated_samples = [interpolation_points]
    sample_names = ['points']

    # Procesar cada DataFrame
    for df, name in zip(df_list, df_names):
        columns = df.columns[1:]  # Excluir la columna 'kDa'

        for column in columns:
            # Crear función de interpolación para la columna
            interp_func = globals()[interp_function](df['kDa'], df[column], **interp_kwargs)

            # Crear máscara para valores dentro y fuera del rango
            in_range_mask = (interpolation_points >= df['kDa'].min()) & (interpolation_points <= df['kDa'].max())
            out_of_range_mask = ~in_range_mask

            # Inicializar un array para los valores interpolados y extrapolados
            interpolated_values = np.empty_like(interpolation_points, dtype=float)

            # Aplicar interpolación solo en puntos dentro del rango
            interpolated_values[in_range_mask] = interp_func(interpolation_points[in_range_mask])

            # Crear función de extrapolación usando la función especificada
            extrap_func = globals()[extrap_function](df['kDa'], df[column], **interp_kwargs)

            # Aplicar extrapolación fuera del rango
            interpolated_values[out_of_range_mask] = extrap_func(interpolation_points[out_of_range_mask])

            # Guardar los resultados
            interpolated_samples.append(interpolated_values)

            # Escoger el nombre para la columna
            if name == "":
                sample_names.append(f"{column}")
            else:
                sample_names.append(f"{name}_{column}")

    # Crear el DataFrame final
    return pd.DataFrame(
        data=np.transpose(interpolated_samples),
        columns=sample_names
    )


def generate_spectra(df):
    """
    Generate spectra matrix from dataframe

    Parameters
    ----------
    df : dataframe
         A dataframe where the first row contains the names of the samples and for each sample we have its spectra

    Returns
    ----------
    matrix : narray
             The spectra associated with each sample
    names  : list
             The list of names of the samples
    """

    names = df.columns[1:]

    return np.transpose(df.values[:, 1:]), names
