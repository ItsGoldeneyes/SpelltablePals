let ENVIRONMENT = "preproduction"; // Set to 'production' or 'preproduction' to change the API environment

const useDefaultDictionary = false; // Set this to false when using the API
let nameDictionary = {}; // Default empty dictionary
const extensionID = chrome.runtime.id; // Extension ID for the API to check for valid requests
let APILink = "";

// Set environment-specific API link
if (ENVIRONMENT == "production") {
  APILink = "https://backend-production-c33b.up.railway.app/";
} else {
  APILink = "https://extension-backend-preproduction.up.railway.app/";
}

function simpleUUID() {
  return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, function (c) {
    var r = Math.random() * 16 | 0,
      v = c === "x" ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
}

let sessionID = simpleUUID(); // Session ID to be sent to the API for proper game processing

console.log("Background script loaded");
console.log("Session ID:", sessionID);

function loadDictionary(inputNames, inputCommanders, sessionID) {
  // If using the test variable, set the default dictionary
  if (useDefaultDictionary) {
    nameDictionary = {
      "Goldeneyes": {
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
          "whiteSpace": "",
        },
      },
    };
    // Send the data back to the content script
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
      const currentTab = tabs[0];
      chrome.tabs.sendMessage(currentTab.id ?? 0, {
        action: "recieveNameDictContent",
        data: nameDictionary,
      });
    });
  } else {
    var requestBody = JSON.stringify({
      session_id: sessionID,
      players: inputNames,
      commanders: inputCommanders,
    });

    fetch(APILink + "user_profiles", {
      method: "POST",
      headers: {
        "Origin": "chrome-extension://" + extensionID,
        "Content-Type": "application/json",
      },
      body: requestBody,
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`Network response was not ok: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        nameDictionary = data;
        console.log("Name dictionary fetched successfully:", nameDictionary);

        // Send the data back to the content script
        chrome.tabs.query(
          { active: true, currentWindow: true },
          function (tabs) {
            const currentTab = tabs[0];
            chrome.tabs.sendMessage(currentTab.id ?? 0, {
              action: "recieveNameDictContent",
              data: nameDictionary,
            });
          },
        );
      })
      .catch((error) => {
        console.error("Error fetching name dictionary:", error.message);
      });
  }
}

try {
  chrome.tabs.onUpdated.addListener(function (tabId, changeInfo, tab) {
    if (changeInfo.status == "complete") {
      chrome.scripting.executeScript({
        files: ["content.js"],
        target: { tabId: tabId },
      });
    }
  });
} catch (err) {
  console.log(err);
}

chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
  if (message.action === "getNameDictContent") {
    const sessionID = message.data.sessionID;
    const namesOnPage = message.data.namesOnPage;
    const commandersOnPage = message.data.commandersOnPage;
    console.log("sessionID:", sessionID);
    console.log("namesOnPage:", namesOnPage);
    console.log("commandersOnPage:", commandersOnPage);
    loadDictionary(namesOnPage, commandersOnPage, sessionID);
  } else if (message.action === "getNameDictPopup") {
    console.log(message);
    // Send the data back to the popup
    chrome.runtime.sendMessage({
      action: "recieveNameDictPopup",
      data: nameDictionary,
    });
  }
  if (message.action === "reportPlayer") {
    console.log(message);
    const reason = message.data.reason;
    const username = message.data.reportedUser.trim();
    const sessionId = message.data.sessionId;
    const requestBody = JSON.stringify({
      username,
      reason,
    });
    console.log(requestBody);
    console.log("reporting user...");
    fetch(APILink + "block_user", {
      method: "POST",
      headers: {
        "Origin": "chrome-extension://" + extensionID,
        "Content-Type": "application/json",
      },
      body: requestBody,
    }).then((response) => {
      console.log("getting a response...");
      if (!response.ok) {
        throw new Error(`Network response was not ok: ${response.status}`);
      }
      return response.json();
    })
      .then((data) => {
        console.log("done");
        console.log(data);
      }).catch((error) => {
        console.error("Error reporting user:", error.message);
      });
  }
});
