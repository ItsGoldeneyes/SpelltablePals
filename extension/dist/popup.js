"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
let nameDictionary = {};
chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
  if (message.action === "recieveNameDictPopup") {
    nameDictionary = message.data;
  }
});
function loadDynamicCSS() {
  // Create a link element
  const linkElement = document.createElement("link");
  // Set the attributes of the link element
  linkElement.rel = "stylesheet";
  linkElement.type = "text/css";
  linkElement.href = "popup.css";
  // Append the link element to the head section of the document
  document.head.appendChild(linkElement);
}
document.addEventListener("DOMContentLoaded", function () {
  loadDynamicCSS();
  // if value of nameDictionary is empty, send message to background script to get the name dictionary
  if (Object.keys(nameDictionary).length === 0) {
    chrome.runtime.sendMessage({ action: "getNameDictPopup" });
  }
  chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    const currentTab = tabs[0];
    const url = new URL(currentTab.url);
    const titlePage = document.getElementById("titlePage");
    const gamePage = document.getElementById("gamePage");
    const playerInfoContainer = document.getElementById("playerInfoContainer");
    if (
      url.hostname === "spelltable.wizards.com" &&
      url.pathname.startsWith("/game/")
    ) {
      if (titlePage !== null) {
        titlePage.style.display = "none";
      }
      if (gamePage !== null) {
        gamePage.style.display = "block";
      }
      // Execute content script to get player names after timeout
      setTimeout(() => {
        if (currentTab.id !== undefined) {
          chrome.scripting.executeScript({
            target: { tabId: currentTab.id },
            func: getPlayersInfo,
          });
        }
      }, 25);
    } else {
      if (titlePage !== null) {
        titlePage.style.display = "block";
      }
      if (gamePage !== null) {
        gamePage.style.display = "none";
      }
    }
    loadDynamicCSS();
  });
});
function getPlayersInfo() {
  const elements = document.querySelectorAll(
    ".font-bold.truncate.leading-snug.text-sm",
  );
  const namesOnPage = Array.from(elements).map((element) => {
    var _a;
    return (_a = element.textContent) === null || _a === void 0
      ? void 0
      : _a.trim();
  });
  chrome.runtime.sendMessage({ action: "updatePopup", names: namesOnPage });
}
chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
  if (message.action === "updatePopup") {
    const playerInfoContainer = document.getElementById("playerInfoContainer");
    if (playerInfoContainer !== null) {
      playerInfoContainer.innerHTML = "";
    }
    // Ensure that there are always four players
    for (let i = 0; i < 4; i++) {
      const playerName = message.names[i] || "<no player>";
      const playerInfoDiv = document.createElement("div");
      playerInfoDiv.classList.add("player-info");
      playerInfoDiv.textContent = `${playerName} - ${
        getPlayerStatus(playerName.lower())
      }`;
      if (playerInfoContainer !== null) {
        playerInfoContainer.appendChild(playerInfoDiv);
      }
    }
  }
});
function getPlayerStatus(name) {
  if (nameDictionary[name]) {
    if (nameDictionary[name].blocked) {
      // If the user is blocked, display role as "Blocked" and include the reason
      return `Role: Blocked - Reason: ${
        nameDictionary[name].reason || "Unknown"
      }`;
    } else if (nameDictionary[name].role) {
      // If the user is not blocked and has a role, display the role
      return `Role: ${nameDictionary[name].role}`;
    }
  }
  // If no information is available or the user is not blocked and has no role information
  return "Role: Unknown";
}
