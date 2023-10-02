from pathlib import Path

from .modules.doc import Document
from .modules.runner import BaseRunner
from .utils import (NotAPDFError, PipelineOrderError, check_pipeline,
                    get_template, print_data)


def main(args):
    #####
    # Sanity check 
    #####
    # input
    input_path: Path = Path(args.input_dir_or_file_path)
    is_dir: bool = False
    if not input_path.exists():
        raise FileNotFoundError()
    elif input_path.is_dir():
        is_dir = True
    elif input_path.suffix.lower() != ".pdf":
        raise NotAPDFError(f"Invalid file type. Expected a PDF, but got: {input_path.suffix}")
    # output
    output_dir: Path = Path(args.output_dir)
    if not output_dir.exists():
        output_dir.mkdir()
        print(f"{args.output_dir} does not exist. Create a new directory.")
    # template & pipeline
    if args.paper_type is not None:
        new_args = get_template(args.paper_type, args)
        print(f"Overwrite the pipeline {args.pipeline} to {new_args.pipeline} following --paper_type={args.paper_type}.")
        args = new_args
    elif args.pipeline == None:
        raise NotImplementedError("Please specify `--pipeline` when `--paper_type` is not set!")
    # pipeline check
    if check_pipeline(args.pipeline) is False:
        raise PipelineOrderError()
    
    #####
    # Load PDF files
    #####
    docs: list[Document] = []
    if is_dir:
        for pdf_path in input_path.glob('**/*.pdf'):
            docs.append(Document(pdf_path))
    else:
        docs.append(Document(input_path))
        
    #####
    # Process PDF files
    #####
    for index, module_name in enumerate(args.pipeline):
        print(f'Now running {index}: {module_name}')
        
        # get a module instance
        module_cls = BaseRunner.by_name(module_name)

        # execute a process
        docs = module_cls().execute(documents=docs, **vars(args))

        # print and save current data
        if args.verbose:
            print_data(
                docs, 
                output_dir, 
                f'{index}_{module_name}',
                args.insert_page_break,
                args.show_pos,
                args.show_font,
                args.show_style,
                args.show_meta
            )
    

def run_cli():
    """`appjsonify` CLI Entrypoint."""
    import argparse
    parser = argparse.ArgumentParser(description="appjsonify: An Academic Paper PDF to JSON Conversion Toolkit.")
    
    #####
    # required
    #####
    parser.add_argument(
        "input_dir_or_file_path", 
        default=None, 
        type=str, 
        help="Specify an input directory that contains PDF files or a path to a target PDF."
    )
    parser.add_argument(
        "output_dir", 
        default=None, 
        type=str, 
        help="Specify an output directory."
    )

    #####
    # optional
    #####
    # template
    parser.add_argument(
        "--paper_type",
        default=None,
        type=str,
        required=False,
        choices=['ACL', 'ACL2', 'AAAI', 'AAAI2', 'ACM', 'ACM2', 'IEEE', 'IEEE2', 
                 'ICML', 'ICML2', 'ICLR', 'ICLR2', 'NeurIPS', 'NeurIPS2', 'Springer', 'Springer2'],
        help="Specify a paper format from ACL, AAAI, ACM, IEEE, ICML, ICLR, NeurIPS, and Springer. " \
            + "`2` denotes a rule-based approach, which is a faster but produces a bit noisy output."
    )
    
    # manual processing
    parser.add_argument(
        '--pipeline', 
        type=str, 
        nargs='+', 
        required=False, 
        default=None,
        help="Specify module names that you want to use in the process."
    )
    
    # common settings
    parser.add_argument(
        '--consider_font_size', 
        action='store_true', 
        default=False,
        help="[extract_paragraphs, concat_columns, concat_pages] " \
            + "Consider font size in judgements. Defaults to False."
    )
    parser.add_argument(
        '--max_headline_len', 
        type=int, 
        default=30,
        help='[detect_sections, load_objects_with_ml] Specify a maximum value to determine ' \
             + 'if an element is a headline. Defaults to 30.'
    )
    parser.add_argument(
        '--object_bbox_offset', 
        type=int, 
        default=25,
        help='[remove_lines_by_objects, remove_figures_with_ml, remove_tables_with_ml] ' \
            + 'Specify a threshold value to determine ' \
            + 'if an element is within the margin area of an object. Defaults to 25.'
    )
    parser.add_argument(
        '--listing_offset', 
        type=int, 
        default=40,
        help='[extract_paragraphs, tailor_references] Specify a threshold offset for listing. Defaults to 40.'
    )
    
    # load_docs settings
    parser.add_argument(
        '--x_tolerance', 
        type=float, 
        default=3.5,
        help="[load_docs] Specify a threshold value to determine " \
            + "if one character forms the same word. Defaults to 3.5."
    )
    
    # load_objects_with_ml settings
    parser.add_argument(
        '--tablebank_threshold', 
        type=float, 
        default=0.9,
        help="[load_objects_with_ml] Specify a threshold value for a TableBank detection model."
    )
    parser.add_argument(
        '--publaynet_threshold', 
        type=float, 
        default=0.75,
        help="[load_objects_with_ml] Specify a threshold value for a Publaynet detection model."
    )
    parser.add_argument(
        '--docbank_threshold', 
        type=float, 
        default=0.75,
        help="[load_objects_with_ml] Specify a threshold value for a DocBank detection model."
    )
    parser.add_argument(
        '--detectron_device_mode', 
        type=str,  
        choices=['cpu', 'cuda'], 
        default='cpu',
        help="[load_objects_with_ml] Specify a type of a device for Detectron2 based models."
    )
    parser.add_argument(
        '--save_image', 
        action='store_true', 
        default=False,
        help="[load_objects_with_ml] " \
             + "Set this to save object images. Defaults to False."
    )
    parser.add_argument(
        '--output_image_dir', 
        type=str,
        default='',
        help="[load_objects_with_ml] Specify an image path if `save_image` is True."
    )
    
    # extract_lines settings
    parser.add_argument(
        '--y_tolerance', 
        type=float, 
        default=3.0,
        help="[extract_lines] Specify a threshold value to determine " \
            + "if different tokens are in the same line. Defaults to 3.0."
    )
    
    # remove_meta settings
    parser.add_argument(
        '--header_offset', 
        type=int, 
        default=80,
        help='[remove_meta] Specify a threshold value to determine ' \
            + 'if an element is a header. Defaults to 80.'
    )
    parser.add_argument(
        '--footer_offset', 
        type=int, 
        default=80,
        help='[remove_meta] Specify a threshold value to determine ' \
            + 'if an element is a footer. Defaults to 80.'
    )
    parser.add_argument(
        '--left_side_offset', 
        type=int, 
        default=40,
        help='[remove_meta] Specify a threshold value to determine ' \
        + 'if an element is in a left-hand side margin area. Defaults to 40.'
    )
    parser.add_argument(
        '--right_side_offset', 
        type=int, 
        default=40,
        help='[remove_meta] Specify a threshold value to determine ' \
            + 'if an element is in a right-hand side margin area. Defaults to 40.'
    )

    # extract_footnotes settings
    parser.add_argument(
        '--footnote_offset', 
        type=int, 
        default=150,
        help='[extract_footnotes] Specify a threshold value to determine ' \
            + 'if an element is a footnote or not. Defaults to 150.'
    )
    parser.add_argument(
        '--use_horizontal_lines',
        action='store_true', 
        default=False,
        help="[extract_footnotes] Set this to use horizontal line object information " \
             + "to judge whether a token is a footnote or not. Defaults to False."
    )
    
    # remove_lines_by_objects settings
    parser.add_argument(
        '--remove_by_obj', 
        action='store_true', 
        default=False,
        help='[remove_lines_by_objects] Set this to remove captions based on ' \
            + 'bounding box information on objects. Defaults to False.'
    )
    parser.add_argument(
        '--remove_by_line', 
        action='store_true', 
        default=False,
        help='[remove_lines_by_objects] Set this to remove captions based on ' \
            + 'bounding box information on line objects. Defaults to False.'
    )
    parser.add_argument(
        '--remove_by_rect', 
        action='store_true', 
        default=False,
        help='[remove_lines_by_objects] Set this to remove captions based on ' \
            + 'bounding box information on rect objects. Defaults to False.'
    )
    parser.add_argument(
        '--remove_by_curve', 
        action='store_true', 
        default=False,
        help='[remove_lines_by_objects] Set this to remove captions based on ' \
            + 'bounding box information on curve objects. Defaults to False.'
    )
    
    # remove_equations_with_ml settings
    parser.add_argument(
        '--equation_overlap_threshold', 
        type=float, 
        default=0.5,
        help='[remove_equations_with_ml] Specify a threshold value to determine ' \
            + 'if a line is a equation. Defaults to 0.5.'
    )
    
    # extract_captions_with_ml settings
    parser.add_argument(
        '--caption_overlap_threshold', 
        type=float, 
        default=0.5,
        help='[extract_captions_with_ml] Specify a threshold value to determine ' \
            + 'if a line is a caption. Defaults to 0.5.'
    )
    parser.add_argument(
        '--table_start_ptn_str', 
        type=str, 
        default=r'Table [0-9]+:',
        help='[extract_captions_with_ml] Specify a regex pattern to detect ' \
            + 'a caption for a table.'
    )
    parser.add_argument(
        '--figure_start_ptn_str', 
        type=str, 
        default=r'Figure [0-9]+:',
        help='[extract_captions_with_ml] Specify a regex pattern to detect ' \
            + 'a caption for a figure.'
    )
    parser.add_argument(
        '--preset_table_caption_pos', 
        type=str, 
        choices=['standard', 'below', 'above'],
        default='standard',
        help="[extract_captions_with_ml] " \
             + "Specify if you want to assume the position of table captions. " \
             + "Defaults to `standard`."
    )
    parser.add_argument(
        '--preset_figure_caption_pos', 
        type=str, 
        choices=['standard', 'below', 'above'],
        default='standard',
        help="[extract_captions_with_ml] " \
             + "Specify if you want to assume the position of figure captions. " \
             + "Defaults to `standard`."
    )
    parser.add_argument(
        '--caption_assignment_threshold', 
        type=float, 
        default=75.0,
        help='[extract_captions_with_ml] Specify a threshold distance value to determine ' \
            + 'if we should assign a caption to a table or image. Defaults to 75.0.'
    )
    
    # extract_footnotes_with_ml settings
    parser.add_argument(
        '--footnote_overlap_threshold', 
        type=float, 
        default=0.5,
        help='[extract_footnotes_with_ml] Specify a threshold value to determine ' \
            + 'if a line is a footnote. Defaults to 0.5.'
    )

    # extract_paragraphs settings
    parser.add_argument(
        '--x_offset', 
        type=int, 
        default=18,
        help='[extract_paragraphs] Specify a threshold x-axis value to determine ' \
            + 'if different elements are in the same paragraph. Defaults to 18.'
    )
    parser.add_argument(
        '--y_offset', 
        type=int, 
        default=4,
        help='[extract_paragraphs] Specify a threshold y-axis value to determine ' \
            + 'if different elements are in the same paragraph. Defaults to 4.'
    )
    parser.add_argument(
        '--indent_offset', 
        type=int, 
        default=25,
        help='[extract_paragraphs] Specify a threshold offset for indents. Defaults to 25.'
    )
    
    # detect_sections settings
    parser.add_argument(
        '--headline_names', 
        type=str, 
        nargs='+',
        default=[],
        help='[detect_sections] Specify a known headline name(s) ' \
             + 'if they do not have section numbers.'
    )
    
    # concat_columns settings
    parser.add_argument(
        '--column_offset', 
        type=int, 
        default=300,
        help='[concat_column] Specify a threshold value to determine ' \
            + 'if an element is in a different column from a previous one. ' \
            + 'Defaults to 300.'
    )
    
    # print settings
    parser.add_argument(
        '--verbose', 
        action='store_true', 
        default=False,
        help="Set this to save intermediate log files."
    )
    parser.add_argument(
        '--insert_page_break', 
        action='store_true', 
        default=False,
        help="Set this to insert page breaks when printing results."
    )
    parser.add_argument(
        '--show_pos', 
        action='store_true', 
        default=False,
        help="Set this to insert bounding box information " \
             + "when printing intermediate results."
    ) 
    parser.add_argument(
        '--show_font',
        action='store_true', 
        default=False,
        help="Set this to insert font information " \
             + "when printing intermediate results."
    )
    parser.add_argument(
        '--show_style',
        action='store_true', 
        default=False,
        help="Set this to insert style information " \
             + "when printing intermediate results."
    )
    parser.add_argument(
        '--show_meta',
        action='store_true', 
        default=False,
        help="Set this to insert meta information " \
             + "when printing intermediate results."
    )
    
    args = parser.parse_args()
    main(args)
    

if __name__ == "__main__":
    run_cli()
