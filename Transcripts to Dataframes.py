import pdfplumber
import pandas as pd
import os

# Specify the subfolder name defined above
subfolder_name = "Transcripts"

# Construct the full path for the subfolder
subfolder_path = os.path.join(os.getcwd(), subfolder_name)

# Initialize an empty list to store extracted data
data = []

# Loop through PDF files within the subfolder
for filename in os.listdir(subfolder_path):
    if filename.endswith('.pdf'):
        pdf_file = os.path.join(subfolder_path, filename)

        # Initialize variables for tracking the current speaker and their text
        current_speaker = None
        current_text = []

        # Open the current PDF file using pdfplumber
        with pdfplumber.open(pdf_file) as pdf:

            # Iterate through pages in the PDF
            for page in pdf.pages:

                # Extract text from the page
                page_text = page.extract_text()

                # Split the text into lines
                lines = page_text.split('\n')

                # Loop through each line
                for line in lines:
                    line = line.strip()

                    # Check if the line is not empty
                    if line:
                        # Check if the line contains the name of a speaker followed by a colon
                        if any(name in line for name in ["Justin:", "Travis:", "Griffin:"]):
                            if current_speaker:
                                # If there's a current speaker, add the previous text to the data
                                data.append({'Speaker': current_speaker, 'Text': '\n'.join(current_text)})
                                current_text = []  # Reset the current text
                            current_speaker, text = line.split(':', 1)
                            current_speaker = current_speaker.strip()
                            current_text.append(text.strip())
                        elif current_speaker:
                            # Append the line to the current text for the current speaker
                            current_text.append(line.strip())

            # Add the last speaker's text to the data for the current PDF file
            if current_speaker and current_text:
                data.append({'Speaker': current_speaker, 'Text': '\n'.join(current_text)})

# Create a DataFrame from the list of dictionaries
df = pd.DataFrame(data)

# Display the DataFrame
print(df)
