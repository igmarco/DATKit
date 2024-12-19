import matplotlib.pyplot as plt
from seaborn import heatmap
from scipy.cluster.hierarchy import dendrogram
import os


def plot_linechart(spectra, x, element_names, name='linechart.svg', x_label='kDa', **kwargs):
    """
    Plots the interpolated data from the given DataFrame.

    Parameters
    ----------
    spectra : np.ndarray
        The spectra matrix containing the interpolated data.
    x : np.ndarray
        The domain vector to use as the x-axis.
    element_names : list
        List of element names.
    name : str, optional
        The filename where the plot will be saved (default is 'plot.png').
    x_label : str, optional
        The label for the domain (default is 'kDa').
    kwargs : dict, optional
        Additional keyword arguments to pass to plt.plot (e.g., line styles or colors).

    Returns
    ----------
    None
        Saves the plot as a file with the given filename and displays it.
    """
    # Prepare data for plot
    plt.figure(figsize=(10, 6))
    for i, element_name in enumerate(element_names):
        plt.plot(x, spectra[i], label=element_name, **kwargs)

    # Add the legend
    plt.legend()

    # Axis labels
    plt.xlabel(x_label)
    plt.ylabel('Values')

    # Plot title
    plt.title('Interpolated Data Plot')

    # Adjust layout to prevent cutting off elements
    plt.tight_layout()

    # Save and display the plot
    # chart_path = os.path.join(os.path.dirname(__file__), '../' + name)
    # plt.savefig(chart_path, bbox_inches='tight')  # Use bbox_inches='tight' to avoid clipping
    plt.savefig(name, bbox_inches='tight')  # Use bbox_inches='tight' to avoid clipping
    plt.show()


def plot_heatmap(similarity_matrix, names, metric="", name='heatmap.svg'):
    """
    Plots a heatmap based on the provided similarity matrix.

    Parameters
    ----------
    similarity_matrix : ndarray
        The similarity matrix (1 - distance matrix).
    names : list of str
        The sample names to use as labels for the heatmap axes.
    metric : str, optional
        The metric name to be displayed in the plot title.
    name : str, optional, default='heatmap.svg'
        The filename where the heatmap image will be saved.

    Returns
    ----------
    None
        Displays and saves the heatmap plot.
    """
    # # Clear the current figure to ensure a fresh plot
    # plt.clf()

    # Set up the figure size dynamically based on the number of samples
    plt.figure(figsize=(len(names) * 1.5 + 1, len(names) * 1.5))

    # Create the heatmap
    ax = heatmap(similarity_matrix, xticklabels=names, yticklabels=names, annot=True)

    # Rotate the x-axis and y-axis labels to make them horizontal
    plt.xticks(rotation=35)
    plt.yticks(rotation=35)

    # Define the title
    title = 'Heatmap'

    # Conditionally append information to the title if not empty
    if metric != "":
        title += f' (Metric: {metric})'

    # Set the title in the plot
    plt.title(title)

    # Label the colorbar with 'Distances'
    cbar = ax.collections[0].colorbar
    cbar.set_label('Distances')

    # Adjust layout to prevent cutting off elements
    plt.tight_layout()

    # Save and display the plot
    # chart_path = os.path.join(os.path.dirname(__file__), '../' + name)
    # plt.savefig(chart_path, bbox_inches='tight')  # Use bbox_inches='tight' to avoid clipping
    plt.savefig(name, bbox_inches='tight')  # Use bbox_inches='tight' to avoid clipping
    plt.show()


def plot_dendrogram(linkage_matrix, threshold=0, labels=None, name='dendrogram.svg', linkage_method="", metric=""):
    """
    Plots a dendrogram using the provided linkage matrix.

    Parameters
    ----------
    linkage_matrix : ndarray
        A linkage matrix that contains the hierarchical clustering information.
    threshold : float
        If threshold != 0.: The threshold to color clusters and add a horizontal line in the plot.
    labels : Optional[ndarray]
        Labels for the samples, displayed on the dendrogram leaves.
    name : str
        The filename where the dendrogram image will be saved.
    linkage_method : str
        The linkage method name
    metric : str
        The metric name

    Returns
    ----------
    None
        Displays and saves the dendrogram plot.
    """
    plt.figure(figsize=(len(labels) * 1.2, len(labels) * 0.5 + 2))

    # Plot the dendrogram
    dendrogram(
        linkage_matrix,
        labels=labels,
        orientation='top',
        color_threshold=threshold,
        leaf_font_size=11,  # Reduce font size for better visibility
        leaf_rotation=35  # Rotate labels to avoid overlap
    )

    # Add a horizontal threshold line
    if threshold > 0.:
        plt.axhline(y=threshold, color='b', linestyle='dotted', label=f'Threshold: {threshold}')

    # Add axis labels and title
    plt.ylabel("Distances")

    # Define the title
    title = 'Dendrogram'

    # Conditionally append information to the title if not empty
    if metric != "" and linkage_method != "":
        title += f' (Metric: {metric} - Linkage method: {linkage_method})'
    elif metric != "":
        title += f' (Metric: {metric})'
    elif linkage_method != "":
        title += f' (Linkage method: {linkage_method})'

    # Set the title in the plot
    plt.title(title)

    # Save and display the plot
    if threshold > 0.:
        plt.legend(loc='upper right')

    # Adjust layout to prevent cutting off elements
    plt.tight_layout()

    # Save and display the plot
    # chart_path = os.path.join(os.path.dirname(__file__), '../' + name)
    # plt.savefig(chart_path, bbox_inches='tight')  # Use bbox_inches='tight' to avoid clipping
    plt.savefig(name, bbox_inches='tight')  # Use bbox_inches='tight' to avoid clipping
    plt.show()
