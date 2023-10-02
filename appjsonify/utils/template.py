import argparse

def get_template(
    paper_type: str,
    args: argparse.Namespace
) -> argparse.Namespace:
    """Return a registered pipeline template.

    Args:
        paper_type (str): A paper type.

    Raises:
        ValueError: Throws an error when `paper_type` is not registered.

    Returns:
        argparse.Namespace: Pre-defined arguments.
    """
    if paper_type == "ACL":
        args_dict: dict = {
            "input_dir_or_file_path": args.input_dir_or_file_path,
            "output_dir": args.output_dir,
            "paper_type": args.paper_type,
            "pipeline": [
                "load_docs", "load_objects_with_ml", "remove_illegal_tokens",
                "remove_meta", "extract_lines", "extract_captions_with_ml",
                "remove_figures_with_ml", "remove_tables_with_ml", "remove_equations_with_ml",
                "extract_footnotes_with_ml", "extract_footnotes", "remove_lines_by_objects",
                "extract_paragraphs", "detect_sections", "tailor_references", 
                "concat_columns", "concat_pages", "dump_formatted_doc"
            ],
            "verbose": args.verbose,
            "insert_page_break": args.insert_page_break,
            "show_pos": args.show_pos,
            "show_font": args.show_font,
            "show_style": args.show_style,
            "show_meta": args.show_meta,
            "x_tolerance": 1.2,
            "tablebank_threshold": 0.9,
            "detectron_device_mode": args.detectron_device_mode,
            "save_image": args.save_image,
            "output_image_dir":args.output_image_dir,
            "header_offset": 75,
            "footer_offset": 80,
            "left_side_offset": 40,
            "right_side_offset": 40,
            "y_tolerance": 6.0,
            "object_bbox_offset": 25,
            "equation_overlap_threshold": 0.5,
            "caption_overlap_threshold": 0.5,
            "table_start_ptn_str": r"Table [0-9]+:",
            "figure_start_ptn_str": r"Figure [0-9]+:",
            "preset_table_caption_pos": "below",
            "preset_figure_caption_pos": "below",
            "caption_assignment_threshold": 75.0,
            "footnote_overlap_threshold": 0.5,
            "footnote_offset": 200,
            "use_horizontal_lines": True,
            "remove_by_line": True,
            "remove_by_curve": True,
            "x_offset": 10,
            "y_offset": 4,
            "consider_font_size": True,
            "indent_offset": 25,
            "listing_offset": 45,
            "max_headline_len": 10,
            "headline_names": [
                "Abstract", "References", "Acknowledgement", "Acknowledgements",
                "Acknowledgment", "Acknowledgments", "Appendix", "Appendices",
                "Limitations", "Ethics Statement", "Ethics Statements"
            ],
            "column_offset": 300
        }
        return argparse.Namespace(**args_dict)
    elif paper_type == "ACL2":
        args_dict: dict = {
            "input_dir_or_file_path": args.input_dir_or_file_path,
            "output_dir": args.output_dir,
            "paper_type": args.paper_type,
            "pipeline": [
                "load_docs", "remove_illegal_tokens", "remove_meta", "extract_lines",
                "extract_footnotes", "remove_lines_by_objects", "extract_paragraphs",
                "detect_sections", "tailor_references", "concat_columns", "concat_pages", "dump_formatted_doc"
            ],
            "verbose": args.verbose,
            "insert_page_break": args.insert_page_break,
            "show_pos": args.show_pos,
            "show_font": args.show_font,
            "show_style": args.show_style,
            "show_meta": args.show_meta,
            "x_tolerance": 1.2,
            "header_offset": 75,
            "footer_offset": 80,
            "left_side_offset": 40,
            "right_side_offset": 40,
            "y_tolerance": 6.0,
            "footnote_offset": 200,
            "use_horizontal_lines": True,
            "object_bbox_offset": 25,
            "remove_by_line": True,
            "remove_by_curve": True,
            "x_offset": 10,
            "y_offset": 4,
            "consider_font_size": True,
            "indent_offset": 25,
            "listing_offset": 45,
            "max_headline_len": 10,
            "headline_names": [
                "Abstract", "References", "Acknowledgement", "Acknowledgements",
                "Acknowledgment", "Acknowledgments", "Appendix", "Appendices",
                "Limitations", "Ethics Statement", "Ethics Statements"
            ],
            "column_offset": 300
        }
        return argparse.Namespace(**args_dict)
    elif paper_type == "AAAI":
        args_dict: dict = {
            "input_dir_or_file_path": args.input_dir_or_file_path,
            "output_dir": args.output_dir,
            "paper_type": args.paper_type,
            "pipeline": [
                "load_docs", "load_objects_with_ml", "remove_illegal_tokens",
                "remove_meta", "extract_lines", "extract_captions_with_ml",
                "remove_figures_with_ml", "remove_tables_with_ml", "remove_equations_with_ml",
                "extract_footnotes_with_ml", "extract_footnotes", "remove_lines_by_objects",
                "extract_paragraphs", "detect_sections", "concat_columns", 
                "concat_pages", "dump_formatted_doc"
            ],
            "verbose": args.verbose,
            "insert_page_break": args.insert_page_break,
            "show_pos": args.show_pos,
            "show_font": args.show_font,
            "show_style": args.show_style,
            "show_meta": args.show_meta,
            "x_tolerance": 1.2,
            "tablebank_threshold": 0.9,
            "detectron_device_mode": args.detectron_device_mode,
            "save_image": args.save_image,
            "output_image_dir": args.output_image_dir,
            "header_offset": 65,
            "footer_offset": 80,
            "left_side_offset": 40,
            "right_side_offset": 40,
            "y_tolerance": 3.0,
            "object_bbox_offset": 25,
            "equation_overlap_threshold": 0.5,
            "caption_overlap_threshold": 0.5,
            "table_start_ptn_str": r"Table [0-9]+:",
            "figure_start_ptn_str": r"Figure [0-9]+:",
            "preset_table_caption_pos": "below",
            "preset_figure_caption_pos": "below",
            "caption_assignment_threshold": 75.0,
            "footnote_overlap_threshold": 0.5,
            "footnote_offset": 200,
            "use_horizontal_lines": True,
            "remove_by_line": True,
            "remove_by_curve": True,
            "x_offset": 15,
            "y_offset": 4,
            "consider_font_size": True,
            "indent_offset": 25,
            "listing_offset": 45,
            "max_headline_len": 10,
            "headline_names": [
                "Abstract", "References", "Acknowledgement", "Acknowledgements",
                "Acknowledgment", "Acknowledgments", "Appendix", "Appendices",
                "Limitations", "Ethics Statement", "Ethics Statements"
            ],
            "column_offset": 300
        }
        return argparse.Namespace(**args_dict)
    elif paper_type == "AAAI2":
        args_dict: dict = {
            "input_dir_or_file_path": args.input_dir_or_file_path,
            "output_dir": args.output_dir,
            "paper_type": args.paper_type,
            "pipeline": [
                "load_docs", "remove_illegal_tokens", "remove_meta", "extract_lines",
                "extract_footnotes", "remove_lines_by_objects", "extract_paragraphs",
                "detect_sections", "concat_columns", "concat_pages", "dump_formatted_doc"
            ],
            "verbose": args.verbose,
            "insert_page_break": args.insert_page_break,
            "show_pos": args.show_pos,
            "show_font": args.show_font,
            "show_style": args.show_style,
            "show_meta": args.show_meta,
            "x_tolerance": 1.2,
            "header_offset": 65,
            "footer_offset": 80,
            "left_side_offset": 40,
            "right_side_offset": 40,
            "y_tolerance": 3.0,
            "footnote_offset": 200,
            "use_horizontal_lines": True,
            "object_bbox_offset": 25,
            "remove_by_line": True,
            "remove_by_curve": True,
            "x_offset": 15,
            "y_offset": 4,
            "consider_font_size": True,
            "indent_offset": 25,
            "listing_offset": 45,
            "max_headline_len": 10,
            "headline_names": [
                "Abstract", "References", "Acknowledgement", "Acknowledgements",
                "Acknowledgment", "Acknowledgments", "Appendix", "Appendices",
                "Limitations", "Ethics Statement", "Ethics Statements"
            ],
            "column_offset": 300
        }
        return argparse.Namespace(**args_dict)
    elif paper_type == "ACM":
        args_dict: dict = {
            "input_dir_or_file_path": args.input_dir_or_file_path,
            "output_dir": args.output_dir,
            "paper_type": args.paper_type,
            "pipeline": [
                "load_docs", "load_objects_with_ml", "remove_illegal_tokens",
                "remove_meta", "extract_lines", "extract_captions_with_ml",
                "remove_figures_with_ml", "remove_tables_with_ml", "remove_equations_with_ml",
                "extract_footnotes_with_ml", "extract_footnotes", "remove_lines_by_objects",
                "extract_paragraphs", "detect_sections", "tailor_references", 
                "concat_pages", "dump_formatted_doc"
            ],
            "verbose": args.verbose,
            "insert_page_break": args.insert_page_break,
            "show_pos": args.show_pos,
            "show_font": args.show_font,
            "show_style": args.show_style,
            "show_meta": args.show_meta,
            "x_tolerance": 1.2,
            "tablebank_threshold": 0.9,
            "detectron_device_mode": args.detectron_device_mode,
            "save_image": args.save_image,
            "output_image_dir": args.output_image_dir,
            "header_offset": 60,
            "footer_offset": 90,
            "left_side_offset": 40,
            "right_side_offset": 40,
            "y_tolerance": 6.0,
            "object_bbox_offset": 25,
            "equation_overlap_threshold": 0.5,
            "caption_overlap_threshold": 0.5,
            "table_start_ptn_str": r"Table [0-9]+.",
            "figure_start_ptn_str": r"Fig. [0-9]+.",
            "preset_table_caption_pos": "above",
            "preset_figure_caption_pos": "below",
            "caption_assignment_threshold": 75.0,
            "footnote_overlap_threshold": 0.5,
            "footnote_offset": 200,
            "use_horizontal_lines": True,
            "remove_by_line": True,
            "remove_by_curve": True,
            "x_offset": 15,
            "y_offset": 4,
            "consider_font_size": True,
            "indent_offset": 35,
            "listing_offset": 60,
            "max_headline_len": 10,
            "headline_names": [
                "Abstract", "REFERENCES", "References", "Acknowledgement", "Acknowledgements",
                "Acknowledgment", "Acknowledgments", "Appendix", "Appendices",
                "Limitations", "Ethics Statement", "Ethics Statements"
            ]
        }
        return argparse.Namespace(**args_dict)
    elif paper_type == "ACM2":
        args_dict: dict = {
            "input_dir_or_file_path": args.input_dir_or_file_path,
            "output_dir": args.output_dir,
            "paper_type": args.paper_type,
            "pipeline": [
                "load_docs", "remove_illegal_tokens", "remove_meta", "extract_lines",
                "extract_footnotes", "remove_lines_by_objects", "extract_paragraphs",
                "detect_sections", "tailor_references", "concat_pages", "dump_formatted_doc"
            ],
            "verbose": args.verbose,
            "insert_page_break": args.insert_page_break,
            "show_pos": args.show_pos,
            "show_font": args.show_font,
            "show_style": args.show_style,
            "show_meta": args.show_meta,
            "x_tolerance": 1.2,
            "header_offset": 60,
            "footer_offset": 90,
            "left_side_offset": 40,
            "right_side_offset": 40,
            "y_tolerance": 6.0,
            "footnote_offset": 200,
            "use_horizontal_lines": True,
            "object_bbox_offset": 25,
            "remove_by_line": True,
            "remove_by_curve": True,
            "x_offset": 15,
            "y_offset": 4,
            "consider_font_size": True,
            "indent_offset": 35,
            "listing_offset": 60,
            "max_headline_len": 10,
            "headline_names": [
                "Abstract", "REFERENCES", "References", "Acknowledgement", "Acknowledgements",
                "Acknowledgment", "Acknowledgments", "Appendix", "Appendices",
                "Limitations", "Ethics Statement", "Ethics Statements"
            ]
        }
        return argparse.Namespace(**args_dict)
    elif paper_type == "IEEE":
        args_dict: dict = {
            "input_dir_or_file_path": args.input_dir_or_file_path,
            "output_dir": args.output_dir,
            "paper_type": args.paper_type,
            "pipeline": [
                "load_docs", "load_objects_with_ml", "remove_illegal_tokens",
                "remove_meta", "extract_lines", "extract_captions_with_ml",
                "remove_figures_with_ml", "remove_tables_with_ml", "remove_equations_with_ml",
                "extract_footnotes_with_ml", "extract_footnotes", "remove_lines_by_objects",
                "extract_paragraphs", "detect_sections", "concat_columns", 
                "concat_pages", "dump_formatted_doc"
            ],
            "verbose": args.verbose,
            "insert_page_break": args.insert_page_break,
            "show_pos": args.show_pos,
            "show_font": args.show_font,
            "show_style": args.show_style,
            "show_meta": args.show_meta,
            "x_tolerance": 1.2,
            "tablebank_threshold": 0.9,
            "detectron_device_mode": args.detectron_device_mode,
            "save_image": args.save_image,
            "output_image_dir":args.output_image_dir,
            "header_offset": 60,
            "footer_offset": 80,
            "left_side_offset": 40,
            "right_side_offset": 40,
            "y_tolerance": 3.0,
            "object_bbox_offset": 25,
            "equation_overlap_threshold": 0.5,
            "caption_overlap_threshold": 0.5,
            "table_start_ptn_str": r"TABLE [IVXLCDM]+",
            "figure_start_ptn_str": r"Fig. [0-9]+.",
            "preset_table_caption_pos": "above",
            "preset_figure_caption_pos": "below",
            "caption_assignment_threshold": 75.0,
            "footnote_overlap_threshold": 0.5,
            "footnote_offset": 200,
            "use_horizontal_lines": True,
            "remove_by_line": True,
            "remove_by_curve": True,
            "x_offset": 10,
            "y_offset": 4,
            "consider_font_size": True,
            "indent_offset": 25,
            "listing_offset": 40,
            "max_headline_len": 10,
            "headline_names": [
                "Abstract", "REFERENCES", "ACKNOWLEDGEMENT", "ACKNOWLEDGEMENTS",
                "ACKNOWLEDGMENT", "ACKNOWLEDGMENTS", "APPENDIX", "APPENDICES",
                "LIMITATIONS", "ETHICS STATEMENT", "ETHICS STATEMENTS"
            ],
            "column_offset": 300
        }
        return argparse.Namespace(**args_dict)
    elif paper_type == "IEEE2":
        args_dict: dict = {
            "input_dir_or_file_path": args.input_dir_or_file_path,
            "output_dir": args.output_dir,
            "paper_type": args.paper_type,
            "pipeline": [
                "load_docs", "remove_illegal_tokens", "remove_meta", "extract_lines",
                "extract_footnotes", "remove_lines_by_objects", "extract_paragraphs",
                "detect_sections", "concat_columns", "concat_pages", "dump_formatted_doc"
            ],
            "verbose": args.verbose,
            "insert_page_break": args.insert_page_break,
            "show_pos": args.show_pos,
            "show_font": args.show_font,
            "show_style": args.show_style,
            "show_meta": args.show_meta,
            "x_tolerance": 1.2,
            "header_offset": 60,
            "footer_offset": 80,
            "left_side_offset": 40,
            "right_side_offset": 40,
            "y_tolerance": 3.0,
            "footnote_offset": 200,
            "use_horizontal_lines": True,
            "object_bbox_offset": 25,
            "remove_by_line": True,
            "remove_by_curve": True,
            "x_offset": 10,
            "y_offset": 4,
            "consider_font_size": True,
            "indent_offset": 25,
            "listing_offset": 40,
            "max_headline_len": 10,
            "headline_names": [
                "Abstract", "REFERENCES", "ACKNOWLEDGEMENT", "ACKNOWLEDGEMENTS",
                "ACKNOWLEDGMENT", "ACKNOWLEDGMENTS", "APPENDIX", "APPENDICES",
                "LIMITATIONS", "ETHICS STATEMENT", "ETHICS STATEMENTS"
            ],
            "column_offset": 300
        }
        return argparse.Namespace(**args_dict)
    elif paper_type == "Springer":
        args_dict: dict = {
            "input_dir_or_file_path": args.input_dir_or_file_path,
            "output_dir": args.output_dir,
            "paper_type": args.paper_type,
            "pipeline": [
                "load_docs", "load_objects_with_ml", "remove_illegal_tokens",
                "remove_meta", "extract_lines", "extract_captions_with_ml",
                "remove_figures_with_ml", "remove_tables_with_ml", "remove_equations_with_ml",
                "extract_footnotes_with_ml", "extract_footnotes", "remove_lines_by_objects",
                "extract_paragraphs", "detect_sections", "concat_pages", "dump_formatted_doc"
            ],
            "verbose": args.verbose,
            "insert_page_break": args.insert_page_break,
            "show_pos": args.show_pos,
            "show_font": args.show_font,
            "show_style": args.show_style,
            "show_meta": args.show_meta,
            "x_tolerance": 1.2,
            "tablebank_threshold": 0.9,
            "detectron_device_mode": args.detectron_device_mode,
            "save_image": args.save_image,
            "output_image_dir": args.output_image_dir,
            "header_offset": 60,
            "footer_offset": 90,
            "left_side_offset": 40,
            "right_side_offset": 40,
            "y_tolerance": 3.0,
            "object_bbox_offset": 25,
            "equation_overlap_threshold": 0.5,
            "caption_overlap_threshold": 0.5,
            "table_start_ptn_str": r"Table [0-9]+.",
            "figure_start_ptn_str": r"Fig. [0-9]+.",
            "preset_table_caption_pos": "above",
            "preset_figure_caption_pos": "below",
            "caption_assignment_threshold": 75.0,
            "footnote_overlap_threshold": 0.5,
            "footnote_offset": 200,
            "use_horizontal_lines": True,
            "remove_by_line": True,
            "remove_by_curve": True,
            "x_offset": 15,
            "y_offset": 4,
            "consider_font_size": True,
            "indent_offset": 35,
            "listing_offset": 60,
            "max_headline_len": 10,
            "headline_names": [
                "Abstract", "References", "Acknowledgement", "Acknowledgements",
                "Acknowledgment", "Acknowledgments", "Appendix", "Appendices",
                "Limitations", "Ethics Statement", "Ethics Statements"
            ]
        }
        return argparse.Namespace(**args_dict)
    elif paper_type == "Springer2":
        args_dict: dict = {
            "input_dir_or_file_path": args.input_dir_or_file_path,
            "output_dir": args.output_dir,
            "paper_type": args.paper_type,
            "pipeline": [
                "load_docs", "remove_illegal_tokens", "remove_meta", "extract_lines",
                "extract_footnotes", "remove_lines_by_objects", "extract_paragraphs",
                "detect_sections", "concat_pages", "dump_formatted_doc"
            ],
            "verbose": args.verbose,
            "insert_page_break": args.insert_page_break,
            "show_pos": args.show_pos,
            "show_font": args.show_font,
            "show_style": args.show_style,
            "show_meta": args.show_meta,
            "x_tolerance": 1.2,
            "header_offset": 60,
            "footer_offset": 90,
            "left_side_offset": 40,
            "right_side_offset": 40,
            "y_tolerance": 3.0,
            "footnote_offset": 200,
            "use_horizontal_lines": True,
            "object_bbox_offset": 25,
            "remove_by_line": True,
            "remove_by_curve": True,
            "x_offset": 15,
            "y_offset": 4,
            "consider_font_size": True,
            "indent_offset": 35,
            "listing_offset": 60,
            "max_headline_len": 10,
            "headline_names": [
                "Abstract", "References", "Acknowledgement", "Acknowledgements",
                "Acknowledgment", "Acknowledgments", "Appendix", "Appendices",
                "Limitations", "Ethics Statement", "Ethics Statements"
            ]
        }
        return argparse.Namespace(**args_dict)
    elif paper_type == 'ICML':
        args_dict: dict = {
            "input_dir_or_file_path": args.input_dir_or_file_path,
            "output_dir": args.output_dir,
            "paper_type": args.paper_type,
            "pipeline": [
                "load_docs", "load_objects_with_ml", "remove_illegal_tokens",
                "remove_meta", "extract_lines", "extract_captions_with_ml",
                "remove_figures_with_ml", "remove_tables_with_ml", "remove_equations_with_ml",
                "extract_footnotes_with_ml", "extract_footnotes", "remove_lines_by_objects",
                "extract_paragraphs", "detect_sections", "tailor_references", 
                "concat_columns", "concat_pages", "dump_formatted_doc"
            ],
            "verbose": args.verbose,
            "insert_page_break": args.insert_page_break,
            "show_pos": args.show_pos,
            "show_font": args.show_font,
            "show_style": args.show_style,
            "show_meta": args.show_meta,
            "x_tolerance": 1.2,
            "tablebank_threshold": 0.9,
            "detectron_device_mode": args.detectron_device_mode,
            "save_image": args.save_image,
            "output_image_dir": args.output_image_dir,
            "header_offset": 65,
            "footer_offset": 80,
            "left_side_offset": 40,
            "right_side_offset": 40,
            "y_tolerance": 3.0,
            "object_bbox_offset": 25,
            "equation_overlap_threshold": 0.5,
            "caption_overlap_threshold": 0.5,
            "table_start_ptn_str": r"Table [A-Z\.]*[0-9]+:",
            "figure_start_ptn_str": r"Figure [A-Z\.]*[0-9]+:",
            "preset_table_caption_pos": "above",
            "preset_figure_caption_pos": "below",
            "caption_assignment_threshold": 75.0,
            "footnote_overlap_threshold": 0.5,
            "footnote_offset": 200,
            "use_horizontal_lines": True,
            "remove_by_curve": True,
            "x_offset": 15,
            "y_offset": 4,
            "consider_font_size": True,
            "indent_offset": 25,
            "listing_offset": 45,
            "max_headline_len": 10,
            "headline_names": [
                "Abstract", "References", "Acknowledgement", "Acknowledgements",
                "Acknowledgment", "Acknowledgments", "Appendix", "Appendices",
                "Limitations", "Ethics Statement", "Ethics Statements"
            ],
            "column_offset": 300
        }
        return argparse.Namespace(**args_dict)
    elif paper_type == "ICML2":
        args_dict: dict = {
            "input_dir_or_file_path": args.input_dir_or_file_path,
            "output_dir": args.output_dir,
            "paper_type": args.paper_type,
            "pipeline": [
                "load_docs", "remove_illegal_tokens", "remove_meta", "extract_lines",
                "extract_footnotes", "remove_lines_by_objects", "extract_paragraphs",
                "detect_sections", "tailor_references", "concat_columns", "concat_pages", "dump_formatted_doc"
            ],
            "verbose": args.verbose,
            "insert_page_break": args.insert_page_break,
            "show_pos": args.show_pos,
            "show_font": args.show_font,
            "show_style": args.show_style,
            "show_meta": args.show_meta,
            "x_tolerance": 1.2,
            "header_offset": 65,
            "footer_offset": 80,
            "left_side_offset": 40,
            "right_side_offset": 40,
            "y_tolerance": 3.0,
            "footnote_offset": 200,
            "use_horizontal_lines": True,
            "object_bbox_offset": 25,
            "remove_by_curve": True,
            "x_offset": 15,
            "y_offset": 4,
            "consider_font_size": True,
            "indent_offset": 25,
            "listing_offset": 45,
            "max_headline_len": 10,
            "headline_names": [
                "Abstract", "References", "Acknowledgement", "Acknowledgements",
                "Acknowledgment", "Acknowledgments", "Appendix", "Appendices",
                "Limitations", "Ethics Statement", "Ethics Statements"
            ],
            "column_offset": 300
        }
        return argparse.Namespace(**args_dict)
    elif paper_type == "ICLR":
        args_dict: dict = {
            "input_dir_or_file_path": args.input_dir_or_file_path,
            "output_dir": args.output_dir,
            "paper_type": args.paper_type,
            "pipeline": [
                "load_docs", "load_objects_with_ml", "remove_illegal_tokens",
                "remove_meta", "extract_lines", "extract_captions_with_ml",
                "remove_figures_with_ml", "remove_tables_with_ml", "remove_equations_with_ml",
                "extract_footnotes_with_ml", "extract_footnotes", "remove_lines_by_objects",
                "extract_paragraphs", "detect_sections", "tailor_references", "concat_pages", "dump_formatted_doc"
            ],
            "verbose": args.verbose,
            "insert_page_break": args.insert_page_break,
            "show_pos": args.show_pos,
            "show_font": args.show_font,
            "show_style": args.show_style,
            "show_meta": args.show_meta,
            "x_tolerance": 1.2,
            "tablebank_threshold": 0.9,
            "detectron_device_mode": args.detectron_device_mode,
            "save_image": args.save_image,
            "output_image_dir": args.output_image_dir,
            "header_offset": 60,
            "footer_offset": 75,
            "left_side_offset": 40,
            "right_side_offset": 40,
            "y_tolerance": 3.0,
            "object_bbox_offset": 25,
            "equation_overlap_threshold": 0.5,
            "caption_overlap_threshold": 0.5,
            "table_start_ptn_str": r"Table [0-9]+:",
            "figure_start_ptn_str": r"Figure [0-9]+:",
            "preset_table_caption_pos": "below",
            "preset_figure_caption_pos": "below",
            "caption_assignment_threshold": 75.0,
            "footnote_overlap_threshold": 0.5,
            "footnote_offset": 200,
            "use_horizontal_lines": True,
            "remove_by_line": True,
            "remove_by_curve": True,
            "x_offset": 15,
            "y_offset": 4,
            "consider_font_size": True,
            "indent_offset": 35,
            "listing_offset": 60,
            "max_headline_len": 10,
            "headline_names": [
                "Abstract", "References", "Acknowledgement", "Acknowledgements",
                "Acknowledgment", "Acknowledgments", "Appendix", "Appendices",
                "Limitations", "Ethics Statement", "Ethics Statements"
            ]
        }
        return argparse.Namespace(**args_dict)
    elif paper_type == "ICLR2":
        args_dict: dict = {
            "input_dir_or_file_path": args.input_dir_or_file_path,
            "output_dir": args.output_dir,
            "paper_type": args.paper_type,
            "pipeline": [
                "load_docs", "remove_illegal_tokens", "remove_meta", "extract_lines",
                "extract_footnotes", "remove_lines_by_objects", "extract_paragraphs",
                "detect_sections", "tailor_references", "concat_pages", "dump_formatted_doc"
            ],
            "verbose": args.verbose,
            "insert_page_break": args.insert_page_break,
            "show_pos": args.show_pos,
            "show_font": args.show_font,
            "show_style": args.show_style,
            "show_meta": args.show_meta,
            "x_tolerance": 1.2,
            "header_offset": 60,
            "footer_offset": 75,
            "left_side_offset": 40,
            "right_side_offset": 40,
            "y_tolerance": 3.0,
            "footnote_offset": 200,
            "use_horizontal_lines": True,
            "object_bbox_offset": 25,
            "remove_by_line": True,
            "remove_by_curve": True,
            "x_offset": 15,
            "y_offset": 4,
            "consider_font_size": True,
            "indent_offset": 35,
            "listing_offset": 60,
            "max_headline_len": 10,
            "headline_names": [
                "Abstract", "References", "Acknowledgement", "Acknowledgements",
                "Acknowledgment", "Acknowledgments", "Appendix", "Appendices",
                "Limitations", "Ethics Statement", "Ethics Statements"
            ]
        }
        return argparse.Namespace(**args_dict)
    elif paper_type == "NeurIPS":
        args_dict: dict = {
            "input_dir_or_file_path": args.input_dir_or_file_path,
            "output_dir": args.output_dir,
            "paper_type": args.paper_type,
            "pipeline": [
                "load_docs", "load_objects_with_ml", "remove_illegal_tokens",
                "remove_meta", "extract_lines", "extract_captions_with_ml",
                "remove_figures_with_ml", "remove_tables_with_ml", "remove_equations_with_ml",
                "extract_footnotes_with_ml", "extract_footnotes", "remove_lines_by_objects",
                "extract_paragraphs", "detect_sections", "tailor_references", "concat_pages", "dump_formatted_doc"
            ],
            "verbose": args.verbose,
            "insert_page_break": args.insert_page_break,
            "show_pos": args.show_pos,
            "show_font": args.show_font,
            "show_style": args.show_style,
            "show_meta": args.show_meta,
            "x_tolerance": 1.2,
            "tablebank_threshold": 0.9,
            "detectron_device_mode": args.detectron_device_mode,
            "save_image": args.save_image,
            "output_image_dir": args.output_image_dir,
            "header_offset": 60,
            "footer_offset": 75,
            "left_side_offset": 40,
            "right_side_offset": 40,
            "y_tolerance": 3.0,
            "object_bbox_offset": 25,
            "equation_overlap_threshold": 0.5,
            "caption_overlap_threshold": 0.5,
            "table_start_ptn_str": r"Table [0-9]+:",
            "figure_start_ptn_str": r"Figure [0-9]+:",
            "preset_table_caption_pos": "above",
            "preset_figure_caption_pos": "below",
            "caption_assignment_threshold": 75.0,
            "footnote_overlap_threshold": 0.5,
            "footnote_offset": 200,
            "use_horizontal_lines": True,
            "remove_by_line": True,
            "remove_by_curve": True,
            "x_offset": 15,
            "y_offset": 4,
            "consider_font_size": True,
            "indent_offset": 35,
            "listing_offset": 60,
            "max_headline_len": 10,
            "headline_names": [
                "Abstract", "References", "Acknowledgement", "Acknowledgements",
                "Acknowledgment", "Acknowledgments", "Appendix", "Appendices",
                "Limitations", "Ethics Statement", "Ethics Statements"
            ]
        }
        return argparse.Namespace(**args_dict)
    elif paper_type == "NeurIPS2":
        args_dict: dict = {
            "input_dir_or_file_path": args.input_dir_or_file_path,
            "output_dir": args.output_dir,
            "paper_type": args.paper_type,
            "pipeline": [
                "load_docs", "remove_illegal_tokens", "remove_meta", "extract_lines",
                "extract_footnotes", "remove_lines_by_objects", "extract_paragraphs",
                "detect_sections", "tailor_references", "concat_pages", "dump_formatted_doc"
            ],
            "verbose": args.verbose,
            "insert_page_break": args.insert_page_break,
            "show_pos": args.show_pos,
            "show_font": args.show_font,
            "show_style": args.show_style,
            "show_meta": args.show_meta,
            "x_tolerance": 1.2,
            "header_offset": 60,
            "footer_offset": 75,
            "left_side_offset": 40,
            "right_side_offset": 40,
            "y_tolerance": 3.0,
            "footnote_offset": 200,
            "use_horizontal_lines": True,
            "object_bbox_offset": 25,
            "remove_by_line": True,
            "remove_by_curve": True,
            "x_offset": 15,
            "y_offset": 4,
            "consider_font_size": True,
            "indent_offset": 35,
            "listing_offset": 60,
            "max_headline_len": 10,
            "headline_names": [
                "Abstract", "References", "Acknowledgement", "Acknowledgements",
                "Acknowledgment", "Acknowledgments", "Appendix", "Appendices",
                "Limitations", "Ethics Statement", "Ethics Statements"
            ]
        }
        return argparse.Namespace(**args_dict)
    else:
        raise ValueError()
    