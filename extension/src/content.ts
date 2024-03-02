export { };

type NameDictionaryPlayer = {
  custom_format: {
    color: string;
    fontSize: string;
    fontWeight: string;
    backgroundColor: string;
    textDecoration: string;
    textTransform: string;
    textShadow: string;
    textIndent: string;
    letterSpacing: string;
    lineHeight: string;
    wordSpacing: string;
    whiteSpace: string;
  };
  blocked: boolean;
  reason: string;
  role: string;
};

let nameDictionary: Record<string, NameDictionaryPlayer> = {};
let lastNamesOnPage: string[] = [];
let lastCommandersOnPage: string[] = [];
let playerDropdownButtonListeners: Element[] = [];

let currentReportedPlayer: string | null = null;

function main() {
  addSpectatorButton();
  const playerDropdownButtons = document.querySelectorAll(
    "button.p-1.shadow-md.rounded.text-white.transition-all.ease-in-out.duration-200.bg-surface-high",
  );
  for (
    const dropdown of Array.from(playerDropdownButtons.values()).filter((
      dropdown,
    ) => !playerDropdownButtonListeners.includes(dropdown))
  ) {
    playerDropdownButtonListeners.push(dropdown);
    dropdown.addEventListener("click", () => {
      setTimeout(() => {
        addReportButton();
      }, 10);
      const player = dropdown.parentElement?.parentElement
        ?.parentElement
        ?.querySelector(
          "div.flex-1.overflow-hidden",
        )?.querySelector("div.flex-1")?.querySelector(
          "div.cursor-pointer.text-white.w-full.overflow-hidden",
        )?.querySelector("div.flex.items-center.w-full")?.querySelector(
          "div.font-bold.truncate.leading-snug.text-sm",
        )?.innerHTML;
      if (player !== undefined) {
        currentReportedPlayer = player;
      } else {
        currentReportedPlayer = null;
      }
    });
  }

  // Retrieve the player names
  const nameElements = document.querySelectorAll(
    ".font-bold.truncate.leading-snug.text-sm",
  );
  const namesOnPage: string[] = [];

  nameElements.forEach((element) => {
    const name = element?.textContent?.trim().toLowerCase();
    if (name !== undefined) {
      namesOnPage.push(name);
    }
  });

  // Retrieve the player's commanders
  const commanderElements = document.querySelectorAll(
    ".text-xs.italic.text-gray-400.truncate.leading-snug.flex",
  );
  const commandersOnPage: string[] = [];

  commanderElements.forEach((element) => {
    // If there are no child divs, add two empty strings to the array
    if (!element.children) {
      commandersOnPage.push("", "");
    } else {
      let child;
      if (element.children[0]) {
        child = element?.children[0]?.textContent?.trim();
        if (child !== undefined) commandersOnPage.push(child);
      } // child 1 is a / character
      if (element.children[2]) {
        child = element?.children[2]?.textContent?.trim();
        if (child !== undefined) commandersOnPage.push(child);
      } else {
        commandersOnPage.push("");
      }
    }
  });

  // If there are no names on the page, the active page is probably the game start page
  if (namesOnPage.length !== 0) {
    const allNamesOnPageAreContained =
      JSON.stringify(lastNamesOnPage) === JSON.stringify(namesOnPage);
    const allCommandersAreContained =
      JSON.stringify(lastCommandersOnPage) === JSON.stringify(commandersOnPage);

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
    nameDictionary = message.data;
    formatNames();
  }
});

// Convert all keys in an object to lowercase
const lowerize = (obj: Record<string, any>) =>
  Object.keys(obj).reduce((acc, k) => {
    acc[k.toLowerCase()] = obj[k];
    return acc;
  }, {} as Record<string, string>);

// Format names on the page
function formatNames() {
  lowerize(nameDictionary);
  const elements = document.querySelectorAll(
    ".font-bold.truncate.leading-snug.text-sm",
  );

  elements.forEach((element) => {
    const elementText = element.textContent?.trim().toLowerCase();
    // If the player has a record in the name dictionary, apply the custom format
    if (
      elementText !== undefined &&
      nameDictionary[elementText] &&
      nameDictionary[elementText].custom_format !== null
    ) {
      (element as HTMLElement).style.color =
        nameDictionary[elementText].custom_format.color;
      (element as HTMLElement).style.fontSize =
        nameDictionary[elementText].custom_format.fontSize;
      (element as HTMLElement).style.fontWeight =
        nameDictionary[elementText].custom_format.fontWeight;
      (element as HTMLElement).style.backgroundColor =
        nameDictionary[elementText].custom_format.backgroundColor;
      (element as HTMLElement).style.textDecoration =
        nameDictionary[elementText].custom_format.textDecoration;
      (element as HTMLElement).style.textTransform =
        nameDictionary[elementText].custom_format.textTransform;
      (element as HTMLElement).style.textShadow =
        nameDictionary[elementText].custom_format.textShadow;
      (element as HTMLElement).style.textIndent =
        nameDictionary[elementText].custom_format.textIndent;
      (element as HTMLElement).style.letterSpacing =
        nameDictionary[elementText].custom_format.letterSpacing;
      (element as HTMLElement).style.lineHeight =
        nameDictionary[elementText].custom_format.lineHeight;
      (element as HTMLElement).style.wordSpacing =
        nameDictionary[elementText].custom_format.wordSpacing;
      (element as HTMLElement).style.whiteSpace =
        nameDictionary[elementText].custom_format.whiteSpace;
    } else {
      // If the player does not have a record in the name dictionary, reset the format
      (element as HTMLElement).style.color = "";
      (element as HTMLElement).style.fontSize = "";
      (element as HTMLElement).style.fontWeight = "";
      (element as HTMLElement).style.backgroundColor = "";
      (element as HTMLElement).style.textDecoration = "";
      (element as HTMLElement).style.textTransform = "";
      (element as HTMLElement).style.textShadow = "";
      (element as HTMLElement).style.textIndent = "";
      (element as HTMLElement).style.letterSpacing = "";
      (element as HTMLElement).style.lineHeight = "";
      (element as HTMLElement).style.wordSpacing = "";
      (element as HTMLElement).style.whiteSpace = "";
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
  return document.querySelectorAll(
    "div .flex-1.flex.flex-row.w-full.h-full.flex-wrap.justify-center.max-h-full",
  );
}

function getPlayerDiv(n: number): HTMLDivElement | null {
  return getCameraDiv()[n] as HTMLDivElement ?? null;
}

function getPlayerStatusDiv(n: number): HTMLDivElement | null {
  return getPlayerDiv(n)?.querySelector(
    "div .absolute.inset-x-0.top-0.block.z-30",
  ) ?? null;
}

function getPlayerLifeTotalInput(n: number): HTMLInputElement | null {
  return getPlayerStatusDiv(n)?.querySelector(
    "input bg-transparent.font-bold.text-center.select-auto.text-white.text-3xl",
  ) ?? null;
}

function getPlayerLifeTotal(n: number): number | null {
  const input = getPlayerLifeTotalInput(n);
  if (input === null) return null;
  const value = Number(input.value);
  if (isNaN(value)) return null;
  return value;
}

function addReportButton() {
  const playerDropdownDiv = document.querySelectorAll(
    "div .bg-surface-high.rounded.text-sm.shadow-lg.py-1.w-40",
  );
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
      const reason = prompt(
        `Please enter the reason for reporting ${currentReportedPlayer}.`,
      );
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
const intervalId = setInterval(() => main(), 1000);

const lifeSoundInterval = setInterval(() => {
  console.log(getPlayerLifeTotal(3));
}, 1000);

console.log("starting");

setInterval(() => console.log("hello world"), 1000);
