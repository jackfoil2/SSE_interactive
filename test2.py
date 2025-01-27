##Imported Libraries 
import pdfplumber
import re
from bs4 import BeautifulSoup
import os

########## ablle to extract the enitre table from the PDF (assuming only given the table (will update this later maybe))
def extract_table_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        table = []
        for page in pdf.pages:
            rows = page.extract_table()
            if rows:
                for row in rows:
                    # Convert all elements to strings and add to the table
                    row = [str(cell) if cell else '' for cell in row]
                    table.append(row)
    return table

##filters the Headers from the table 
def filter_header(table, filter_sequence):
    filtered_table = []
    for row in table:
        if row != filter_sequence:  # Exclude rows matching the filter sequence
            filtered_table.append(row)
    return filtered_table

##Now combines the empty Rows 
def combine_rows(table):
    combined_table = []
    for row in table:
        if row[0] == '':  # Check if the first element is empty
            # Append the content of this row to the previous row
            if combined_table:
                combined_table[-1] = [
                    combined_table[-1][i] + row[i] for i in range(len(row))
                ]
        else:
            combined_table.append(row)
    return combined_table

### select the tables depending on the user inputs
def select_tables(table, prefix):
    selected_table = []
    has_seen = False
    for row in table:
        first_element = row[0]
        if first_element.startswith(prefix):
            selected_table.append(row)
            has_seen = True 
        elif not first_element.startswith(prefix) and has_seen == True:
            break  # Stop if the prefix changes
    return selected_table

###Now making the HTMLS 
def generate_html_from_table(table):
    if not table or not table[0] or not table[0][0]:
        raise ValueError("The table is empty or does not contain a valid first row to determine the file name.")

    # Use the first element of the first row as the file name
    output_filename = f"{table[0][0].replace(' ', '_').replace('/', '_')}.html"

    # Ensure the 'templates' directory exists
    output_directory = "templates"
    os.makedirs(output_directory, exist_ok=True)

    # Full path to save the file
    output_path = os.path.join(output_directory, output_filename)

    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>PDF Table to HTML</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 20px;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 20px;
            }
            th, td {
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
                vertical-align: top;
            }
            th {
                background-color: #f4f4f4;
            }
        </style>
    </head>
    <body>
        <h1>Extracted Table from PDF</h1>
        <table>
            <tr>
                <th>WBS</th>
                <th>Activity</th>
                <th>Description</th>
                <th>Artifact</th>
                <th>OPR/Supplier</th>
                <th>References</th>
            </tr>
    """

    for row in table:
        html_content += "<tr>"
        for cell in row:
            html_content += f"<td>{cell if cell else ''}</td>"
        html_content += "</tr>"

    html_content += """
        </table>
    </body>
    </html>
    """

    # Write HTML content to the file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"HTML file has been created: {output_filename}")


############################################### MAIN ############################################
file_path = "SEEGuidebook_WBS.pdf"
table = extract_table_from_pdf(file_path)

##gets rid of the header
filter_sequence = ['WBS', 'Activity', 'Description', 'Artifact', 'OPR/ Supplier', 'References']
filtered_table = filter_header(table, filter_sequence)

##Combines empty rows
combined_table = combine_rows(filtered_table)


sections = [1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 2.1, 2.2, 2.3, 2.4, 3.1, 4.1, 4.2, 4.3, 4.4, 4.5, 5.1, 5.2, 5.3, 6.1, 6.2, 6.3, 6.4]
# Iterate through all sections
for section in sections:
    print(f"Processing section: {section}")
    
    # Filters based on parameters for the current section
    selected_rows = select_tables(combined_table, str(section))
    
    # Try generating HTML for the selected table
    try:
        generate_html_from_table(selected_rows)
        print(f"HTML successfully generated for section {section}")
    except ValueError as e:
        print(f"Error generating HTML for section {section}: {e}")
