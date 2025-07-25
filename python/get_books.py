import sys
import json
import html
import re
import copy

def extract_books(input_file, output_file):
  books_data = {
    'favorites': [], # Holds the id references to books
    'booksByYear': {}
  }

  # Open and read the JSON file
  with open(input_file, 'r', encoding='utf-8') as file:
    data = json.load(file)

    # Loop though each entry
    for entry_id, book in data.items(): 
      # Clean up the 'title' property, which may include a subtitle
      # Step 1: Replace HTML entity and split on colon to separate title and subtitle
      title_raw = html.unescape(book['title']).split(':')

      # Step 2: Remove any text after '(', since some entries repeat the title or series' name in parentheses
      title = title_raw[0].split('(')[0].strip()

      subtitle = extract_subtitle(title_raw)

      # Get last, first names of authors and illustrators only
      authors = []
      for author in book['authors']:
        if author['role'] in ('Author', 'Illustrator'):
          authors.append(html.unescape(author['lf']))
      
      # Quotes 
      quotes = []
      # 'privatecomment' holds quotes entered by the user
      raw_quotes = book.get('privatecomment')
      if raw_quotes:
        # Replace all whitespace (spaces, tabs, newlines) with a single space
        cleaned = re.sub(r'\s+', ' ', raw_quotes)

        # Split on '+', strip each part and ignore empty strings
        raw_quotes_list = cleaned.split('+')        
        
        # Loop through each piece to add to quotes 
        for q in raw_quotes_list:
          stripped = q.strip()
          # Only add if its not an empty string after stripping
          if stripped: 
            quotes.append(stripped)
     
      # Default just incase its missing a color
      book_color = None 

      # Keeps track if its a re-read 
      is_reread = False 

      for item in book['collections']:
        # Extract the book's color
        if item.startswith('_'):
          book_color = item.split('_')[1]
        # If its a favorite book, store the entry id 
        elif item == 'Favorites':
          books_data['favorites'].append(entry_id)
        # Check if its a reread book
        elif item == 'Re-Read':
          is_reread = True

      # Physical features of the book
      physical = {
        'color': book_color
      }

      pages = convert_to_num(book.get('pages'), 'int')
      physical['pages'] = pages

      height = convert_to_num(book.get('height'), 'float')
      default_height = 8.5
      physical['height'] = height if height is not None else default_height

      thickness = convert_to_num(book.get('thickness'), 'float')
      default_thickness = 0.00323 * pages + 0.0547
      physical['thickness'] = thickness if thickness is not None else default_thickness
   
      book_entry = {
        'id': entry_id,
        'isbn': book.get('originalisbn'),
        'title': title,
        'author': authors,
        'started': book['datestarted'],
        'ended': book['dateread'],
        'physical': physical
      }

      if subtitle is not None:
        book_entry['subtitle'] = subtitle    
      
      if quotes:
        book_entry['quotes'] = quotes

      
      
      append_entry(book_entry, books_data['booksByYear'])
     
      
      # Handle re-read books
      if is_reread:
        # Re-Reads alway include additional dates in the 'comment' field, separated by `||`
        reread_dates = book['comment'].split('||')
        
        # Matches YYYY-MM or YYYY-MM-DD
        date_pattern = r'\d{4}-\d{2}(?:-\d{2})?'

        # For each re-read instance, duplicate the book and update its read dates
        for rr_date in reread_dates:
          dates = re.findall(date_pattern, rr_date)
          
          re_read_book = copy.deepcopy(book_entry)
          re_read_book['started'] = dates[0]
          re_read_book['ended'] = dates[1]

          append_entry(re_read_book, books_data['booksByYear'])

    
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


def append_entry(entry, data):
  # Append the book entry under the year it was finished in
  year = re.findall(r'\d{4}', entry['ended'])[0]
  # Just in case that year doesn't exit yet, create an empty list for it
  data.setdefault(year, []).append(entry)

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