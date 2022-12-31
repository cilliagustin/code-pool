const mediumMediaQuery = window.matchMedia('(min-width: 576px)');
const largeMediaQuery = window.matchMedia('(min-width: 768px)');
const navbar = document.querySelector("nav");
const navButton = document.getElementById("hamb");
const overlay = document.getElementById("overlay");
const codeEditor = document.getElementById("code-editor");
const codeEditorBtns = document.querySelectorAll(".code-editor-btn");
const authFormInputs = document.querySelectorAll(".auth-card form p input[type='text'], .auth-card form p input[type='password'], .auth-card form p input[type='email']")


// ##### GENERAL FUNCTIONS #####

// #### NAVBAR ####
//  Navbar collapse 
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
function navbarWindowResize(largeMediaQuery) {
  if (largeMediaQuery.matches) {
    navbar.setAttribute("data-open", "false");
    overlay.setAttribute("data-open", "false");
  }
};
largeMediaQuery.addEventListener('change', navbarWindowResize);

// #### FOOTER ####
// add year to footer
function addYear() {
  document.getElementById("footerYear").innerHTML = new Date().getFullYear();
}

// #### CODE EDITOR FUNCTION ####
function runEditor(iframe, htmlCode, cssCode, jsCode) {
  const code = `${htmlCode} <style>${cssCode}</style><script>${jsCode}</script>`
  const iframeContent = iframe.contentWindow.document;
  iframeContent.open();
  iframeContent.write(code);
  iframeContent.close();
}

// #### init general functions
// Init addYear On DOM Load
document.addEventListener('DOMContentLoaded', addYear);


// ##### INDEX #####

// #### Typewritter effect ####
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
  new TypeWriter(titleWord, words);
}

// #### Display preview cards ####
function displayPreviewCards(){
  let previewCards = document.querySelectorAll(".preview-card");
  previewCards.forEach(card =>{
    let htmlCode = card.querySelector(".preview-card-body [data-code-html]").value;
    let cssCode = card.querySelector(".preview-card-body [data-code-css]").value;
    let jsCode = card.querySelector(".preview-card-body [data-code-js]").value;
    let iframe = card.querySelector(".preview-card-body iframe");
    runEditor(iframe, htmlCode, cssCode, jsCode)
  })
}

//#### Init index functions ####
function runIndexFunctions(){
  if(document.querySelector(".main-banner") !== null){
    initTypewriter()
    displayPreviewCards()
  }
}

document.addEventListener('DOMContentLoaded', runIndexFunctions);


// ##### POST DETAILS #####

// #### CODE EDITOR BUTTON CONTROL ####
codeEditorBtns.forEach(btn =>{
  btn.addEventListener("click", ()=>{
    toggleEditor(btn)
  })
})

// toggle open/close code editor
function toggleEditor(codeBtn){
  const dataCodeType = codeBtn.getAttribute("data-code-type");
  const codeElements = document.querySelectorAll(`[data-code-type=${dataCodeType}]`)
  

  //Toggle open or close elements (1 element open at the time) when width is less than 576px
  if (!mediumMediaQuery.matches){
    document.querySelectorAll("[data-code-type]").forEach(el =>{
      if(el.getAttribute("data-code-type") === dataCodeType){
        if(el.getAttribute("data-open") === "true"){
          el.setAttribute("data-open", "false")
        } else{
          el.setAttribute("data-open", "true")
        }  
      } else {
        el.setAttribute("data-open", "false")
      }
    })
  }else{
    //Toggle open or close elements (up to 3 elements open at the time) when width is over 576px
    if(codeBtn.getAttribute("data-open") === "false"){
      codeElements.forEach(el =>{
        el.setAttribute("data-open", "true")
      });
    } else{
      codeElements.forEach(el =>{
        el.setAttribute("data-open", "false")
      });
    }
  }

  //check if there is an open element
  let openElements = false;
  codeEditorBtns.forEach(btn =>{
    if(btn.getAttribute("data-open") === "true"){
      openElements =true;
    } 
  })

  if(openElements){
    codeEditor.setAttribute("data-open", "true");
  } else {
    codeEditor.setAttribute("data-open", "false");
  }
};

function codeEditorWindowResize(mediumMediaQuery){
  let openElements = false;
  codeEditorBtns.forEach(btn =>{
    if(btn.getAttribute("data-open") === "true"){
      openElements =true;
    } 
  })

  if(!mediumMediaQuery.matches && codeEditor !== null && openElements){
    document.querySelectorAll("[data-code-type]").forEach(el =>{
      if(el.getAttribute("data-code-type") === "html"){
        el.setAttribute("data-open", "true")
      } else {
        el.setAttribute("data-open", "false")
      }
    })
  }
}

//#### Init post detail functions ####
function postDetailFunctions(){
  if(codeEditor !== null){
    let iframe = document.querySelector(".code-editor-iframe iframe");
    let htmlCode = document.getElementById("htmlCode").value
    let cssCode = document.getElementById("cssCode").value
    let jsCode = document.getElementById("jsCode").value

    console.log(htmlCode)
    console.log(cssCode)
    console.log(jsCode)

    runEditor(iframe, htmlCode, cssCode, jsCode)
    
  }
}

document.addEventListener('DOMContentLoaded', postDetailFunctions);


mediumMediaQuery.addEventListener('change', codeEditorWindowResize);
