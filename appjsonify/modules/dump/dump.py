import copy
import json
from pathlib import Path

from tqdm.contrib import tenumerate

from ..doc import Document
from ..runner import BaseRunner


@BaseRunner.register("dump_doc_with_tokens")
class TokenLevelJSONDumper(BaseRunner):
    """Export as a .json file structured with tokens."""
    def _process_by_doc(
        self,
        doc: Document,
        output_dir: Path
    ):      
        # init
        formatted_doc: dict = {
            'doc_name' : doc.meta.get('Title') if doc.meta.get('Title') is not None else doc.input_path.stem,
            'author' : doc.meta.get('Author') if doc.meta.get('Author') is not None else '',
            'creation_date' : doc.meta.get('CreationDate') if doc.meta.get('CreationDate') is not None else '',
            'mod_date' : doc.meta.get('ModDate') if doc.meta.get('ModDate') is not None else '',
            'tables': doc.meta.get('tables') if doc.meta.get('tables') is not None else '',
            'figures': doc.meta.get('figures') if doc.meta.get('figures') is not None else '',
            'footers': doc.meta.get('footers') if doc.meta.get('footers') is not None else '',
            'body': []
        }
        
        # process by page
        for page in doc.pages:
            for token in page.tokens:
                if token.token != "":
                    formatted_doc["body"].append(token.token)
        
        # make a directory if necessary
        output_doc_dir = output_dir / doc.input_path.stem 
        if not output_doc_dir.exists():
            output_doc_dir.mkdir()
            
        # output as a json
        output_path = output_dir / doc.input_path.stem / f'{doc.input_path.stem}_with_tokens.json'
        with open(str(output_path), 'w') as f:
            json.dump(formatted_doc, f, indent=4, ensure_ascii=False)
        return
    
    
    def execute(
        self, 
        documents: list[Document],
        output_dir: str,
        **kwargs: dict
    ) -> list[Document]:
        # init
        self.check_args(self.execute, locals())
        
        # avoid overwrite
        copied_documents = copy.deepcopy(documents)
        for _, doc in tenumerate(copied_documents, total=len(copied_documents)):
            self._process_by_doc(doc, Path(output_dir))
        return copied_documents
    

@BaseRunner.register("dump_doc_with_lines")
class LineLevelJSONDumper(BaseRunner):
    """Export as a .json file structured with lines."""
    def _process_by_doc(
        self,
        doc: Document,
        output_dir: Path
    ):
        # init
        formatted_doc: dict = {
            'doc_name' : doc.meta.get('Title') if doc.meta.get('Title') is not None else doc.input_path.stem,
            'author' : doc.meta.get('Author') if doc.meta.get('Author') is not None else '',
            'creation_date' : doc.meta.get('CreationDate') if doc.meta.get('CreationDate') is not None else '',
            'mod_date' : doc.meta.get('ModDate') if doc.meta.get('ModDate') is not None else '',
            'tables': doc.meta.get('tables') if doc.meta.get('tables') is not None else '',
            'figures': doc.meta.get('figures') if doc.meta.get('figures') is not None else '',
            'footers': doc.meta.get('footers') if doc.meta.get('footers') is not None else '',
            'body': []
        }
        
        # process by page
        for page in doc.pages:
            for line in page.lines:
                if line.line != "":
                    formatted_doc["body"].append(line.line)
        
        # make a directory if necessary
        output_doc_dir = output_dir / doc.input_path.stem 
        if not output_doc_dir.exists():
            output_doc_dir.mkdir()
            
        # output as a json
        output_path = output_dir / doc.input_path.stem / f'{doc.input_path.stem}_with_lines.json'
        with open(str(output_path), 'w') as f:
            json.dump(formatted_doc, f, indent=4, ensure_ascii=False)
        return

    
    def execute(
        self, 
        documents: list[Document],
        output_dir: str,
        **kwargs: dict
    ) -> list[Document]:
        # init
        self.check_args(self.execute, locals())
        
        # avoid overwrite
        copied_documents = copy.deepcopy(documents)
        for _, doc in tenumerate(copied_documents, total=len(copied_documents)):
            self._process_by_doc(doc, Path(output_dir))
        return copied_documents



@BaseRunner.register("dump_doc_with_paragraphs")
class ParagraphLevelJSONDumper(BaseRunner):
    """Export as a .json file structured with paragraphs."""
    def _process_by_doc(
        self,
        doc: Document,
        output_dir: Path
    ):
        # init
        formatted_doc: dict = {
            'doc_name' : doc.meta.get('Title') if doc.meta.get('Title') is not None else doc.input_path.stem,
            'author' : doc.meta.get('Author') if doc.meta.get('Author') is not None else '',
            'creation_date' : doc.meta.get('CreationDate') if doc.meta.get('CreationDate') is not None else '',
            'mod_date' : doc.meta.get('ModDate') if doc.meta.get('ModDate') is not None else '',
            'tables': doc.meta.get('tables') if doc.meta.get('tables') is not None else '',
            'figures': doc.meta.get('figures') if doc.meta.get('figures') is not None else '',
            'footers': doc.meta.get('footers') if doc.meta.get('footers') is not None else '',
            'body': []
        }
        
        # process by page
        for page in doc.pages:
            for paragraph in page.paragraphs:
                if paragraph.paragraph != "":
                    formatted_doc["body"].append(paragraph.paragraph)
        
        # make a directory if necessary
        output_doc_dir = output_dir / doc.input_path.stem 
        if not output_doc_dir.exists():
            output_doc_dir.mkdir()
        
        # output as a json
        output_path = output_dir / doc.input_path.stem / f'{doc.input_path.stem}_with_paragraphs.json'
        with open(str(output_path), 'w') as f:
            json.dump(formatted_doc, f, indent=4, ensure_ascii=False)
        return

    
    def execute(
        self, 
        documents: list[Document],
        output_dir: str,
        **kwargs: dict
    ) -> list[Document]:
        # init
        self.check_args(self.execute, locals())
        
        # avoid overwrite
        copied_documents = copy.deepcopy(documents)
        for _, doc in tenumerate(copied_documents, total=len(copied_documents)):
            self._process_by_doc(doc, Path(output_dir))
        return copied_documents


@BaseRunner.register("dump_doc_with_sections")
class SectionLevelJSONDumper(BaseRunner):
    """Export as a .json file structured with sections."""
    def _process_by_doc(
        self,
        doc: Document,
        output_dir: Path
    ):
        # init
        formatted_doc: dict = {
            'doc_name' : doc.meta.get('Title') if doc.meta.get('Title') is not None else doc.input_path.stem,
            'author' : doc.meta.get('Author') if doc.meta.get('Author') is not None else '',
            'creation_date' : doc.meta.get('CreationDate') if doc.meta.get('CreationDate') is not None else '',
            'mod_date' : doc.meta.get('ModDate') if doc.meta.get('ModDate') is not None else '',
            'tables': doc.meta.get('tables') if doc.meta.get('tables') is not None else '',
            'figures': doc.meta.get('figures') if doc.meta.get('figures') is not None else '',
            'footers': doc.meta.get('footers') if doc.meta.get('footers') is not None else '',
            'body': []
        }
        section_group: dict = {
            "title": "",
            "content": []
        }
        
        # process by page
        for page in doc.pages:
            for paragraph in page.paragraphs:
                # TODO: More sophisticated way of structuring
                if paragraph.meta["style"] in ("title", "section", "subsection"):
                    # register
                    if section_group["title"] != "" or section_group["content"] != []:
                        formatted_doc["body"].append(section_group)
                    # init
                    section_group = {
                        "title": paragraph.paragraph,
                        "content": []
                    }
                else:
                    section_group["content"].append(paragraph.paragraph)
        else:
            if section_group["title"] != "" or section_group["content"] != []:
                formatted_doc["body"].append(section_group)
        
        # make a directory if necessary
        output_doc_dir = output_dir / doc.input_path.stem 
        if not output_doc_dir.exists():
            output_doc_dir.mkdir()
         
        # output as a json
        output_path = output_dir / doc.input_path.stem / f'{doc.input_path.stem}_with_sections.json'
        with open(str(output_path), 'w') as f:
            json.dump(formatted_doc, f, indent=4, ensure_ascii=False)
        return
    
    
    def execute(
        self, 
        documents: list[Document],
        output_dir: str,
        **kwargs: dict
    ) -> list[Document]:
        # init
        self.check_args(self.execute, locals())
        
        # avoid overwrite
        copied_documents = copy.deepcopy(documents)
        
        for _, doc in tenumerate(copied_documents, total=len(copied_documents)):
            self._process_by_doc(doc, Path(output_dir))
        return copied_documents


@BaseRunner.register("dump_formatted_doc")
class FormattedDocJSONDumper(BaseRunner):
    """Export as a .json file structured with sections."""
    def _process_by_doc(
        self,
        doc: Document,
        output_dir: Path
    ):
        # init
        formatted_doc: dict = {
            'doc_name' : doc.meta.get('Title') if doc.meta.get('Title') is not None else doc.input_path.stem,
            'author' : doc.meta.get('Author') if doc.meta.get('Author') is not None else '',
            'creation_date' : doc.meta.get('CreationDate') if doc.meta.get('CreationDate') is not None else '',
            'mod_date' : doc.meta.get('ModDate') if doc.meta.get('ModDate') is not None else '',
            'tables': doc.meta.get('tables') if doc.meta.get('tables') is not None else '',
            'figures': doc.meta.get('figures') if doc.meta.get('figures') is not None else '',
            'footers': doc.meta.get('footers') if doc.meta.get('footers') is not None else '',
            'body': []
        }
        section_group: dict = {
            "title": "",
            "content": []
        }
        
        # process by paragraph
        for paragraph in doc.formatted_paragraphs:
            # TODO: More sophisticated way of structuring
            if paragraph.meta["style"] in ("title", "section", "subsection"):
                # register
                if section_group["title"] != "" or section_group["content"] != []:
                    formatted_doc["body"].append(section_group)
                # inits
                section_group = {
                    "title": paragraph.paragraph,
                    "content": []
                }
            else:
                section_group["content"].append(paragraph.paragraph)
        else:
            if section_group["title"] != "" or section_group["content"] != []:
                formatted_doc["body"].append(section_group)
        
        # make a directory if necessary
        output_doc_dir = output_dir / doc.input_path.stem 
        if not output_doc_dir.exists():
            output_doc_dir.mkdir()
           
        # output as a json
        output_path = output_dir / doc.input_path.stem / f'{doc.input_path.stem}.json'
        with open(str(output_path), 'w') as f:
            json.dump(formatted_doc, f, indent=4, ensure_ascii=False)
        return
    
    
    def execute(
        self, 
        documents: list[Document],
        output_dir: str,
        **kwargs: dict
    ) -> list[Document]:
        # init
        self.check_args(self.execute, locals())
        
        # avoid overwrite
        copied_documents = copy.deepcopy(documents)
        
        for _, doc in tenumerate(copied_documents, total=len(copied_documents)):
            self._process_by_doc(doc, Path(output_dir))
        return copied_documents
