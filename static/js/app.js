// Front-end logic: switch tabs, send the form to Flask, show the QR code.

const tabs = document.querySelectorAll(".tab");
const textForm = document.getElementById("form-text");
const contactForm = document.getElementById("form-contact");
const contentInput = document.getElementById("content");
const sizeInput = document.getElementById("size");
const sizeLabel = document.getElementById("size-label");
const generateBtn = document.getElementById("generate");
const errorBox = document.getElementById("error");
const placeholder = document.getElementById("placeholder");
const qrImage = document.getElementById("qr-image");
const downloadLink = document.getElementById("download");

let currentType = "text";

const hints = {
  text: "Type or paste anything",
  url: "example.com or https://example.com",
};

function showError(message) {
  errorBox.textContent = message;
  errorBox.hidden = false;
}

function clearError() {
  errorBox.hidden = true;
  errorBox.textContent = "";
}

// Switching tabs just swaps which fields are visible
tabs.forEach((tab) => {
  tab.addEventListener("click", () => {
    currentType = tab.dataset.type;

    tabs.forEach((t) => {
      const active = t === tab;
      t.classList.toggle("active", active);
      t.setAttribute("aria-selected", String(active));
    });

    const isContact = currentType === "contact";
    textForm.hidden = isContact;
    contactForm.hidden = !isContact;
    if (!isContact) contentInput.placeholder = hints[currentType];

    clearError();
  });
});

sizeInput.addEventListener("input", () => {
  sizeLabel.textContent = `${sizeInput.value} px`;
});

// Collect whatever the current tab needs into one object
function buildRequest() {
  const body = { type: currentType, size: Number(sizeInput.value) };

  if (currentType === "contact") {
    body.contact = {
      name: document.getElementById("c-name").value,
      phone: document.getElementById("c-phone").value,
      email: document.getElementById("c-email").value,
      organization: document.getElementById("c-org").value,
    };
  } else {
    body.content = contentInput.value;
  }
  return body;
}

async function generate() {
  clearError();
  generateBtn.disabled = true;
  generateBtn.textContent = "Generating...";

  try {
    const response = await fetch("/api/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(buildRequest()),
    });
    const data = await response.json();

    if (!response.ok) {
      showError(data.error || "Something went wrong. Please try again.");
      return;
    }

    qrImage.src = data.image;
    qrImage.width = Math.min(data.size, 400); // keep it from overflowing the card
    downloadLink.href = data.image;

    placeholder.hidden = true;
    qrImage.hidden = false;
    downloadLink.hidden = false;
  } catch (err) {
    showError("Couldn't reach the server. Is it still running?");
  } finally {
    generateBtn.disabled = false;
    generateBtn.textContent = "Generate QR code";
  }
}

generateBtn.addEventListener("click", generate);

// Ctrl/Cmd + Enter is a handy shortcut when typing in the big text box
contentInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && (event.ctrlKey || event.metaKey)) generate();
});
