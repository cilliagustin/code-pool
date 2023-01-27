const mediumMediaQuery = window.matchMedia('(min-width: 576px)');
const largeMediaQuery = window.matchMedia('(min-width: 768px)');
const navbar = document.querySelector("nav");
const navButton = document.getElementById("hamb");
const overlay = document.getElementById("overlay");
const ratingForm = document.getElementById("rating-form");
const starBtns = document.querySelectorAll(".star-btn");
const starContainer = document.getElementById("full-star-container");
const starContainers = document.querySelectorAll(".full-star-container");
const codeEditor = document.getElementById("code-editor");
const copyBtns = document.querySelectorAll(".copy-btn");
const codeEditorBtns = document.querySelectorAll(".code-editor-btn");
const previewCode = document.getElementById("preview-code");
const postTitle = document.getElementById("post-title");
const postSlug = document.getElementById("post-slug");
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
/**
 * takes value from variables htmlCode, cssCode and jsCode and
 * writes the code inside the iframe
*/
function runEditor(iframe, htmlCode, cssCode, jsCode) {
  const code = `${htmlCode} <style>${cssCode}</style><script>${jsCode}</script>`
  const iframeContent = iframe.contentWindow.document;
  iframeContent.open();
  iframeContent.write(code);
  iframeContent.close();
}

// #### DISPLAY AVG RATING ####
/**
 * gets the average rating and gives opacity 1 to 
 * the hidden stars. If the number has decimals the 
 * last star gets cut to display only that percentage
 */
function displayAvgRating(container){
  let val = container.getAttribute("data-avg-rating");
  let integer = parseInt((val.charAt(0)));
  let digits = (val.substring(2,4));
  let stars = container.querySelectorAll("i");
  stars.forEach(star=>{
    if(star.getAttribute("data-value") <= integer + 1){
      star.style.opacity = "1";
    } else {
      star.style.opacity = "0";
    }
  })
  if(integer < 5){
    stars[integer].style.clipPath = `polygon(0 0, ${digits}% 0, ${digits}% 100%, 0% 100%)`;
  }
}

// #### Display preview cards ####
//Used on index and post templates
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

// #### init general functions
// Init addYear On DOM Load
document.addEventListener('DOMContentLoaded', addYear);
