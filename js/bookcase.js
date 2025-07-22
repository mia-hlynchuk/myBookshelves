import { getRandomInt, appendElement } from './helpers.js';
import { createBook } from './createBook.js';

export function createBookcase(numOfShelves, shelfId) {  
  // Create the bookcase structure and its label 
  appendElement('article', shelfId, 'bookcase', 'container', null);
  appendElement('h3', null, 'year', shelfId, shelfId); 

  // Create shelf sections and append it to the bookcase
  for (let i = 1; i <= numOfShelves; i++) {
    appendElement('section', `${shelfId}-${i}`, 'shelf', shelfId, null);
  }
}

export function placeBooks(books, bookcaseId) {
  // Books will be placed/appended only to the specific bookcase
  // Get the number of shelves in the bookcase
  const shelvesNum = document.getElementById(bookcaseId).querySelectorAll('.shelf').length;
  books.forEach(book => {
    // Get a random shelf number and append the book to it
    const randomShelfId = `${bookcaseId}-${getRandomInt(1, shelvesNum)}`;
    const randomShelf = document.getElementById(randomShelfId);
    randomShelf.appendChild(createBook(book));
  });
}

