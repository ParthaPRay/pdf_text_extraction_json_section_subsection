import fitz  # PyMuPDF

"""
PDF Extraction with PyMuPDF
Using PyMuPDF allows for efficient extraction of text 
while maintaining layout information.
"""

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text("text")
        full_text += text + "\n"
    return full_text


##############
"""
Define Regular Expressions for Different PDF Types
Regular expressions (regex) will help identify patterns corresponding 
to sections, articles, and footnotes.
"""
import re

# Patterns for Type 1 PDF
type1_chapter_pattern = re.compile(r'^Chapter\s+([IVXLC]+)\s+(.+)$', re.MULTILINE)
type1_article_pattern = re.compile(r'^Article\s+(\d+)\.\s+(.+)$', re.MULTILINE)

# Patterns for Type 2 PDF
import re

# Updated Patterns for Type 2 PDF
type2_section_pattern = re.compile(r'^SECTION\s+(\d+)\.\s+(.+)$', re.MULTILINE | re.IGNORECASE)
type2_chapter_pattern = re.compile(r'^Chapter\s+(\d+)\.\s+(.+)$', re.MULTILINE)
type2_article_pattern = re.compile(r'^Article\s+(\d+)\.\s+(.+)$', re.MULTILINE)
footnote_pattern = re.compile(r'^Footnote\.\s+(.+)$', re.MULTILINE | re.IGNORECASE)

# Patterns for Type 3 PDF
type3_chapter_pattern = re.compile(r'^([IVXLC]+)\.\s+(.+)$', re.MULTILINE)
type3_subsection_pattern = re.compile(r'^(\d+(\.\d+)*)\.\s+(.+)$', re.MULTILINE)

# Footnote pattern (assuming footnotes are marked with superscript numbers)
footnote_pattern = re.compile(r'\[\d+\]')  # Adjust based on actual footnote markers


############
"""
Type 1 PDF parsing
"""
def parse_type1(text):
    data = []
    chapters = type1_chapter_pattern.split(text)
    # The split will create a list like ['', chapter_num, chapter_title, rest, ...]
    for i in range(1, len(chapters), 3):
        chapter_num = chapters[i]
        chapter_title = chapters[i+1].strip()
        chapter_content = chapters[i+2].strip()
        
        # Extract articles within the chapter
        articles = type1_article_pattern.split(chapter_content)
        chapter_dict = {
            "chapter_number": chapter_num,
            "chapter_title": chapter_title,
            "articles": []
        }
        for j in range(1, len(articles), 3):
            article_num = articles[j]
            article_title = articles[j+1].strip()
            article_body = articles[j+2].strip()
            chapter_dict["articles"].append({
                "article_number": article_num,
                "article_title": article_title,
                "article_body": article_body,
                "footnotes": extract_footnotes(article_body)
            })
        data.append(chapter_dict)
    return data


##########
"""
Type 2 PDF parsing
"""
def parse_type2_revised(text):
    data = []
    sections = type2_section_pattern.split(text)
    # The split creates a list like ['', section_num, section_title, rest, ...]
    for i in range(1, len(sections), 3):
        section_num = sections[i]
        section_title = sections[i+1].strip()
        section_content = sections[i+2].strip()
        
        # Initialize section dictionary
        section_dict = {
            "section_number": section_num,
            "section_title": section_title,
            "chapters": []
        }
        
        # Split into chapters
        chapters = type2_chapter_pattern.split(section_content)
        # The split creates a list like ['', chapter_num, chapter_title, rest, ...]
        for j in range(1, len(chapters), 3):
            chapter_num = chapters[j]
            chapter_title = chapters[j+1].strip()
            chapter_content = chapters[j+2].strip()
            
            # Initialize chapter dictionary
            chapter_dict = {
                "chapter_number": chapter_num,
                "chapter_title": chapter_title,
                "articles": []
            }
            
            # Split into articles
            articles = type2_article_pattern.split(chapter_content)
            # The split creates a list like ['', article_num, article_title, rest, ...]
            for k in range(1, len(articles), 3):
                article_num = articles[k]
                article_title = articles[k+1].strip()
                article_body = articles[k+2].strip()
                
                # Extract footnotes from article_body
                footnotes = footnote_pattern.findall(article_body)
                # Remove footnotes from article_body
                article_body_clean = footnote_pattern.sub('', article_body).strip()
                
                # Initialize article dictionary
                article_dict = {
                    "article_number": article_num,
                    "article_title": article_title,
                    "article_body": article_body_clean,
                    "footnotes": footnotes
                }
                
                # Append article to chapter
                chapter_dict["articles"].append(article_dict)
            
            # Append chapter to section
            section_dict["chapters"].append(chapter_dict)
        
        # Append section to data
        data.append(section_dict)
    
    return data

##########
"""
Type 3 PDF parsing
"""
def parse_type3(text):
    data = []
    lines = text.split('\n')
    current_chapter = None
    current_section = None
    current_subsection = None

    for line in lines:
        chapter_match = type3_chapter_pattern.match(line)
        if chapter_match:
            if current_chapter:
                data.append(current_chapter)
            current_chapter = {
                "chapter_number": chapter_match.group(1),
                "chapter_title": chapter_match.group(2).strip(),
                "sections": []
            }
            continue

        subsection_match = type3_subsection_pattern.match(line)
        if subsection_match:
            num = subsection_match.group(1)
            title = subsection_match.group(3).strip()
            levels = num.split('.')
            if len(levels) == 1:
                # New section
                current_section = {
                    "section_number": num,
                    "section_title": title,
                    "subsections": []
                }
                if current_chapter:
                    current_chapter["sections"].append(current_section)
            else:
                # Subsection or deeper
                if current_section:
                    current_section["subsections"].append({
                        "subsection_number": num,
                        "subsection_title": title,
                        "subsubsections": []  # Extend as needed
                    })
            continue

        # Assuming remaining lines are body content
        if current_subsection:
            current_subsection["content"] += f" {line.strip()}"
        elif current_section:
            current_section.setdefault("content", "")
            current_section["content"] += f" {line.strip()}"
        elif current_chapter:
            current_chapter.setdefault("content", "")
            current_chapter["content"] += f" {line.strip()}"

    if current_chapter:
        data.append(current_chapter)

    # Post-processing to extract footnotes
    for chapter in data:
        for section in chapter.get("sections", []):
            if "content" in section:
                section["footnotes"] = extract_footnotes(section["content"])
            for subsection in section.get("subsections", []):
                if "content" in subsection:
                    subsection["footnotes"] = extract_footnotes(subsection["content"])
    return data


###########
"""
Footnote Extraction
Assuming footnotes are denoted by markers like [1], [2], etc., 
you can extract them using the defined footnote_pattern.
"""
def extract_footnotes(text):
    footnotes = footnote_pattern.findall(text)
    return footnotes

###############
"""
JSON Structuring
After parsing, structure the extracted data into a JSON format.
"""

import json

def convert_to_json(parsed_data):
    return json.dumps(parsed_data, indent=4, ensure_ascii=False)

#############
"""
Putting It All Together
Create a main function to handle different PDF types.
"""
def process_pdf(pdf_path, pdf_type):
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


##########
"""
 If the PDF type is not known beforehand, implement a detection mechanism 
 based on specific patterns in the text.
"""
# def detect_pdf_type(text):
#     if type1_chapter_pattern.search(text):
#         return 1
#     elif type2_section_pattern.search(text):
#         return 2
#     elif type3_chapter_pattern.search(text):
#         return 3
#     else:
#         return None



##############
if __name__ == "__main__":
    pdf_path = "example-2.pdf"  # Chane the PDF as per the type 1 or 2 or 3
    pdf_type = 2  # Change to 1 or 2 or 3 based on the PDF structure
    json_result = process_pdf(pdf_path, pdf_type)
    
    with open("output.json", "w", encoding="utf-8") as f:
        f.write(json_result)
    
    print("JSON extraction complete. Check output.json.")

