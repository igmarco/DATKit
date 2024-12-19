from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak

from DATKit.utils.image_utils import convert_svg_to_png

# import os


def generate_pdf_report(
        filename,
        CSV_list,
        data_groups,
        kDa_range,
        interp_function,
        filter_inclusion,
        inclusion_elements,
        filter_exclusion,
        exclusion_elements,
        filter_distance,
        filter_distance_element,
        filter_distance_threshold,
        filter_distance_metric,
        heatmap_metric,
        dendrogram_linkage_method,
        dendrogram_metric,
        dendrogram_threshold,
        selected_items,
        linechart_path="linechart.svg",
        heatmap_path="heatmap.svg",
        dendrogram_path="dendrogram.svg",
):
    """
    Generates a PDF report for TAU Data Analysis.

    Parameters
    ----------
    filename : str
        Name of the output PDF file.
    CSV_list : list of str
        List of CSV files used in the analysis.
    data_groups : list of str
        Names of the data groups analyzed.
    kDa_range : tuple of (float, float)
        Range of kDa values used in the analysis.
    interp_function : str
        Name of the interpolation function used.
    filter_inclusion : bool
        Whether an exclusion filter was applied.
    inclusion_elements : list
        Elements considered (filtering all others).
    filter_exclusion : bool
        Whether an inclusion filter was applied.
    exclusion_elements : list
        Elements excluded.
    filter_distance : bool
        Whether a distance filter was applied.
    filter_distance_element : str
        Element used as a reference for filtering.
    filter_distance_threshold : float
        Maximum distance threshold for filtering.
    filter_distance_metric : str
        Metric used for distance calculations in filtering.
    heatmap_metric: str
        Metric used for distance calculations for the heatmap chart.
    dendrogram_linkage_method: str
        Method used for linkage calculations for the dendrogram chart.
    dendrogram_metric: str
        Metric used for distance calculations for the dendrogram chart.
    dendrogram_threshold: str
        Threshold used for the dendrogram chart.
    selected_items : list of str
        List of selected items from the analysis.
    linechart_path : str
        Path to the SVG file of the line chart.
    heatmap_path : str
        Path to the SVG file of the heatmap.
    dendrogram_path : str
        Path to the SVG file of the dendrogram.

    Returns
    -------
    None
        Generates and saves the PDF report to the specified filename.

    Raises
    ------
    IOError
        If any of the provided image paths cannot be found or read.
    """
    # Create a PDF document with a title
    # report_path = os.path.join(os.path.dirname(__file__), filename)
    # doc = SimpleDocTemplate(report_path, pagesize=letter)
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Title and Subtitle
    title = Paragraph("TAU Data Analysis Report", styles["Title"])
    subtitle = Paragraph("",
                         # """ This report aims to obtain an analysis from collected data in the context of the
                         # project...<br/> ...<br/> ... """,
                         styles["Normal"]
                         )
    elements.extend([title, Spacer(1, 12), subtitle, Spacer(1, 24)])

    # CSV and kDa Info Section
    elements.append(Paragraph("Reporting info", styles['Heading2']))

    CSV_info = """
    <b>CSV info</b><br/>
    CSV_list                  = {0}<br/>
    data_groups               = {1}<br/><br/>
    <b>kDa values info</b><br/>
    kDa_range                 = {2}<br/>
    interp_function           = {3}<br/><br/>
    <b>Filtering info</b><br/>
    filter_inclusion          = {4}<br/>
    inclusion_elements        = {5}<br/>
    filter_exclusion          = {6}<br/>
    exclusion_elements        = {7}<br/>
    filter_distance           = {8}<br/>
    filter_distance_element   = {9}<br/>
    filter_distance_threshold = {10}<br/>
    filter_distance_metric    = {11}<br/><br/>
    <b>Charts info</b><br/>
    heatmap_metric            = {12}<br/>
    dendrogram_linkage_method = {13}<br/>
    dendrogram_metric         = {14}<br/>
    dendrogram_threshold      = {15}
    """

    # Replace placeholders with actual values
    CSV_info = CSV_info.format(
        CSV_list,
        data_groups,
        kDa_range,
        interp_function,
        filter_inclusion,
        inclusion_elements,
        filter_exclusion,
        exclusion_elements,
        filter_distance,
        filter_distance_element,
        filter_distance_threshold,
        filter_distance_metric,
        heatmap_metric,
        dendrogram_linkage_method,
        dendrogram_metric,
        dendrogram_threshold)
    elements.append(Paragraph(CSV_info.replace("\n", "<br/>"), styles["Normal"]))
    elements.append(Spacer(1, 24))

    # Selected items section
    elements.append(Paragraph("Selected Items", styles['Heading2']))
    selected_items_text = ", ".join(selected_items) if selected_items else "No items selected."
    elements.append(Paragraph(selected_items_text, styles['BodyText']))
    elements.append(Spacer(1, 24))

    # Add a page break before the Line Chart section
    elements.append(PageBreak())

    # Charts Section
    elements.append(Paragraph("Charts", styles["Heading2"]))

    # Line Chart Subsection
    elements.append(Paragraph("Line Chart", styles["Heading3"]))
    try:
        # Convert SVG image to PNG
        if linechart_path.endswith(".svg"):
            # linechart_path = os.path.join(os.path.dirname(__file__), linechart_path)
            linechart_path = convert_svg_to_png(linechart_path)

        # Create an Image object with width 450, preserving aspect ratio
        line_chart = Image(linechart_path, width=450)
        line_chart.drawHeight = line_chart.drawWidth * line_chart.imageHeight / line_chart.imageWidth
        elements.append(line_chart)
    except IOError:
        elements.append(Paragraph("Error: Could not load Line Chart image.", styles["Normal"]))
    elements.append(Spacer(1, 24))

    # Add a page break between chart subsections
    elements.append(PageBreak())

    # Heatmap Subsection
    elements.append(Paragraph("Heatmap", styles["Heading3"]))
    try:
        # Convert SVG image to PNG
        if heatmap_path.endswith(".svg"):
            # heatmap_path = os.path.join(os.path.dirname(__file__), heatmap_path)
            heatmap_path = convert_svg_to_png(heatmap_path)
        # Create an Image object with width 450, preserving aspect ratio
        heatmap = Image(heatmap_path, width=450)
        heatmap.drawHeight = heatmap.drawWidth * heatmap.imageHeight / heatmap.imageWidth
        elements.append(heatmap)
    except IOError:
        elements.append(Paragraph("Error: Could not load Heatmap image.", styles["Normal"]))
    elements.append(Spacer(1, 24))

    # Add a page break between chart subsections
    elements.append(PageBreak())

    # Dendrogram Subsection
    elements.append(Paragraph("Dendrogram", styles["Heading3"]))
    try:
        # Convert SVG image to PNG
        if dendrogram_path.endswith(".svg"):
            # dendrogram_path = os.path.join(os.path.dirname(__file__), dendrogram_path)
            dendrogram_path = convert_svg_to_png(dendrogram_path)
        # Create an Image object with width 450, preserving aspect ratio
        dendrogram = Image(dendrogram_path, width=450)
        dendrogram.drawHeight = dendrogram.drawWidth * dendrogram.imageHeight / dendrogram.imageWidth
        elements.append(dendrogram)
    except IOError:
        elements.append(Paragraph("Error: Could not load Dendrogram image.", styles["Normal"]))

    # Build the PDF
    doc.build(elements)
