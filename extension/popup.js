let useDefaultDictionary = false; // Set this to false when using the API

let nameDictionary = {}; // Default empty dictionary

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

document.addEventListener('DOMContentLoaded', function () {
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
      const currentTab = tabs[0];
      const url = new URL(currentTab.url);
  
      const titlePage = document.getElementById('titlePage');
      const gamePage = document.getElementById('gamePage');
      const playerInfoContainer = document.getElementById('playerInfoContainer');
  
      if (url.hostname === 'spelltable.wizards.com' && url.pathname.startsWith('/game/')) {
        titlePage.style.display = 'none';
        gamePage.style.display = 'block';
  
        // Execute content script to get player names
        chrome.scripting.executeScript({
          target: { tabId: currentTab.id },
          function: getPlayersInfo
        });
      } else {
        titlePage.style.display = 'block';
        gamePage.style.display = 'none';
      }
    });
  });
  
  function getPlayersInfo() {
    const elements = document.querySelectorAll('.font-bold.truncate.leading-snug.text-sm');
    const namesOnPage = Array.from(elements).map(element => element.textContent.trim());
  
    chrome.runtime.sendMessage({ action: 'updatePopup', names: namesOnPage });
  }
  
  chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
    if (message.action === 'updatePopup') {
      const playerInfoContainer = document.getElementById('playerInfoContainer');
      playerInfoContainer.innerHTML = '';
  
      message.names.forEach(name => {
        const playerInfoDiv = document.createElement('div');
        playerInfoDiv.classList.add('player-info');
  
        if (nameDictionary[name] && nameDictionary[name].blocked) {
          playerInfoDiv.classList.add('blocked-player');
        }
  
        playerInfoDiv.textContent = `${name} - ${getPlayerStatus(name)}`;
        playerInfoContainer.appendChild(playerInfoDiv);
      });
    }
  });
  
  function getPlayerStatus(name) {
    if (nameDictionary[name]) {
      if (nameDictionary[name].blocked) {
        // If the user is blocked, display role as "Blocked" and include the reason
        return `Role: Blocked - Reason: ${nameDictionary[name].reason || 'Unknown'}`;
      } else if (nameDictionary[name].role) {
        // If the user is not blocked and has a role, display the role
        return `Role: ${nameDictionary[name].role}`;
      }
    }
  
    // If no information is available or the user is not blocked and has no role information
    return 'Role: Unknown';
  }
  