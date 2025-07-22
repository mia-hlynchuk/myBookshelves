export function createBook(bookInfo) {
  const book = document.createElement('div');
  book.classList.add('book', bookInfo.physical.color);
  book.dataset.id = bookInfo.id;
  book.dataset.title = bookInfo.title;
  book.dataset.author = JSON.stringify(bookInfo.author);

  const title = document.createElement('span');
  title.appendChild(document.createTextNode(bookInfo.title));
  title.className = 'title';
  book.appendChild(title);

  // Only show author's last name if there are fewer than 3
  // and skip all if there are 3 or more because they won't fit on the spine
  if (bookInfo.author.length < 3) {
    bookInfo.author.forEach(author => {
      const authorEle = document.createElement('span');
      authorEle.appendChild(document.createTextNode(author.split(',')[0]));
      authorEle.className = 'author';

      book.appendChild(authorEle);
    });
  }
  return book;
}