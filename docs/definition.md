Document Handling in `appjsonify`
===

[Go back to top](../README.md)

`appjsonify` defines five classes (`Token`, `Line`, `Paragraph`, `Page`, and `Document`) to structure a given document(s).

## [`Token`](../appjsonify/modules/doc.py#L3)
This class holds a token (word) and its position and surface information such as its bounding box coordinates, font size and font name.

### [`__init__`](../appjsonify/modules/doc.py#L5)
#### Inputs
* token (`str`): A token string.
* pos (`tuple[int]`): A tuple of bounding box information ($x_0$, $y_0$, $x_1$, $y_1$). The bounding box values range from 0 to 1000.
* font_size (`float`): Font size obtained using `pdfplumber`.
* font_name (`str`): Font name obtained using `pdfplumber`.
* meta (`dict`): A meta dictionary used to save supplementary information.


## [`Line`](../appjsonify/modules/doc.py#L20)
This class holds a line element, its position and surface information such as its bounding box coordinates, font size and font name, and a list of tokens.
`Line` consists of a list of `Token`, i.e. a line instance must be formed with the corresponding `Token` instances.


### [`__init__`](../appjsonify/modules/doc.py#L22)
#### Inputs
* line (`str`): A line string.
* pos (`tuple[int]`): A tuple of bounding box information ($x_0$, $y_0$, $x_1$, $y_1$). The bounding box values range from 0 to 1000.
* font_size (`float`): Font size obtained using `pdfplumber`.
* font_name (`str`): Font name obtained using `pdfplumber`.
* tokens (`list[Token]`): A list of `Token` instances that form a line.
* meta (`dict`): A meta dictionary used to save supplementary information.


## [`Paragraph`](../appjsonify/modules/doc.py#L39)
This class holds a paragraph element, its position and surface information such as its bounding box coordinates, font size and font name, and a list of lines.
`Paragraph` consists of a list of `Line`, i.e. a paragraph instance must be formed with the corresponding `Line` instances.

### [`__init__`](../appjsonify/modules/doc.py#L41)
#### Inputs
* paragraph (`str`): A paragraph string.
* pos (`tuple[int]`): A tuple of bounding box information ($x_0$, $y_0$, $x_1$, $y_1$). The bounding box values range from 0 to 1000.
* font_size (`float`): Font size obtained using `pdfplumber`.
* font_name (`str`): Font name obtained using `pdfplumber`.
* lines (`list[Line]`): A list of `Line` instances that form a paragraph.
* meta (`dict`): A meta dictionary used to save supplementary information.


## [`Page`](../appjsonify/modules/doc.py#L58)
This class holds lists of `Paragraph`, `Line`, and `Token` instances per PDF page, as well as its meta dictionary.

### [`__init__`](../appjsonify/modules/doc.py#L60)
#### Inputs
* paragraphs (`list[Paragraph]`): A list of `Paragraph` instances that form a `Page`.
* lines (`list[Line]`): A list of `Line` instances that form a `Page`.
* tokens (`list[Token]`): A list of `Token` instances that form a `Page`.
* meta (`dict`): A meta dictionary used to save supplementary information.


## [`Document`](../appjsonify/modules/doc.py#L73)
This class holds the path to an original PDF file, its `Page` instances, formatted `Paragraph` instances, and meta dictionary.
This is the core class used in `BaseRunner`, and every processing module needs to take the list of `Document`: `list[Document]` as its first input parameter and return the processed `list[Document]` in the `execute` method.

### [`__init__`](../appjsonify/modules/doc.py#L75)
#### Inputs
* `input_path` (`Path`): A path to a PDF file.
* `pages` (`list[Page]`): A list of `Page` instances.
* `formatted_paragraphs` (`list[Paragraph]`): A list of `Paragraph` instances.
* `meta` (`dict`): A meta dictionary used to save supplementary information such as footers and captions.

