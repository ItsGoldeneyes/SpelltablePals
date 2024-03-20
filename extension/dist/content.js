"use strict";
/// <reference lib="dom" />
let nameDictionary2 = {};
let lastNamesOnPage = [];
let lastCommandersOnPage = [];
let playerDropdownButtonListeners = [];
let currentReportedPlayer = null;
function main() {
    addSpectatorButton();
    const playerDropdownButtons = document.querySelectorAll("button.p-1.shadow-md.rounded.text-white.transition-all.ease-in-out.duration-200.bg-surface-high");
    for (const dropdown of Array.from(playerDropdownButtons).filter((dropdown) => !(playerDropdownButtonListeners.filter((v) => v === dropdown).length >
        0))) {
        playerDropdownButtonListeners.push(dropdown);
        dropdown.addEventListener("click", () => {
            var _a, _b, _c, _d, _e, _f, _g, _h;
            setTimeout(() => {
                addReportButton();
            }, 10);
            const player = (_h = (_g = (_f = (_e = (_d = (_c = (_b = (_a = dropdown.parentElement) === null || _a === void 0 ? void 0 : _a.parentElement) === null || _b === void 0 ? void 0 : _b.parentElement) === null || _c === void 0 ? void 0 : _c.querySelector("div.flex-1.overflow-hidden")) === null || _d === void 0 ? void 0 : _d.querySelector("div.flex-1")) === null || _e === void 0 ? void 0 : _e.querySelector("div.cursor-pointer.text-white.w-full.overflow-hidden")) === null || _f === void 0 ? void 0 : _f.querySelector("div.flex.items-center.w-full")) === null || _g === void 0 ? void 0 : _g.querySelector("div.font-bold.truncate.leading-snug.text-sm")) === null || _h === void 0 ? void 0 : _h.innerHTML;
            if (player !== undefined) {
                currentReportedPlayer = player;
            }
            else {
                currentReportedPlayer = null;
            }
        });
    }
    // Retrieve the player names
    const nameElements = document.querySelectorAll(".font-bold.truncate.leading-snug.text-sm");
    const namesOnPage = [];
    nameElements.forEach((element) => {
        var _a;
        const name = (_a = element === null || element === void 0 ? void 0 : element.textContent) === null || _a === void 0 ? void 0 : _a.trim().toLowerCase();
        if (name !== undefined) {
            namesOnPage.push(name);
        }
    });
    // Retrieve the player's commanders
    const commanderElements = document.querySelectorAll(".text-xs.italic.text-gray-400.truncate.leading-snug.flex");
    const commandersOnPage = [];
    commanderElements.forEach((element) => {
        var _a, _b, _c, _d;
        // If there are no child divs, add two empty strings to the array
        if (!element.children) {
            commandersOnPage.push("", "");
        }
        else {
            let child;
            if (element.children[0]) {
                child = (_b = (_a = element === null || element === void 0 ? void 0 : element.children[0]) === null || _a === void 0 ? void 0 : _a.textContent) === null || _b === void 0 ? void 0 : _b.trim();
                if (child !== undefined)
                    commandersOnPage.push(child);
            } // child 1 is a / character
            if (element.children[2]) {
                child = (_d = (_c = element === null || element === void 0 ? void 0 : element.children[2]) === null || _c === void 0 ? void 0 : _c.textContent) === null || _d === void 0 ? void 0 : _d.trim();
                if (child !== undefined)
                    commandersOnPage.push(child);
            }
            else {
                commandersOnPage.push("");
            }
        }
    });
    // If there are no names on the page, the active page is probably the game start page
    if (namesOnPage.length !== 0) {
        const allNamesOnPageAreContained = JSON.stringify(lastNamesOnPage) === JSON.stringify(namesOnPage);
        const allCommandersAreContained = JSON.stringify(lastCommandersOnPage) ===
            JSON.stringify(commandersOnPage);
        if (!allNamesOnPageAreContained || !allCommandersAreContained) {
            chrome.runtime.sendMessage({
                action: "getNameDictContent",
                data: {
                    "namesOnPage": namesOnPage,
                    "commandersOnPage": commandersOnPage,
                    "sessionID": window.location.pathname,
                },
            });
        }
    }
    lastNamesOnPage = namesOnPage;
    lastCommandersOnPage = commandersOnPage;
}
chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
    if (message.action === "recieveNameDictContent") {
        nameDictionary2 = message.data;
        formatNames();
    }
});
// Convert all keys in an object to lowercase
const lowerize = (obj) => Object.keys(obj).reduce((acc, k) => {
    acc[k.toLowerCase()] = obj[k];
    return acc;
}, {});
// Format names on the page
function formatNames() {
    lowerize(nameDictionary2);
    const elements = document.querySelectorAll(".font-bold.truncate.leading-snug.text-sm");
    elements.forEach((element) => {
        var _a;
        const elementText = (_a = element.textContent) === null || _a === void 0 ? void 0 : _a.trim().toLowerCase();
        // If the player has a record in the name dictionary, apply the custom format
        if (elementText !== undefined &&
            nameDictionary2[elementText] &&
            nameDictionary2[elementText].custom_format !== null) {
            element.style.color =
                nameDictionary2[elementText].custom_format.color;
            element.style.fontSize =
                nameDictionary2[elementText].custom_format.fontSize;
            element.style.fontWeight =
                nameDictionary2[elementText].custom_format.fontWeight;
            element.style.backgroundColor =
                nameDictionary2[elementText].custom_format.backgroundColor;
            element.style.textDecoration =
                nameDictionary2[elementText].custom_format.textDecoration;
            element.style.textTransform =
                nameDictionary2[elementText].custom_format.textTransform;
            element.style.textShadow =
                nameDictionary2[elementText].custom_format.textShadow;
            element.style.textIndent =
                nameDictionary2[elementText].custom_format.textIndent;
            element.style.letterSpacing =
                nameDictionary2[elementText].custom_format.letterSpacing;
            element.style.lineHeight =
                nameDictionary2[elementText].custom_format.lineHeight;
            element.style.wordSpacing =
                nameDictionary2[elementText].custom_format.wordSpacing;
            element.style.whiteSpace =
                nameDictionary2[elementText].custom_format.whiteSpace;
        }
        else {
            // If the player does not have a record in the name dictionary, reset the format
            element.style.color = "";
            element.style.fontSize = "";
            element.style.fontWeight = "";
            element.style.backgroundColor = "";
            element.style.textDecoration = "";
            element.style.textTransform = "";
            element.style.textShadow = "";
            element.style.textIndent = "";
            element.style.letterSpacing = "";
            element.style.lineHeight = "";
            element.style.wordSpacing = "";
            element.style.whiteSpace = "";
        }
    });
}
// Function to add the "Join as Spectator" button
function addSpectatorButton() {
    // Check if the URL already contains "/?spectate=true"
    if (window.location.href.includes("/?spectate=true")) {
        return; // Do not add the button if it's already present in the URL
    }
    const targetDiv = document.querySelector(".flex.py-6");
    if (targetDiv && !document.getElementById("spectatorButton")) {
        const spectatorButton = document.createElement("button");
        spectatorButton.textContent = "Spectate";
        spectatorButton.id = "spectatorButton";
        // Copy styling from the provided button class
        spectatorButton.className =
            "flex justify-center px-4 rounded items-center hover:no-underline bg-st-purple-light hover:bg-st-purple-normal text-white h-10";
        spectatorButton.style.lineHeight = "100%";
        spectatorButton.style.marginLeft = "0.75rem";
        spectatorButton.addEventListener("click", function () {
            // Reload the page with "?spectate=true" appended to the URL
            window.location.href = window.location.href + "/?spectate=true";
        });
        targetDiv.appendChild(spectatorButton);
    }
}
function getCameraDiv() {
    return document.querySelector("div.flex-1.flex.flex-row.w-full.h-full.flex-wrap.justify-center.max-h-full");
}
function getPlayerDiv(n) {
    var _a, _b;
    return (_b = (_a = getCameraDiv()) === null || _a === void 0 ? void 0 : _a.children[n]) !== null && _b !== void 0 ? _b : null;
}
function getPlayerStatusDiv(n) {
    var _a, _b;
    return (_b = (_a = getPlayerDiv(n)) === null || _a === void 0 ? void 0 : _a.querySelector("div.absolute.inset-x-0.top-0.block.z-30")) !== null && _b !== void 0 ? _b : null;
}
function getPlayerLifeTotalInput(n) {
    var _a, _b;
    return (_b = (_a = getPlayerStatusDiv(n)) === null || _a === void 0 ? void 0 : _a.querySelector("input.bg-transparent.font-bold.text-center.select-auto.text-white.text-3xl")) !== null && _b !== void 0 ? _b : null;
}
function getPlayerLifeTotal(n) {
    const input = getPlayerLifeTotalInput(n);
    if (input === null)
        return null;
    const value = Number(input.value);
    if (isNaN(value))
        return null;
    return value;
}
const inputSelector = "input.bg-transparent.font-bold.text-center.select-auto.text-white.text-3xl";
const observerOptions = {
    attributes: true,
    attributeOldValue: true,
    attributeFilter: ["value"],
};
const observers = {};
function observeInputs() {
    const inputs = document.querySelectorAll(inputSelector);
    inputs.forEach((input) => {
        const id = input.id || input.name ||
            Math.random().toString(36).substring(2); // Generate a unique id for the input
        if (!observers[id]) {
            const observer = new MutationObserver((mutationsList, observer) => {
                for (const mutation of mutationsList) {
                    if (mutation.type === "attributes" && mutation.attributeName === "value") {
                        if (!clickAudio.ended) {
                            clickAudio.pause();
                            clickAudio.currentTime = 0;
                        }
                        clickAudio.play();
                    }
                }
            });
            observer.observe(input, observerOptions);
            observers[id] = observer;
        }
    });
}
const clickAudio = new Audio("https://assets.mixkit.co/active_storage/sfx/2568/2568.wav");
clickAudio.volume = 0.2;
clickAudio.playbackRate = 2;
function getPlayerInfo(n) {
    var _a, _b, _c, _d, _e;
    const div = getPlayerStatusDiv(n);
    const name = (_a = div === null || div === void 0 ? void 0 : div.querySelector("div.font-bold.flex.flex-row.truncate.items-end.leading-snug.text-sm")) === null || _a === void 0 ? void 0 : _a.innerHTML;
    const pronouns = (_b = div === null || div === void 0 ? void 0 : div.querySelector("div.px-2.truncate.leading-snug.text-sm")) === null || _b === void 0 ? void 0 : _b.innerHTML;
    const commander = (_d = (_c = div === null || div === void 0 ? void 0 : div.querySelector("div.text-xs.italic.text-gray-400.truncate.leading-snug.flex.justify-end")) === null || _c === void 0 ? void 0 : _c.children[0]) === null || _d === void 0 ? void 0 : _d.innerHTML;
    const life = (_e = getPlayerLifeTotal(n)) !== null && _e !== void 0 ? _e : undefined;
    return {
        name,
        pronouns,
        commander,
        life,
    };
}
function addReportButton() {
    const playerDropdownDiv = document.querySelectorAll("div .bg-surface-high.rounded.text-sm.shadow-lg.py-1.w-40");
    if (playerDropdownDiv && !document.getElementById("ReportButton")) {
        const reportButton = document.createElement("button");
        reportButton.textContent = "Pals Report";
        reportButton.id = "ReportButton";
        reportButton.className =
            "text-left w-full px-4 cursor-pointer transition-all ease-in-out duration-200 hover:bg-red-700 hover:text-white py-1 text-xs";
        reportButton.style.color = "red";
        reportButton.onmouseover = () => {
            reportButton.style.color = "white";
        };
        reportButton.onmouseout = () => {
            reportButton.style.color = "red";
        };
        reportButton.addEventListener("click", () => {
            const reason = prompt(`Please enter the reason for reporting ${currentReportedPlayer}.`);
            if (reason !== null) {
                chrome.runtime.sendMessage({
                    action: "reportPlayer",
                    data: {
                        reportedUser: currentReportedPlayer,
                        "reason": reason,
                        "sessionID": window.location.pathname,
                    },
                });
            }
        });
        for (const div of playerDropdownDiv) {
            div.appendChild(reportButton);
        }
    }
}
// Set up an interval to execute main function every second
const intervalId = setInterval(() => {
    main();
    observeInputs();
}, 1000);
