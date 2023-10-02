Available Modules
===
[Go back to top](../README.md)

This page explains all the modules available in `appjsonify` and their sample usage. Note that the `prerequisites` in the following tables means that such modules must be executed before a target module.

## Document loading related modules
| Module name | Description | Parameters | Prerequisites |
| -- | -- | -- | -- |
| [`load_docs`](../appjsonify/modules/load/load.py#L15) | `load_docs` loads tokens in given documents and adds them to each `Document` instance as `Token` instances. | <p>`x_tolerance`: A threshold value to determine if one character forms the same word. Defaults to 3.5.</p>  | None |
| [`load_objects_with_ml`](../appjsonify/modules/load/load_objects_with_ml.py#L17) | `load_objects_with_ml` loads objects such as `tables`, `figures`, and `captions`, and adds them to each `Page` instance as its `meta` dictionary. | <p>`tablebank_threshold`: A threshold value for a TableBank detection model. Defaults to 0.75.</p><p>`publaynet_threshold`: A threshold value for a Publaynet detection model. Defaults to 0.75.</p><p>`docbank_threshold`: A threshold value for a DocBank detection model. Defaults to 0.75.</p><p>`detectron_device_mode`: A type of a device for Detectron2 based models. Defaults to `cpu`.</p><p>`save_image`: Set this to save object images. Defaults to False.</p><p>`output_imgae_dir`: Specify an image path if `save_image` is True.</p> |  `load_docs` |

### Sample usage
The following will output all tokens contained in a PDF document as a JSON file.
```bash
appjsonify /path/to/pdf/dir/or/path /path/to/output/dir \
    --pipeline load_docs dump_doc_with_tokens \
    --x_tolerance 1.2
```


## Editing-related modules
### Extraction
| Module name | Description | Parameters | Prerequisites |
| -- | -- | -- | -- |
| [`extract_lines`](../appjsonify/modules/edit/extract_lines.py#L12) | `extract_lines` forms `Line` instances from tokens. Each instance indicates that tokens in registered in the instance should be in the same line. | <p>`y_tolerance`: A threshold value to determine if different tokens are in the same line. Defaults to 3.0.</p> | `load_docs` |
| [`extract_footnotes`](../appjsonify/modules/edit/extract_footnotes.py#L11) | `extract_footnotes` extracts `Line` instances from the body that should be footnotes and saves them as supplementary information. | <p>`footnote_offset`: A threshold value to determine if an element is a footnote or not. Defaults to 150.</p><p>`use_horizontal_lines`: Set this to use horizontal line object information to judge whether a token is a footnote or not. Defaults to False.</p> | `load_docs`, `extract_lines` |
| [`extract_paragraphs`](../appjsonify/modules/edit/extract_paragraphs.py#L12) | `extract_paragraphs` concatenates `Line` instances  and forms a `Paragraph` instance when the conditions are met. | <p>`x_offset`: An x-axis threshold value to determine if different lines are in the same paragraph. Defaults to 18.</p><p>`y_offset`: A y-axis threshold value to determine if different lines are in the same paragraph. Defaults to 4.</p><p>`consider_font_size`: Consider font size in making judgements. Defaults to False.</p><p>`indent_offset`: A threshold x-axis offset for indents. Defaults to 25.</p><p>`listing_offset`: A threshold x-axis offset for listing. Defaults to 40.</p> | `load_docs`, `extract_lines` |
| [`extract_captions_with_ml`](../appjsonify/modules/edit/extract_captions_with_ml.py#L12) | `extract_captions_with_ml` extracts `Line` instances that are highly likely to be captions using outputs from `load_objects_with_ml`. | <p>`caption_overlap_threshold`: A threshold value to determine if a line is a caption. Defaults to 0.5.</p><p>`table_start_ptn_str`: Specify a regex pattern to detect a caption for a table. Defaults to `Table [0-9]+:`.</p><p>`figure_start_ptn_str`: Specify a regex pattern to detect a caption for a figure. Defaults to `Figure [0-9]+:`.</p><p>`preset_table_caption_pos`: Specify if you want to assume the position of table captions from `stndard`, `below`, and `above`. Defaults to `standard`.</p><p>`preset_figure_caption_pos`: Specify if you want to assume the position of figure captions from `stndard`, `below`, and `above`. Defaults to `standard`.</p><p>`caption_assignment_threshold`: Specify a threshold distance value to determine if we should assign a caption to a table or image. Defaults to 75.0.</p> | `load_docs`, `load_objects_with_ml`, `extract_lines` |
| [`extract_footnotes_with_ml`](../appjsonify/modules/edit/extract_footnotes_with_ml.py#L12) | `extract_footnotes_with_ml` extracts `Line` instances that are highly likely to be footnotes using outputs from `load_objects_with_ml`. | <p>`footnote_overlap_threshold`: A threshold value to determine if a line is a footnote. Defaults to 0.5.</p> | `load_docs`, `load_objects_with_ml`, `extract_lines` |


#### Sample usage
The following will not only output all lines contained in a PDF document but also extract captions and footnotes as supplemantary information.

Note that the following assumes the use of a GPU. If you do not have it, please remove `--detectron_device_mode cuda` or set ` --detectron_device_mode cpu`.

```bash
appjsonify /path/to/pdf/dir/or/path /path/to/output/dir \
    --pipeline load_docs load_objects_with_ml extract_lines extract_captions_with_ml extract_footnotes_with_ml dump_doc_with_lines \
    --x_tolerance 1.2 \
    --tablebank_threshold 0.9 \
    --publaynet_threshold 0.9 \
    --docbank_threshold 0.9 \
    --detectron_device_mode cuda \
    --y_tolerance 6.0 \
    --caption_overlap_threshold 0.5 \
    --table_start_ptn_str "Table [0-9]+:" \
    --figure_start_ptn_str "Figure [0-9]+:" \
    --preset_table_caption_pos below \
    --preset_figure_caption_pos below \
    --caption_assignment_threshold 75.0 \
    --footnote_overlap_threshold 0.5
```


### Editing
| Module name | Description | Parameters | Prerequisites |
| -- | -- | -- | -- |
| [`detect_sections`](../appjsonify/modules/edit/detect_sections.py#L12) | `detect_sections` judges whether a `Paragraph` is either a section, subsection, or body. Results will be used for formatting. | <p>`headline_names`: Specify a known headline name(s) if they do not have section numbers so that they can be easily recognized as a section.</p><p>`max_headline_len`: Specify a maximum number of words to determine if an element is a headline. Defaults to 30.</p><p>`paper_type`: If this is set, `detect_sections` will detect sections in a more fine-grained manner on the basis of font size and font name.</p> | `load_docs`, `extract_lines`, `extract_paragraphs` |
| [`tailor_references`](../appjsonify/modules/edit/tailor_references.py#L11) | `tailor_references` tailors reference paragraphs that are fragmented. | <p>`listing_offset`: A threshold x-axis offset for listing. Defaults to 40.</p> | `load_docs`, `extract_lines`, `extract_paragraphs`, `detect_sections` |
| [`concat_columns`](../appjsonify/modules/edit/concat_columns.py#L11) | `concat_columns` concatenates `Paragraph` instances, each of which is in a different column, and forms a new `Paragraph` instance if they met the criteria. | <p>`column_offset`: Specify a threshold value to determine if a paragraph is in a different column from a previous one. Defaults to 300.</p><p>`consider_font_size`: Consider font size in making judgements. Defaults to False.</p> | `load_docs`, `extract_lines`, `extract_paragraphs` |
| [`concat_pages`](../appjsonify/modules/edit/concat_pages.py#L11) | `concat_pages` concatenates `Paragraph` instances in different pages if they meet the conditions. | <p>`consider_font_size`:  Consider font size in making judgements. Defaults to False.</p> | `load_docs`, `extract_lines`, `extract_paragraphs` |


#### Sample usage
The following will list all paragraphs contained in a PDF document with section and subsection information.

```bash
appjsonify /path/to/pdf/dir/or/path /path/to/output/dir \
    --pipeline load_docs extract_lines extract_paragraphs  detect_sections concat_pages dump_formatted_doc \
    --x_tolerance 1.2 \
    --y_tolerance 6.0 \
    --x_offset 10 \
    --consider_font_size \
    --indent_offset 25 \
    --listing_offset 45 \
    --max_headline_len 10 \
    --headline_names Abstract References Limitations Appendix
```


### Removal
| Module name | Description | Parameters | Prerequisites |
| -- | -- | -- | -- |
| [`remove_meta`](../appjsonify/modules/edit/remove_meta.py#L8) | `remove_meta` excludes header and footer `Token` instances from the body. | <p>`header_offset`: A threshold value to determine if an element is a header. Defaults to 80.</p><p>`footer_offset`: A threshold value to determine if an element is a footer. Defaults to 80.</p><p>`left_side_offset`: A threshold value to determine if an element is in a left-hand side margin area. Defaults to 40.</p><p>`right_side_offset`: A threshold value to determine if an element is in a right-hand side margin area. Defaults to 40.</p> | `load_docs` |
| [`remove_lines_by_objects`](../appjsonify/modules/edit/remove_lines_by_objects.py#L9) | `remove_lines_by_objects` removes `Line` instances that can be captions and elements inside figures or tables from the body. | <p>`remove_by_obj`: Set this to remove captions based on bounding box information on objects. Defaults to False.</p><p>`remove_by_line`: Set this to remove captions based on bounding box information on line objects. Defaults to False.</p><p>`remove_by_rect`: Set this to remove captions based on bounding box information on rect objects. Defaults to False.</p><p>`remove_by_curve`: Set this to remove captions based on bounding box information on curve objects. Defaults to False.</p> | `load_docs`, `extract_lines` |
| [`remove_figures_with_ml`](../appjsonify/modules/edit/remove_figures_with_ml.py#L9) | `remove_figures_with_ml` excludes `Line` instances inside figures from the body. | <p>`object_bbox_offset`: Specify a threshold value to determine if a line element is within the margin area of an object. Defaults to 25.</p> | `load_docs`, `load_objects_with_ml`, `extract_lines` |
| [`remove_tables_with_ml`](../appjsonify/modules/edit/remove_figures_with_ml.py#L9) | `remove_tables_with_ml` excludes `Line` instances inside tables from the body. | <p>`object_bbox_offset`: Specify a threshold value to determine if a line element is within the margin area of an object. Defaults to 25.</p> | `load_docs`, `load_objects_with_ml`, `extract_lines` |
| [`remove_equations_with_ml`](../appjsonify/modules/edit/remove_equations_with_ml.py#L9) | `remove_equations_with_ml` removes `Line` instances that must be equations on the basis of the outputs from the ML-based bounding box detectors. | <p>`equation_overlap_threshold`: Specify a threshold value to determine if a line is a equation. Defaults to 0.5.</p> | `load_docs`, `load_objects_with_ml`, `extract_lines` |

#### Sample usage
The following will list all paragraphs contained in a PDF document with section and subsection information, while filtering out non-body contents.

```bash
appjsonify /path/to/pdf/dir/or/path /path/to/output/dir \
    --pipeline load_docs remove_illegal_tokens remove_meta extract_lines extract_footnotes remove_lines_by_objects extract_paragraphs  detect_sections concat_columns concat_pages dump_formatted_doc \
    --x_tolerance 1.2 \
    --header_offset 75 \
    --footer_offset 80 \
    --left_side_offset 40 \
    --right_side_offset 40 \
    --y_tolerance 6.0 \
    --footnote_offset 200 \
    --use_horizontal_lines \
    --object_bbox_offset 25 \
    --remove_by_line \
    --remove_by_curve \
    --x_offset 10 \
    --consider_font_size \
    --indent_offset 25 \
    --listing_offset 45 \
    --max_headline_len 10 \
    --headline_names Abstract References Limitations Appendix
```


## Output related modules
| Module name | Description | Parameters | Prerequisites |
| -- | -- | -- | -- |
| `dump_doc_with_tokens` | `dump_doc_with_tokens` exports all `Token` instances in a PDF document. | <p>`output_dir`: Specify an output directory.</p> | `load_docs` |
| `dump_doc_with_lines` | `dump_doc_with_lines` exports all `Line` instances in a PDF document. | <p>`output_dir`: Specify an output directory.</p> | `load_docs`, `extract_lines` |
| `dump_doc_with_paragraphs` | `dump_doc_with_paragraphs` exports all `Paragraph` instances in a PDF document. | <p>`output_dir`: Specify an output directory.</p> | `load_docs`, `extract_lines`, `extract_paragraphs` |
| `dump_doc_with_sections` | `dump_doc_with_sections` exports all `Paragraph` instances with sections information in a PDF document. | <p>`output_dir`: Specify an output directory.</p> | `load_docs`, `extract_lines`, `extract_paragraphs`, `detect_sections` |
| `dump_formatted_doc` | `dump_formatted_doc` exports all `Paragraph` instances with sections information in a PDF document. This should be used after `concat_pages`. | <p>`output_dir`: Specify an output directory.</p> | `load_docs`, `extract_lines`, `extract_paragraphs`, `detect_sections`, `concat_pages` |
