let useDefaultDictionary = false; // Set this to false when using the API

let nameDictionary = {}; // Default empty dictionary

// If using the test variable, set the default dictionary
if (useDefaultDictionary) {
  nameDictionary = {
    "Goldeneyes": true,
  };
} else {
  fetch('https://backend-production-c33b.up.railway.app/blocked_users', {
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

function detectBlocked(nameDictionary) {
  const elements = document.querySelectorAll('.font-bold.truncate.leading-snug.text-sm');

  elements.forEach(element => {
    const elementText = element.textContent.trim();

    // Check if the element's text is in the name dictionary
    if (nameDictionary[elementText]) {
      element.style.color = 'red';
      element.style.fontSize = '1.5em'
    } else {
      // Reset the color if it's not in the dictionary
      element.style.color = '';
    }
  });
}

function main(nameDictionary) {

  // Detect names in the window
  const textElements = document.querySelectorAll('.font-bold.truncate.leading-snug.text-sm');
  const namesOnPage = [];

  textElements.forEach(element => {
    const name = element.textContent.trim();
    namesOnPage.push(name);
  });

  // Check if the length of namesOnPage is not zero before calling the function
  if (namesOnPage.length !== 0) {
    detectBlocked(nameDictionary);
  }
}

// Set up an interval to execute detectAndHighlight every 2 seconds
const intervalId = setInterval(() => main(nameDictionary), 2000);