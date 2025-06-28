import sys
import json
import re

def extract_books(input_file, output_file):
  books_data = []

  # Open and read the JSON file
  with open(input_file, 'r', encoding='utf-8') as file:
    data = json.load(file)

    # Loop though each entry
    for entry_id, book in data.items(): 
      # Clean up the 'title' property, which may include a subtitle
      # Step 1: Replace HTML entity and split on colon to separate title and subtitle
      title_raw = book['title'].replace("&#039;", "'").split(':')

      # Step 2: Remove any text after '(', since some entries repeat the title or series' name in parentheses
      title = title_raw[0].split('(')[0].strip()

      subtitle = extract_subtitle(title_raw)

      primary_author = book['primaryauthor']
      
      secondary_author_raw = book.get('secondaryauthor')
      # Always return a list, even if empty
      secondary_author = secondary_author_raw.split("|") if secondary_author_raw else []

      # Removing duplicates if secondary is just the same primary
      if len(secondary_author) == 1 and secondary_author[0].strip() == primary_author.strip():
        secondary_author = [] 

      # Combine with primary author
      authors = [primary_author] + secondary_author

      # Default just incase its missing a color
      book_color = None 

      for item in book['collections']:
        if item.startswith('_'):
          book_color = item.split('_')[1]
       
      # Physical features of the book
      physical = {
        'color': book_color
      }

      # Optional fields because they might not be included 
      height = convert_to_num(book.get('height'), 'float')
      if height is not None:
        physical['height'] = height

      thickness = convert_to_num(book.get('thickness'), 'float')
      if thickness is not None:
        physical['thickness'] = thickness
     
      pages = convert_to_num(book.get('pages'), 'int')
      if pages is not None:
        physical['pages'] = pages


      book_entry = {
        'id': entry_id,
        'isbn': book.get('originalisbn'),
        'title': title,
        'author': authors,
        'started': book['datestarted'],
        'ended': book['dateread'],
        'quotes': 'optional quotes go here',
        'physical': physical
      }

      if subtitle is not None:
        book_entry['subtitle'] = subtitle      

      books_data.append(book_entry)
      


  
  # Write the output file
  with open(output_file, "w", encoding='utf-8') as outfile:
    json.dump(books_data, outfile, ensure_ascii=False, indent=2)

# Helper Functions
def extract_subtitle(title_raw):
  if len(title_raw) == 1: 
    return None
    
  subtitle = title_raw[1].split('(')[0].strip()

  # Remove generic subtitles like "A Novel", "A Novel of" or "A Memoir" but not "A Memoir of"
  if re.search(r'\bA Novel\b(?:\s+of\b)?|\bA Memoir\b(?!\s+of\b)', subtitle, re.IGNORECASE):
    return None
    
  # Only return subtitle if it's not empty 
  return subtitle if subtitle else None
  

def convert_to_num(s, num_type='int'):
  """
  Extracts the number from the input string and converts it to an integer or a float.
  
  Parameters:
    s (str) - the input string containing a number
    num_type (str) - the type of number to convert to, either 'int' (default) or 'float' 
  
  Returns:
    int, float rounded to 2 decimals or None if no number found
  """
  if not s:
    return None
  
  pattern = r'\d+(\.\d+)?' if num_type == 'float' else r'\d+'
  match = re.search(pattern, s)

  if not match:
    return None
  
  num = match.group()
  
  return round(float(num), 2) if num_type == 'float' else int(num)

 

if __name__ == "__main__":
  if len(sys.argv) != 3:
    print("Usage: python get_books.py <input_file> <output_file>")
    sys.exit(1)  
  
  input_file = sys.argv[1]
  output_file = sys.argv[2]
  try:
    extract_books(input_file, output_file)
  except FileNotFoundError:
    print(f"Error: File not found: {input_file}")  
    sys.exit(1)
  except Exception as e:
    print(f"An error occurred: {e}")
    sys.exit(1)