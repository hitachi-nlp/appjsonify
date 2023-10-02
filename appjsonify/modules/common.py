from collections import Counter

from .doc import Document


def normalize_bbox(
    bbox: list[float], 
    width: int, 
    height: int
) -> tuple[int]:
    """Normalise a bounding box

    Args:
        bbox (list[float]): A bounding box.
        width (int): A page width.
        height (int): A page height.

    Returns:
        tuple[int]: A normalised bounding box.
    """
    normalised_x0 = min(1000, max(0, int(bbox[0] / width * 1000)))
    normalised_y0 = min(1000, max(0, int(bbox[1] / height * 1000)))
    normalised_x1 = min(1000, max(0, int(bbox[2] / width * 1000)))
    normalised_y1 = min(1000, max(0, int(bbox[3] / height * 1000)))
    return (normalised_x0, normalised_y0, normalised_x1, normalised_y1)


def judge_within_bbox(
    ref_bbox: tuple[int], 
    target_bbox: tuple[int]
) -> bool:
    """Classify if `target_bbox` is inside `ref_bbox`."""
    # check x axis
    # cond: ref_x0 <= target_x0 <= target_x1 <= ref_x1
    if ref_bbox[0] <= target_bbox[0] and target_bbox[2] <= ref_bbox[2]:
        # check y axis
        # cond: ref_y0 <= target_y0 <= target_y1 <= ref_y1
        if ref_bbox[1] <= target_bbox[1] and target_bbox[3] <= ref_bbox[3]:
            return True
    return False


def check_token_overlap(
    ref_bbox: tuple[int], 
    target_bbox: tuple[int],
    threshold: float = 0.95, 
    bbox_overlap_metric: str = 'min'
) -> bool:
    """Judge if two bboxes overlap significantly.

    Args:
        ref_bbox (tuple[int]): A reference bbox.
        target_bbox (tuple[int]): A target bbox.
        threshold (float, optional): A threshold to determin if two bboxes overlap significantly. 
        Defaults to 0.95.
        bbox_overlap_metric (str, optional): Specify a metric to calculate the overlap ratio. Defaults to 'min'.

    Raises:
        ValueError: Not defined overlap metric.

    Returns:
        bool: Returns True if two bboxes overlap significantly.
    """
    # get and (intersection) bbox
    and_x0 = max(ref_bbox[0], target_bbox[0])
    and_x1 = min(ref_bbox[2], target_bbox[2])
    and_y0 = max(ref_bbox[1], target_bbox[1])
    and_y1 = min(ref_bbox[3], target_bbox[3])
    
    # no overlap
    if and_x0 > and_x1 or and_y0 > and_y1:
        return False
    
    # calc overlap ratio
    and_area = abs(and_x1 - and_x0) * abs(and_y1 - and_y0)
    if bbox_overlap_metric == 'min':
        ref_area = abs(ref_bbox[2] - ref_bbox[0]) * abs(ref_bbox[3] - ref_bbox[1])
        target_area = abs(target_bbox[2] - target_bbox[0]) * abs(target_bbox[3] - target_bbox[1])
        overlap_ratio = and_area / float(min(ref_area, target_area))
    elif bbox_overlap_metric == 'union':
        # union area
        union_x0 = min(ref_bbox[0], target_bbox[0])
        union_x1 = max(ref_bbox[2], target_bbox[2])
        union_y0 = min(ref_bbox[1], target_bbox[1])
        union_y1 = max(ref_bbox[3], target_bbox[3])
        union_area = abs(union_x1 - union_x0) * abs(union_y1 - union_y0)
        overlap_ratio = and_area / float(union_area)
    else:
        raise ValueError('No such a `bbox_overlap_metric`!')
    
    if overlap_ratio > threshold:
        return True
    else:
        return False


def get_math_font_names(
    paper_type: str
) -> tuple[str]:
    """Return a tuple of regex math font names.

    Args:
        paper_type (str): A paper type.

    Raises:
        ValueError: Raises this error if a given `paper_type` does not exist.

    Returns:
        tuple[str]: A tuple of regex math font names used.
    """
    if paper_type in ("ACL", "ACL2"):
        return (
            r"CMMIB[0-9]+", 
            r"CMMI[0-9]+",
            r"CMSY[0-9]+",
            r"CMR[0-9]+",
            r"CMEX[0-9]+",
            r"MSBM[0-9]+",
            r"CMBX[0-9]+"
        )
    elif paper_type in ("AAAI", "AAAI2"):
        return (
            r"CMMIB[0-9]+", 
            r"CMMI[0-9]+",
            r"CMSY[0-9]+",
            r"CMR[0-9]+",
            r"CMEX[0-9]+",
            r"MSBM[0-9]+",
            r"CMBX[0-9]+"
        )
    elif paper_type in ("Springer", "Springer2"):
        return (
            r"CMMI[0-9]+"
        )
    elif paper_type in ("IEEE", "IEEE2"):
        return (
            r"CMMIB[0-9]+",
            r"CMMI[0-9]+",
            r"CMR[0-9]+",
            r"CMEX[0-9]+",
            r"CMSY[0-9]+",
            r"MSBM[0-9]+",
            r"CMBX[0-9]+"
        )
    elif paper_type in ("ACM", "ACM2"):
        return (
            r"txsys",
            r"txexs",
            r"LibertineMathMI[0-9]+",
            r"CMMIB[0-9]+",
            r"CMMI[0-9]+",
            r"CMR[0-9]+",
            r"CMEX[0-9]+",
            r"CMSY[0-9]+",
            r"MSBM[0-9]+",
            r"CMBX[0-9]+"
        )
    elif paper_type in ("ICML", "ICML2"):
        return (
            r"CMMIB[0-9]+",
            r"CMMI[0-9]+",
            r"CMR[0-9]+",
            r"CMEX[0-9]+",
            r"CMSY[0-9]+",
            r"MSBM[0-9]+",
            r"CMBX[0-9]+"
        )
    elif paper_type in ("ICLR", "ICLR2"):
        return (
            r"CMMIB[0-9]+",
            r"CMMI[0-9]+",
            r"CMR[0-9]+",
            r"CMEX[0-9]+",
            r"CMSY[0-9]+",
            r"MSBM[0-9]+",
            r"CMBX[0-9]+"
        )
    elif paper_type in ("NeurIPS", "NeurIPS2"):
        return (
            r"CMMIB[0-9]+",
            r"CMMI[0-9]+",
            r"CMR[0-9]+",
            r"CMEX[0-9]+",
            r"CMSY[0-9]+",
            r"MSBM[0-9]+",
            r"CMBX[0-9]+"
        )
    else:
        raise ValueError("No such a paper_type!")


def get_font_specs_config(
    paper_type: str
) -> dict[tuple[float, str], str]:
    """Return a dict of font configs.

    Args:
        paper_type (str): A paper type.

    Raises:
        NotImplementedError: Throws an error when `paper_type` is not registered.

    Returns:
        dict[tuple[float, str], str]: A dict of font configs.
    """
    if paper_type in ("ACL", "ACL2"):
        return {
            (14.3, "NimbusRomNo9L-Medi"): "title",
            (12.0, "NimbusRomNo9L-Medi"): "section",
            (10.9, "NimbusRomNo9L-Medi"): "subsection",
            (10.9, "NimbusRomNo9L-Regu"): "body",
            (10.0, "NimbusRomNo9L-Regu"): "abstract|references",
            (9.0, "NimbusRomNo9L-Regu"): "footnote",
            (9.0, "Inconsolatazi4-Regular"): "footnote"
        }
    elif paper_type in ("AAAI", "AAAI2"):
        # TODO: Add subsubsection
        return {
            (14.3, "NimbusRomNo9L-Medi"): "title",
            (12.0, "NimbusRomNo9L-Medi"): "section",
            (10.9, "NimbusRomNo9L-Medi"): "subsection",
            (10.0, "NimbusRomNo9L-Medi"): "section", # abstract
            (10.0, "NimbusRomNo9L-Regu"): "body",
            (9.0, "NimbusRomNo9L-Regu"): "abstract|references|footnote"
        }
    elif paper_type in ("ICML", "ICML2"):
        return {
            (14.3, "NimbusRomNo9L-Medi"): "title",
            (12.0, "NimbusRomNo9L-Medi"): "section",
            (10.0, "NimbusRomNo9L-Medi"): "subsection",
            (10.0, "NimbusRomNo9L-Regu"): "body",
            (9.0, "NimbusRomNo9L-Regu"): "footnote",
            (10.0, "NimbusMonL-Regu"): "url"
        }
    elif paper_type in ("ICLR", "ICLR2"):
        # removed body due to sharing the same font specs between subsection and body.
        return {
            (17.2, "NimbusRomNo9L-Regu"): "title", # captilized
            (13.8, "NimbusRomNo9L-Regu"): "title",
            (12.0, "NimbusRomNo9L-Regu"): "section",
            (9.6, "NimbusRomNo9L-Regu"): "section",
            (9.0, "NimbusRomNo9L-Regu"): "footnote",
            (9.0, "NimbusMonL-Regu"): "url"
        }
    elif paper_type in ("NeurIPS", "NeurIPS2"):
        return {
            (17.2, "NimbusRomNo9L-Medi"): "title",
            (12.0, "NimbusRomNo9L-Medi"): "section",
            (10.0, "NimbusRomNo9L-Medi"): "subsection",
            (10.0, "NimbusRomNo9L-Regu"): "body",
            (9.0, "NimbusRomNo9L-Regu"): "footnote",
            (9.0, "SFTT0900"): "url"
        }
    elif paper_type in ("Springer", "Springer2"):
        # TODO: Add subsubsection
        return {
            (14.3, "CMBX12"): "title",
            (12.0, "CMBX12"): "section",
            (10.0, "CMBX10"): "subsection",
            (10.0, "CMR10"): "body",
            (9.0, "CMBX9"): "section", # abstract
            (9.0, "CMR9"): "abstract|references|footnote"
        }
    elif paper_type in ("IEEE", "IEEE2"):
        # removed body due to sharing the same font specs between subsection and body.
        return {
            (23.9, "NimbusRomNo9L-Regu"): "title",
            (9.0, "NimbusRomNo9L-Medi"): "abstract",
            (6.4, "NimbusRomNo9L-Regu"): "caption"
        }
    elif paper_type in ("ACM", "ACM2"):
        return {
            (14.3, "LinBiolinumTB"): "title",
            (10.0, "LinBiolinumTB"): "section",
            (10.0, "LinLibertineT"): "body",
            (9.0, "LinLibertineT"): "abstract",
            (8.0, "LinLibertineT"): "footnote|references"
        }
    else:
        raise NotImplementedError()


def get_most_common_font_size(doc: Document) -> float:
    """Return the most common font size for a given document."""
    font_sizes: list[float] = []
    for page in doc.pages:
        for token in page.tokens:
            font_sizes.append(token.font_size)
    return Counter(font_sizes).most_common(1)[0][0]


def get_most_common_font_name(doc: Document) -> str:
    """Return the most common font name for a given document."""
    font_names: list[str] = []
    for page in doc.pages:
        for token in page.tokens:
            try:
                font_names.append(token.font_name.split('+')[1])
            except IndexError:
                font_names.append(token.font_name)
    return Counter(font_names).most_common(1)[0][0]
