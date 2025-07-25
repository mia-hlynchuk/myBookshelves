export function createBook(bookInfo) {
  const color = bookInfo.physical.color.toLowerCase();

  const book = document.createElement('div');
  book.classList.add('book');
  book.dataset.id = bookInfo.id;
  book.dataset.title = bookInfo.title;
  book.dataset.author = JSON.stringify(bookInfo.author);

  const title = document.createElement('span');
  title.appendChild(document.createTextNode(bookInfo.title));
  title.className = 'title';
  title.style.color = `var(--bk-text-${color})`;
  book.appendChild(title);
  
  book.style.backgroundColor = `var(--bk-bkg-${color})`;
  
  // The width is the spine of the book
  book.style.width = `${bookInfo.physical.thickness * 20}px`;
  book.style.height = `${bookInfo.physical.height * 15}px`;

  // Only show author's last name if there are fewer than 3
  // and skip all if there are 3 or more because they won't fit on the spine
  if (bookInfo.author.length < 3) {
    bookInfo.author.forEach(author => {
      const authorEle = document.createElement('span');
      authorEle.appendChild(document.createTextNode(author.split(',')[0]));
      authorEle.className = 'author';
      authorEle.style.color = `var(--bk-text-${color})`;

      book.appendChild(authorEle);
    });
  }
  return book;
}