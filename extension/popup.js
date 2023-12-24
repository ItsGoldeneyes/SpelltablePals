let nameDictionary = {}; // Instantiate global variable

chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
  if (message.action === 'recieveNameDictPopup') {
    nameDictionary = message.data;
  }
});

document.addEventListener('DOMContentLoaded', function () {
  // if value of nameDictionary is empty, send message to background script to get the name dictionary
  if (Object.keys(nameDictionary).length === 0) {
    chrome.runtime.sendMessage({ action: 'getNameDictPopup' });
  }
  chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    const currentTab = tabs[0];
    const url = new URL(currentTab.url);

    const titlePage = document.getElementById('titlePage');
    const gamePage = document.getElementById('gamePage');
    const playerInfoContainer = document.getElementById('playerInfoContainer');

    if (url.hostname === 'spelltable.wizards.com' && url.pathname.startsWith('/game/')) {
      titlePage.style.display = 'none';
      gamePage.style.display = 'block';

      // Execute content script to get player names after timeout
      setTimeout(() => {
        chrome.scripting.executeScript({
          target: { tabId: currentTab.id },
          function: getPlayersInfo
        });
      }, 25);
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
  