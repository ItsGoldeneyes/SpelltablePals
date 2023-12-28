let nameDictionary = {};
let lastNamesOnPage = [];

chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
  if (message.action === 'recieveNameDictContent') {
    nameDictionary = message.data;
    formatNames();
  }
});

function formatNames() {
  const elements = document.querySelectorAll('.font-bold.truncate.leading-snug.text-sm');

  elements.forEach(element => {
    const elementText = element.textContent.trim();

    // If the player has a record in the name dictionary, apply the custom format
    if (nameDictionary[elementText]) {
        element.style.color = nameDictionary[elementText].custom_format.color;
        element.style.fontSize = nameDictionary[elementText].custom_format.fontSize;
        element.style.fontWeight = nameDictionary[elementText].custom_format.fontWeight;
        element.style.backgroundColor = nameDictionary[elementText].custom_format.backgroundColor;
        element.style.textDecoration = nameDictionary[elementText].custom_format.textDecoration;
        element.style.textTransform = nameDictionary[elementText].custom_format.textTransform;
        element.style.textShadow = nameDictionary[elementText].custom_format.textShadow;
        element.style.textIndent = nameDictionary[elementText].custom_format.textIndent;
        element.style.letterSpacing = nameDictionary[elementText].custom_format.letterSpacing;
        element.style.lineHeight = nameDictionary[elementText].custom_format.lineHeight;
        element.style.wordSpacing = nameDictionary[elementText].custom_format.wordSpacing;
        element.style.whiteSpace = nameDictionary[elementText].custom_format.whiteSpace;
    }
  });
}

function main() {

  // Detect names on the webpage
  const textElements = document.querySelectorAll('.font-bold.truncate.leading-snug.text-sm');
  const namesOnPage = [];

  textElements.forEach(element => {
    const name = element.textContent.trim();
    namesOnPage.push(name);
  });

  // Check if there are any names on the page
  if (namesOnPage.length !== 0) {
    // Check if all elements in namesOnPage are contained within lastNamesOnPage
    const allNamesOnPageAreContained = namesOnPage.every(name => lastNamesOnPage.includes(name));
    
    if (!allNamesOnPageAreContained) {
      chrome.runtime.sendMessage({ action: 'getNameDictContent', data: { "namesOnPage": namesOnPage, "sessionID": window.location.pathname } });
    }
  }

  lastNamesOnPage = namesOnPage;
}

// Set up an interval to execute detectAndHighlight every 2 seconds
const intervalId = setInterval(() => main(), 2000);