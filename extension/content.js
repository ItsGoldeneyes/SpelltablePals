let useDefaultDictionary = false; // Set this to false when using the API

let nameDictionary = {}; // Default empty dictionary

// If using the test variable, set the default dictionary
if (useDefaultDictionary) {
  nameDictionary = {
    "Goldeneyes": {
      "blocked": true,
      "custom_format": {
        "color": "#B8860B",
        "fontSize": ".875rem",
        "fontWeight": "",
        "backgroundColor": "",
        "textDecoration": "",
        "textTransform": "",
        "textShadow": "",
        "textIndent": "",
        "letterSpacing": "",
        "lineHeight": "",
        "wordSpacing": "",
        "whiteSpace": ""
      }
    },
    "blocked_format": {
      "blocked": true,
      "custom_format": {
        "color": "red",
        "fontSize": "1.6em",
        "fontWeight": "bold",
        "backgroundColor": "",
        "textDecoration": "",
        "textTransform": "",
        "textShadow": "",
        "textIndent": "",
        "letterSpacing": "",
        "lineHeight": "",
        "wordSpacing": "",
        "whiteSpace": ""
      }
    }
  };
} else {
  fetch('https://backend-production-c33b.up.railway.app/user_profiles', {
    method: 'GET',
    headers: {
      'Origin': 'chrome-extension://1'
    }
  })
    .then(response => {
      if (!response.ok) {
        throw new Error(`Network response was not ok: ${response.statusText}`);
      }
      return response.json();
    })
    .then(data => {
      nameDictionary = data;
      console.log('Name dictionary fetched successfully:', nameDictionary);
    })
    .catch(error => {
      console.error('Error fetching name dictionary:', error.message);
    });
}

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