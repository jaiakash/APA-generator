import PyPDF2
import re

# Load the PDF document
pdf_file = open('All references in APA style.pdf', 'rb')
pdf_reader = PyPDF2.PdfReader(pdf_file)

# Extract the text from the PDF document
text = ''
for page_num in range(len(pdf_reader.pages)):
    page = pdf_reader.pages[page_num]
    text += page.extract_text()

# Identify the citations in the text using regular expressions
regex_pattern = r'([A-Za-z]+(?:, [A-Za-z]+)*(?: et al.)? \(\d{4}\)(?:, \d+)?)+'
citations = re.findall(regex_pattern, text)

# Sort the citations alphabetically by the author's last name
sorted_citations = sorted(citations, key=lambda x: x.rsplit(', ', 1)[0].lower())

# Create a dictionary to store the formatted references
references = {}

print(sorted_citations)

# Iterate through the citations and extract the necessary information to create the reference
for citation in sorted_citations:
    parts = citation.split(', ')
    authors = parts[0]
    year = re.search(r'\d{4}', citation).group()
    title = re.search(r'"?(.*?)"?', citation).group(1)
    journal = re.search(r'([A-Z][a-z]*)(?:,?\s+\d+)?\s+\(\d{4}[a-z]?\)', citation).group(1)
    volume = re.search(r'\d+\((\d+)\)', citation).group(1)
    pages = re.search(r':(\d+-\d+)', citation).group(1)
    doi = re.search(r'(doi:\S+)', citation, re.IGNORECASE)
    doi_str = f" doi:{doi.group(1)}." if doi else ""
    # Format the author names
    author_list = authors.split(', ')
    if len(author_list) == 1:
        author_str = author_list[0]
    elif len(author_list) == 2:
        author_str = ' & '.join(author_list)
    else:
        author_str = ', '.join(author_list[:-1]) + ', & ' + author_list[-1]
    # Create the reference string
    reference = f"{author_str} ({year}). {title}. {journal}, {volume}, {pages}.{doi_str}"
    references[citation] = reference

# Print the formatted references
for citation, reference in references.items():
    print(f"{citation}: {reference}")
