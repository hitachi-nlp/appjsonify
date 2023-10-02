from pathlib import Path

from ..modules.doc import Document


def _make_data_formatted(
    doc: Document,
    show_pos: bool = False, 
    show_font: bool = False,
    show_style: bool = False,
    show_meta: bool = False
) -> str:
    texts: str = ""
    texts += '\n'.join([
        paragraph.paragraph
        + (('\t' + str(paragraph.pos)) 
            if show_pos is True else '')
        + (('\tfont: [' + str(paragraph.font_size) + ' ' + paragraph.font_name + ']')
            if show_font is True else '')
        + (('\tstyle: ' + paragraph.meta["style"]) 
            if show_style is True and paragraph.meta.get("style") is not None else '')
        for paragraph in doc.formatted_paragraphs
    ])
    if show_meta:
        for page in doc.pages:
            texts += '\n'
            for obj_name in ("images", "curves", "rects", "lines"):
                for obj in page.meta.get(obj_name):
                    texts += obj.token + (('\t' + str(obj.pos)) if show_pos is True else '') + '\n'
            if page.meta.get("footnotes") is not None:
                for footnote in page.meta.get("footnotes"):
                    texts += footnote.line + (('\t' + str(footnote.pos)) if show_pos is True else '') \
                            + (('\tfont: [' + str(footnote.font_size) + ' ' + footnote.font_name + ']')
                                if show_font is True else '') + '\n'
    return texts


def _make_data(
    doc: Document,
    insert_page_break: bool = False, 
    show_pos: bool = False, 
    show_font: bool = False,
    show_style: bool = False,
    show_meta: bool = False
) -> str:
    texts: str = ""
    for page in doc.pages:
        if page.paragraphs is not None:
            texts += '\n'.join([
                paragraph.paragraph
                + (('\t' + str(paragraph.pos)) 
                    if show_pos is True else '')
                + (('\tfont: [' + str(paragraph.font_size) + ' ' + paragraph.font_name + ']')
                    if show_font is True else '')
                + (('\tstyle: ' + paragraph.meta["style"]) 
                    if show_style is True and paragraph.meta.get("style") is not None else '')
                for paragraph in page.paragraphs
            ])
        elif page.lines is not None:
            texts += '\n'.join([
                line.line
                + (('\t' + str(line.pos)) 
                    if show_pos is True else '')
                + (('\tfont: [' + str(line.font_size) + ' ' + line.font_name + ']')
                    if show_font is True else '')
                for line in page.lines
            ])
        else:
            texts += '\n'.join([
                token.token
                + (('\t' + str(token.pos)) 
                    if show_pos is True else '')
                + (('\tfont: [' + str(token.font_size) + ' ' + token.font_name + ']')
                    if show_font is True else '')
                for token in page.tokens
            ])
        if show_meta:
            texts += '\n\n\n'
            for obj_name in ("images", "curves", "rects", "lines"):
                for obj in page.meta.get(obj_name):
                    texts += obj.token + (('\t' + str(obj.pos)) if show_pos is True else '') + '\n'
            if page.meta.get("footnotes") is not None:
                for footnote in page.meta.get("footnotes"):
                    texts += '[FOOTNOTE]' +  footnote.line + (('\t' + str(footnote.pos)) if show_pos is True else '') \
                            + (('\tfont: [' + str(footnote.font_size) + ' ' + footnote.font_name + ']')
                                if show_font is True else '') + '\n'
            if page.meta.get("captions") is not None:
                for caption in page.meta.get("captions"):
                    caption_str = ' '.join([token.token 
                                            for token in caption.meta["tokens"]])
                    texts += '[CAPTION] ' + caption_str +  (('\t' + str(caption.pos)) if show_pos is True else '') + '\n'
            if page.meta.get("line_footers") is not None:
                for footer in page.meta.get("line_footers"):
                    footer_str = ' '.join([line.line for line in footer])
                    texts += '[FOOTER] ' + footer_str + '\n'
            if page.meta.get("tables") is not None:
                for table in page.meta.get("tables"):
                    texts += table.token + (('\t' + str(table.pos)) if show_pos is True else '') + '\n'
            if page.meta.get("figures") is not None:
                for figure in page.meta.get("figures"):
                    texts += figure.token + (('\t' + str(figure.pos)) if show_pos is True else '') + '\n'
        if insert_page_break:
            texts += '\n==========\n'
    return texts


def print_data(
    documents: list[Document], 
    output_dir: Path, 
    module_name: str,
    insert_page_break: bool = False, 
    show_pos: bool = False, 
    show_font: bool = False,
    show_style: bool = False,
    show_meta: bool = False
):
    for doc in documents:
        # make a directory if necessary
        output_doc_dir = output_dir / doc.input_path.stem 
        if not output_doc_dir.exists():
            output_doc_dir.mkdir()
        
        # gather necessary information
        texts: str = ""
        if doc.formatted_paragraphs != []:
            texts += _make_data_formatted(
                doc, 
                show_pos, 
                show_font, 
                show_style,
                show_meta
            )
        else:
            texts += _make_data(
                doc, 
                insert_page_break, 
                show_pos, 
                show_font, 
                show_style,
                show_meta
            )
        
        # output as a txt
        output_path = output_dir / doc.input_path.stem / (module_name + '.txt')
        output_path.write_text(texts)
