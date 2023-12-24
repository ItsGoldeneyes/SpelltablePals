let useDefaultDictionary = false; // Set this to false when using the API

chrome.runtime.sendMessage({ action: 'getNameDict' });

let nameDictionary = {}; // Default empty dictionary

chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
  if (message.action === 'recieveNameDict') {
    nameDictionary = message.data;
  }
});

function formatNames(nameDictionary) {
  const elements = document.querySelectorAll('.font-bold.truncate.leading-snug.text-sm');

  elements.forEach(element => {
    const elementText = element.textContent.trim();

    // Check if the player name is in the name dictionary
    if (nameDictionary[elementText]) {
      // If the player is flagged as blocked, use the default blocked format
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

function main(nameDictionary) {

  // Detect names on the webpage
  const textElements = document.querySelectorAll('.font-bold.truncate.leading-snug.text-sm');
  const namesOnPage = [];

  textElements.forEach(element => {
    const name = element.textContent.trim();
    namesOnPage.push(name);
  });

  // Check if the length of namesOnPage is not zero before calling the format function
  if (namesOnPage.length !== 0) {
    formatNames(nameDictionary);
  }
}

// Set up an interval to execute detectAndHighlight every 2 seconds
const intervalId = setInterval(() => main(nameDictionary), 2000);