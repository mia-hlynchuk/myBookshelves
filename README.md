# My Bookshelves

**My Bookshelves** is a personal project that visually showcases the books I've read over the years, displayed as a curated set of virtual bookshelves.

## What It Does

- Uses **Python** to clean and filter my book data (e.g., from LibraryThing exports).
- Uses **JavaScript** to create a visual bookshelf UI.

## How to Use

1. Place your exported book data into the `data/` folder (e.g., `raw_books.json`).
2. Run the Python script to generate cleaned JSON:

   ```bash
   python get_books.py data/raw_books.json data/books.json
   ```

### Data Format Notes

**author field (in the output JSON)**
Always returned as a list of author names, even if there is only one author. This keeps the data consistent and simplifies processing.

**privatecomment field (in the input JSON)**
This field contains user-entered book quotes in the input JSON. If present, the quotes are separated by the `+` symbol.
