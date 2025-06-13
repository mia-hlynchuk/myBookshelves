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

author is always an array for consistency, even if there’s just one author.
