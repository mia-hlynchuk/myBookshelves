export function getRandomInt(min, max) { 
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

export function appendElement(ele, eleId, eleClass, intoId, textNode) { 
  // Create a new element
  const newDiv = document.createElement(ele);
  if (eleId) newDiv.id = eleId;

  newDiv.className = eleClass;
  
  if (textNode) {
      const newContent = document.createTextNode(textNode);
      newDiv.appendChild(newContent);
  }

  // Add the newly created element and its context into the DOM
  const currentDiv = document.getElementById(intoId);
  currentDiv.appendChild(newDiv);
}