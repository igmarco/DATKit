from DATKit.properties.process_prop_loader import config_process
from DATKit.properties.prop_parser import parse_value
from DATKit.analysis_reporting import generate_pdf_report
from DATKit.data_filtering import filter_columns_by_distance, exclude_elements, exclude_elements_except
from DATKit.data_integration import build_dataframe
from DATKit.data_loading import load_data
from DATKit.data_visualization import generate_dendrogram, generate_linechart, generate_heatmap

# CSV info
CSV_list = parse_value(config_process['CSV']['CSV_list'])
data_groups = parse_value(config_process['CSV']['data_groups'])
CSV_format_list = parse_value(config_process['CSV']['CSV_format_list'])

# kDa values info
kDa_range = parse_value(config_process['KDA']['kDa_range'])
kDa_range_start = parse_value(config_process['KDA']['kDa_range_start'])
kDa_range_end = parse_value(config_process['KDA']['kDa_range_end'])
interp_function = parse_value(config_process['KDA']['interp_function'])
extrap_function = parse_value(config_process['KDA']['extrap_function'])

# Filtering by inclusion elements info
filter_inclusion = parse_value(config_process['INCLUSION']['filter_inclusion'])
inclusion_elements = parse_value(config_process['INCLUSION']['inclusion_elements'])

# Filtering by exclusion elements info
filter_exclusion = parse_value(config_process['EXCLUSION']['filter_exclusion'])
exclusion_elements = parse_value(config_process['EXCLUSION']['exclusion_elements'])

# Filtering by distance info
filter_distance = parse_value(config_process['DISTANCEFILTER']['filter_distance'])
filter_distance_element = parse_value(config_process['DISTANCEFILTER']['filter_distance_element'])
filter_distance_threshold = parse_value(config_process['DISTANCEFILTER']['filter_distance_threshold'])
filter_distance_metric = parse_value(config_process['DISTANCEFILTER']['filter_distance_metric'])

# Line chart info
linechart_filename = parse_value(config_process['LINECHART']['linechart_filename'])

# Heatmap info
heatmap_filename = parse_value(config_process['HEATMAP']['heatmap_filename'])
heatmap_metric = parse_value(config_process['HEATMAP']['heatmap_metric'])

# Dendrogram info
dendrogram_filename = parse_value(config_process['DENDROGRAM']['dendrogram_filename'])
dendrogram_linkage_method = parse_value(config_process['DENDROGRAM']['dendrogram_linkage_method'])
dendrogram_metric = parse_value(config_process['DENDROGRAM']['dendrogram_metric'])
dendrogram_threshold = parse_value(config_process['DENDROGRAM']['dendrogram_threshold'])

# Report info
report = parse_value(config_process['REPORT']['report'])
report_filename = parse_value(config_process['REPORT']['report_filename'])

df_list = load_data(CSV_list, CSV_format_list)

new_df = build_dataframe(df_list, data_groups,
                         kDa_range=kDa_range,
                         kDa_range_start=kDa_range_start,
                         kDa_range_end=kDa_range_end,
                         interp_function=interp_function,
                         extrap_function=extrap_function)

filtered_df, filtered_names = new_df, new_df.columns[1:].to_list()

if filter_inclusion:
    filtered_df, filtered_names = exclude_elements_except(filtered_df,
                                                          inclusion_elements)
if filter_exclusion:
    filtered_df, filtered_names = exclude_elements(filtered_df,
                                                   exclusion_elements)
if filter_distance:
    filtered_df, filtered_names = filter_columns_by_distance(filtered_df,
                                                             filter_distance_element,
                                                             threshold=filter_distance_threshold,
                                                             metric=filter_distance_metric)

generate_linechart(filtered_df,
                   name=linechart_filename)

generate_heatmap(filtered_df,
                 metric=heatmap_metric,
                 name=heatmap_filename)

generate_dendrogram(filtered_df,
                    linkage_method=dendrogram_linkage_method,
                    metric=dendrogram_metric,
                    threshold=dendrogram_threshold,
                    name=dendrogram_filename)

if report:
    generate_pdf_report(
        report_filename,
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
        filtered_names,
        linechart_path=linechart_filename,
        heatmap_path=heatmap_filename,
        dendrogram_path=dendrogram_filename
    )
