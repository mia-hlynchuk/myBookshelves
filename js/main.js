import { loadBooksJSON } from "./loadBooksJSON.js";
import { createBookcase, placeBooks } from "./bookcase.js";

loadBooksJSON().then(books => {
  // Sort the year keys in descending order
  const descendingYears = Object.keys(books['booksByYear']).sort((a, b) => b - a);

  for (const year of descendingYears) {
    createBookcase(5, year);
    placeBooks(books['booksByYear'][year], year);
  }
});
