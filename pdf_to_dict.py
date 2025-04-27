import re
import fitz
import json

file = "/Users/eappelson/MBMBAM-Transcript-Analysis/Transcripts/MBMBaM-Ep034-Make-it-Magic.pdf"

def mbmbam_to_csv(file): 
 
  # Opening the document
  doc = fitz.open(file)

  # Creating lists
  words = []
  bold_positions = []
  bold_data = []
  
  # Creating a word counter
  word_count = 0

  # Looping though all pages
  for page_num in range(len(doc)):
    
      # Loading the page
      page = doc.load_page(page_num)
      
      # Extracting blocks from the page
      blocks = page.get_text("dict")["blocks"]
  
      # Looking through all text blocks
      for block in blocks:
          if block['type'] == 0:
              for line in block["lines"]:
                  for span in line["spans"]:
                    
                      # Splitting the blocks into text words and giving each word a number
                      words_in_span = span["text"].split()
                      for word in words_in_span:
                          word_count += 1
                          
                          # Creating a dictionary of words, their count, and whether they are bold
                          is_bold = "bold" in span["font"].lower()
                          words.append({
                              "text": word,
                              "position": word_count,
                              "is_bold": is_bold
                          })
                          
                          # Appending the bold words to bold positions
                          if is_bold:
                              bold_positions.append(word_count)
  
  # Looping through bold positions
  for i in range(len(bold_positions)):
      
      # Defining range of text between bold positions
      start_pos = bold_positions[i]
      next_pos = bold_positions[i + 1] if i + 1 < len(bold_positions) else len(words)
      bold_word = next(word["text"] for word in words if word["position"] == start_pos)
      
      # Defining the text between these bold positionss
      text_after_bold = " ".join([word["text"] for word in words if start_pos < word["position"] < next_pos])
      
      # Clean up the text after the bold word
      text_after_bold = re.sub(': ', '', text_after_bold)
      text_after_bold = re.sub('\[(.*?)\]', '', text_after_bold).strip()
      
      # Creating a dictionary of bold words and the text
      bold_data.append({"bold_word": bold_word, "text_after_bold": text_after_bold})
  
  return(bold_data)

mbmbam_to_csv(file)
