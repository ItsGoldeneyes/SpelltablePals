let useDefaultDictionary = false; // Set this to false when using the API
let nameDictionary = {}; // Default empty dictionary

function loadDictionary(inputNames) {
    // If using the test variable, set the default dictionary
    if (useDefaultDictionary) {
        nameDictionary = {
        "Goldeneyes": {
            "blocked": true,
            "role": "custom",
            "reason": "Test",
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
        }
        };
        // Send the data back to the content script
        chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
            const currentTab = tabs[0];
            chrome.tabs.sendMessage(currentTab.id, { action: 'recieveNameDictContent', data: nameDictionary });
        });
    } else {
        fetch('https://backend-production-c33b.up.railway.app/user_profiles', {
        method: 'POST',
        headers: {
            'Origin': 'chrome-extension://1'
            },
        body: JSON.stringify(inputNames)
        })
        .then(response => {
            if (!response.ok) {
            throw new Error(`Network response was not ok: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            nameDictionary = data;
            console.log('Name dictionary fetched successfully:', nameDictionary);
            
            // Send the data back to the content script
            chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
                const currentTab = tabs[0];
                chrome.tabs.sendMessage(currentTab.id, { action: 'recieveNameDictContent', data: nameDictionary });
            });
        })
        .catch(error => {
            console.error('Error fetching name dictionary:', error.message);
        });
    } 
}

try {
    chrome.tabs.onUpdated.addListener(function (tabId, changeInfo, tab) {
        if (changeInfo.status == 'complete') {
            chrome.scripting.executeScript({
                files: ['content.js'],
                target: { tabId: tabId }
            });
        }
    });
}catch(err){
    console.log(err);
}

chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
    if (message.action === 'getNameDictContent') {
        namesOnPage = message.data;
        console.log('namesOnPage:', namesOnPage);
        loadDictionary(namesOnPage);
    } else
    if (message.action === 'getNameDictPopup') {
        console.log(message);
        // Send the data back to the popup
        chrome.runtime.sendMessage({ action: 'recieveNameDictPopup', data: nameDictionary });
    }
  });