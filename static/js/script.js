const navbar = document.querySelector("nav");
const navButton = document.getElementById("hamb");
const overlay = document.getElementById("overlay");


// #### NAVBAR ####
// #### Navbar collapse ####

navButton.addEventListener("click", () => {
  if (navbar.getAttribute("data-open") === "false") {
    navbar.setAttribute("data-open", "true");
    overlay.setAttribute("data-open", "true");
  } else {
    navbar.setAttribute("data-open", "false");
    overlay.setAttribute("data-open", "false");
  }
});

// close navbar at 768px
const mediaQuery = window.matchMedia('(min-width: 768px)');

function windowResize(mediaQuery) {
  if (mediaQuery.matches) {
    navbar.setAttribute("data-open", "false");
    overlay.setAttribute("data-open", "false");
  }
};
mediaQuery.addEventListener('change', windowResize);

// #### FOOTER ####
// add year to footer
function addYear() {
  document.getElementById("footerYear").innerHTML = new Date().getFullYear();
}

// Init addYear On DOM Load
document.addEventListener('DOMContentLoaded', addYear);



// #### INDEX ####

// Typewritter effect
class TypeWriter {
  constructor(titleWord, words) {
    this.titleWord = titleWord;
    this.words = words;
    this.txt = '';
    this.wordIndex = 0;
    this.type();
    this.isDeleting = false;
  }

  type() {
    const current = this.wordIndex % this.words.length;
    const fullTxt = this.words[current];

    // Check if deleting
    if (this.isDeleting) {
      this.txt = fullTxt.substring(0, this.txt.length - 1);
    } else {
      this.txt = fullTxt.substring(0, this.txt.length + 1);
    }

    // Insert txt into element
    this.titleWord.innerHTML = this.txt;

    // Initial Type Speed
    let typeSpeed = 300;

    if (this.isDeleting) {
      typeSpeed /= 2;
    }

    // If word is complete
    if (!this.isDeleting && this.txt === fullTxt) {
      // Make pause at end
      typeSpeed = 3000;
      // Set delete to true
      this.isDeleting = true;
    } else if (this.isDeleting && this.txt === '') {
      this.isDeleting = false;
      // Move to next word
      this.wordIndex++;
      // Pause before start typing
      typeSpeed = 500;
    }

    setTimeout(() => this.type(), typeSpeed);
  }
}
  // Init typewriter
function initTypewriter() {
  const titleWord = document.getElementById("title-word");
  const words = ["code", "ideas", "knowledge"];
  // Init TypeWriter
  new TypeWriter(titleWord, words);
}



// Display preview cards
function displayPreviewCards(){
  let previewCards = document.querySelectorAll(".preview-card");
  previewCards.forEach(card =>{
    let htmlCode = card.querySelector(".preview-card-body [data-code-html]").innerText;
    let cssCode = card.querySelector(".preview-card-body [data-code-css]").innerText;
    let jsCode = card.querySelector(".preview-card-body [data-code-js]").innerText;
    let iframe = card.querySelector(".preview-card-body iframe");
    runEditor(iframe, htmlCode, cssCode, jsCode)
  })
}




//init index functions
function runIndexFunctions(){
  if(!document.querySelector(".main-banner") === null){
    initTypewriter()
    displayPreviewCards()
  }
}

document.addEventListener('DOMContentLoaded', runIndexFunctions);










// #### CODE EDITOR FUNCTION ####
function runEditor(iframe, htmlCode, cssCode, jsCode) {
  const code = `${htmlCode} <style>${cssCode}</style><script>${jsCode}</script>`
  const iframeContent = iframe.contentWindow.document;
  iframeContent.open();
  iframeContent.write(code);
  iframeContent.close();
}