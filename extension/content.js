let nameDictionary = {};
let lastNamesOnPage = [];
let lastCommandersOnPage = [];

function main() {

  addSpectatorButton();

  // Retrieve the player names
  const nameElements = document.querySelectorAll('.font-bold.truncate.leading-snug.text-sm');
  const namesOnPage = [];

  nameElements.forEach(element => {
    const name = element.textContent.trim().toLowerCase();
    namesOnPage.push(name);
  });

  // Retrieve the player's commanders
  const commanderElements = document.querySelectorAll('.text-xs.italic.text-gray-400.truncate.leading-snug.flex > div');
  const commandersOnPage = [];

  commanderElements.forEach(element => {
    const commanderName = element.textContent.trim();
    commandersOnPage.push(commanderName);
  });

  // If there are no names on the page, the active page is probably the game start page
  if (namesOnPage.length !== 0) {
    const allNamesOnPageAreContained = JSON.stringify(lastNamesOnPage) === JSON.stringify(namesOnPage);
    const allCommandersAreContained = JSON.stringify(lastCommandersOnPage) === JSON.stringify(commandersOnPage);

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
    if (nameDictionary[elementText] && nameDictionary[elementText].custom_format !== null) {
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
    } else {
      // If the player does not have a record in the name dictionary, reset the format
      element.style.color = '';
      element.style.fontSize = '';
      element.style.fontWeight = '';
      element.style.backgroundColor = '';
      element.style.textDecoration = '';
      element.style.textTransform = '';
      element.style.textShadow = '';
      element.style.textIndent = '';
      element.style.letterSpacing = '';
      element.style.lineHeight = '';
      element.style.wordSpacing = '';
      element.style.whiteSpace = '';
    }
  });
}

// Function to add the "Join as Spectator" button
function addSpectatorButton() {
  // Check if the URL already contains "/?spectate=true"
  if (window.location.href.includes('/?spectate=true')) {
    return; // Do not add the button if it's already present in the URL
  }

  const targetDiv = document.querySelector('.flex.py-6');

  if (targetDiv && !document.getElementById('spectatorButton')) {
    const spectatorButton = document.createElement('button');
    spectatorButton.textContent = 'Spectate';
    spectatorButton.id = 'spectatorButton';

    // Copy styling from the provided button class
    spectatorButton.className = 'flex justify-center px-4 rounded items-center hover:no-underline bg-st-purple-light hover:bg-st-purple-normal text-white h-10';
    spectatorButton.style.lineHeight = '100%';
    spectatorButton.style.marginLeft = '0.75rem';

    spectatorButton.addEventListener('click', function () {
      // Reload the page with "?spectate=true" appended to the URL
      window.location.href = window.location.href + '/?spectate=true';
    });

    targetDiv.appendChild(spectatorButton);
  }
}

// Set up an interval to execute main function every second
const intervalId = setInterval(() => main(), 1000);