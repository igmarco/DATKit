import cairosvg


def convert_svg_to_png(svg_path):
    """
    Converts an SVG file to PNG using cairosvg.

    Parameters
    ----------
    svg_path : str
        Path to the SVG file.

    Returns
    -------
    png_path : str
        Path to the generated PNG file.
    """
    png_path = svg_path.replace(".svg", ".png")
    cairosvg.svg2png(url=svg_path, write_to=png_path)

    return png_path


# import pyvips
#
#
# def convert_svg_to_png(svg_path):
#     """
#     Converts an SVG file to PNG using cairosvg.
#
#     Parameters
#     ----------
#     svg_path : str
#         Path to the SVG file.
#
#     Returns
#     -------
#     png_path : str
#         Path to the generated PNG file.
#     """
#     png_path = svg_path.replace(".svg", ".png")
#
#     image = pyvips.Image.new_from_file(svg_path, dpi=300)
#     image.write_to_file(png_path)
#
#     return png_path