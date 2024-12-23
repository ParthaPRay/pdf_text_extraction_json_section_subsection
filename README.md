# pdf_text_extraction_json_section_subsection
This repo contains codes for extraction of PDF text to JSON to show section number, section title, section body content, footnote

# Document type
Legal

# Types 

3 Types

Thank you for providing the detailed sample of the **Type 2 PDF**. Based on your input, it's clear that the initial **Type 2 parser** needs enhancements to accurately capture the hierarchical structure of sections, chapters, and articles within the PDF. Below is the revised approach to handle **Type 2 PDFs** effectively.

## Revised Approach for Type 2 PDF Parsing

### Type 1

Certainly! Based on the provided sample of the **Type 1 PDF**, here's a clear understanding of its structure and key components:

## **Type 1 PDF Structure Overview**

### **1. Document Hierarchy**

The **Type 1 PDF** follows a hierarchical structure that organizes the legal document into **Chapters**, **Articles**, and **Footnotes**. Here's how each level is structured:

- **Chapters**
  - **Designation**: Each chapter is introduced with the keyword "Chapter" followed by a Roman numeral (e.g., "Chapter I").
  - **Title**: The chapter title follows the chapter number (e.g., "General provisions").
  
- **Articles**
  - **Designation**: Within each chapter, individual sections are designated as "Article" followed by an Arabic numeral (e.g., "Article 1").
  - **Title**: Each article has a specific title that summarizes its content.
  - **Body Content**: The main text of the article provides detailed provisions, regulations, or descriptions relevant to the title.
  
- **Footnotes**
  - **Designation**: Footnotes are introduced with the keyword "Footnote." and provide additional information, amendments, or references related to the preceding article.
  - **Content**: They often include references to laws, dates, or specific amendments that affect the article's provisions.

### **2. Detailed Structure Breakdown**

Here's a more granular look at the structure based on the sample:

#### **a. Chapter Level**

- **Example**:
  ```
  Chapter I General provisions Article
  ```
  
- **Components**:
  - **Chapter Number**: "Chapter I"
  - **Chapter Title**: "General provisions"
  
#### **b. Article Level**

- **Example**:
  ```
  Article 1. Civil legal proceedings legislation of the Republic of Kazakhstan
  1. The procedure of legal proceedings in civil cases...
  2. International contractual and other obligations...
  ```
  
- **Components**:
  - **Article Number**: "Article 1"
  - **Article Title**: "Civil legal proceedings legislation of the Republic of Kazakhstan"
  - **Article Body**: Numbered paragraphs detailing specific provisions.

#### **c. Footnote Level**

- **Example**:
  ```
  Footnote. Article 1 as amended by the Law of the Republic of Kazakhstan dated...
  ```
  
- **Components**:
  - **Footnote Identifier**: "Footnote."
  - **Footnote Content**: Details about amendments, enforcement dates, or references to other laws.


### Type 2
From your sample, the **Type 2 PDF** follows this hierarchical structure:

- **Section**: Denoted by `SECTION n. TITLE`
  - **Chapter**: Denoted by `Chapter n. TITLE`
    - **Article**: Denoted by `Article n. TITLE`
      - **Content**: Numbered paragraphs (e.g., `1. Some text`)
      - **Footnotes**: Denoted by `Footnote. ...`


### 4. Integrating the Revised Parser

Update the `process_pdf` function to use the revised Type 2 parser.

```python
def process_pdf_revised(pdf_path, pdf_type):
    text = extract_text_from_pdf(pdf_path)
    if pdf_type == 1:
        parsed_data = parse_type1(text)
    elif pdf_type == 2:
        parsed_data = parse_type2_revised(text)
    elif pdf_type == 3:
        parsed_data = parse_type3(text)
    else:
        raise ValueError("Unsupported PDF type")
    
    json_output = convert_to_json(parsed_data)
    return json_output
```


## Example Usage

User must provide the pdf as below

```python
pdf_path = "example-2.pdf"  # Chane the PDF as per the type 1 or 2 or 3
```
then the type of pdf such as 1, 2, 3

```python
pdf_type = 2
```

### Result

The result dirctory contains the json files for three example pdf 1, 2, 3 for correspodning output.


## Licensing

This project is dual-licensed:

1. **Non-Commercial Use**:
   - Free for personal, educational, and non-commercial use under the terms outlined in the [LICENSE](LICENSE) file.

2. **Commercial Use**:
   - Requires a paid license. Contact Partha Pratim Ray at [parthapratimray1986@gmail.com](mailto:parthapratimray1986@gmail.com) for more information.

## Contact
For any licensing inquiries, please email [parthapratimray1986@gmail.com](mailto:parthapratimray1986@gmail.com).
