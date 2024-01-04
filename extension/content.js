let nameDictionary = {};
let lastNamesOnPage = [];
let lastCommandersOnPage = [];

function main() {

  // Detect names on the webpage
  const nameElements = document.querySelectorAll('.font-bold.truncate.leading-snug.text-sm');
  const namesOnPage = [];
  const commanderElements = document.querySelectorAll('.text-xs.italic.text-gray-400.truncate.leading-snug.flex > div');
  const commandersOnPage = [];

  nameElements.forEach(element => {
    const name = element.textContent.trim().toLowerCase();
    namesOnPage.push(name);
  });

  commanderElements.forEach(element => {
    const commanderName = element.textContent.trim();
    commandersOnPage.push(commanderName);
  });

  // If there are no names on the page, the active page is probably the start page
  if (namesOnPage.length !== 0) {
    // Check if all elements in namesOnPage and commandersOnPage are contained in the last page
    const allNamesOnPageAreContained = namesOnPage.every(name => lastNamesOnPage.includes(name));
    const allCommandersAreContained = commandersOnPage.every(commander => lastCommandersOnPage.includes(commander));

    if (!allNamesOnPageAreContained || !allCommandersAreContained) {
      chrome.runtime.sendMessage({
        action: 'getNameDictContent',
        data: { "namesOnPage": namesOnPage, "commandersOnPage": commandersOnPage, "sessionID": window.location.pathname }
      });
    }
  }

  lastNamesOnPage = namesOnPage;
  lastCommandersOnPage = commandersOnPage;
}

chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
  if (message.action === 'recieveNameDictContent') {
    nameDictionary = message.data;
    formatNames();
  }
});

// Convert all keys in an object to lowercase
const lowerize = obj =>
  Object.keys(obj).reduce((acc, k) => {
    acc[k.toLowerCase()] = obj[k];
    return acc;
  }, {});

// Format names on the page
function formatNames() {
  lowerize(nameDictionary);
  const elements = document.querySelectorAll('.font-bold.truncate.leading-snug.text-sm');

  elements.forEach(element => {
    const elementText = element.textContent.trim().toLowerCase();

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

// Set up an interval to execute main function every 2 seconds
const intervalId = setInterval(() => main(), 2000);