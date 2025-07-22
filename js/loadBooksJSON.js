export async function loadBooksJSON() {
  try {
    const response = await fetch('../data/books.json');
    if (!response.ok) {
      throw new Error(`HTTP Error! status: ${response.status}`);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Failed to load JSON: ', error);
  }
}