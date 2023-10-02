prerequisites = {
    'load_docs': [],
    'remove_illegal_tokens': ['load_docs'],
    'remove_meta': ['load_docs'],
    'extract_lines': ['load_docs'],
    'extract_footnotes': ['load_docs', 'extract_lines'],
    'remove_lines_by_objects': ['load_docs', 'extract_lines'],
    'extract_paragraphs': ['load_docs', 'extract_lines'],
    'detect_sections': ['load_docs', 'extract_lines', 'extract_paragraphs'],
    'concat_columns': ['load_docs', 'extract_lines', 'extract_paragraphs'],
    'concat_pages': ['load_docs', 'extract_lines', 'extract_paragraphs'],
    'tailor_references': ['load_docs', 'extract_lines', 'extract_paragraphs', 'detect_sections'],
    'dump_doc_with_sections': ['load_docs', 'extract_lines', 'extract_paragraphs', 'detect_sections'],
    'dump_doc_with_paragraphs': ['load_docs', 'extract_lines', 'extract_paragraphs'],
    'dump_doc_with_lines': ['load_docs', 'extract_lines'],
    'dump_doc_with_tokens': ['load_docs'],
    'dump_formatted_doc': ['load_docs', 'extract_lines', 'extract_paragraphs', 'detect_sections', 'concat_pages'],
    'load_objects_with_ml': ['load_docs'],
    'remove_figures_with_ml': ['load_docs', 'load_objects_with_ml', 'extract_lines'],
    'remove_tables_with_ml': ['load_docs', 'load_objects_with_ml', 'extract_lines'],
    'remove_equations_with_ml': ['load_docs', 'load_objects_with_ml', 'extract_lines'],
    'extract_captions_with_ml': ['load_docs', 'load_objects_with_ml', 'extract_lines'],
    'extract_footnotes_with_ml': ['load_docs', 'load_objects_with_ml', 'extract_lines']
}

def check_pipeline(pipeline: list[str]) -> bool:
    completed_modules = set()
    for module in pipeline:
        if module not in prerequisites:
            print(f"Error: Module '{module}' is not a valid module.")
            return False

        unmet_prerequisites = [p for p in prerequisites[module] if p not in completed_modules]
        if unmet_prerequisites:
            print(f"Error: Module '{module}' has unmet prerequisites: {', '.join(unmet_prerequisites)}")
            return False

        completed_modules.add(module)
        
    return True
