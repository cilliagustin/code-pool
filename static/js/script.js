/* jshint esversion: 11 */
const mediumMediaQuery = window.matchMedia('(min-width: 576px)');
const largeMediaQuery = window.matchMedia('(min-width: 768px)');
const navbar = document.querySelector("nav");
const navButton = document.getElementById("hamb");
const overlay = document.getElementById("overlay");
const fullScreenBtns = document.querySelectorAll(".full-screen-btn");
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
}
largeMediaQuery.addEventListener('change', navbarWindowResize);

// #### FOOTER ####
// add year to footer
function addYear() {
  document.getElementById("footerYear").innerHTML = new Date().getFullYear();
}

// #### FULL SCREEN FUNCTION ####
/**
 * opens a modal that occupies the fullscreen and displays the
 * code in an iframe
 */
function fullScreen(btn) {

  //declare variables
  let htmlCode;
  let cssCode;
  let jsCode;


  // if the page has preview cards get value from those
  if (document.querySelector(".preview-card") !== null) {
    let previewCardBody = btn.parentElement.nextElementSibling;
    htmlCode = previewCardBody.querySelector('[data-code-html]').value;
    cssCode = previewCardBody.querySelector('[data-code-css]').value;
    jsCode = previewCardBody.querySelector('[data-code-js]').value;
    // If the page is code editor get values from there
  } else {
    htmlCode = document.getElementById("htmlCode").value;
    cssCode = document.getElementById("cssCode").value;
    jsCode = document.getElementById("jsCode").value;
  }

  //create modal
  const modal = document.createElement("div");
  modal.setAttribute("id", "full-screen-modal");
  modal.classList.add("d-flex", "flex-column");
  modal.innerHTML = `
  <nav class="d-flex w-100 align-items-center justify-content-between">
  <p>Viewing code on full screen</p>
  <button class="close-iframe"><i class="fa-regular fa-circle-xmark"></i></button>
  </nav>
  <iframe id="full-screen-iframe" src="{% url 'canvas' %}" title="blank canvas"></iframe>`;

  // insert modal before footer
  const footer = document.querySelector("footer");
  document.body.insertBefore(modal, footer);

  //block scroll
  document.body.style.top = `-${window.scrollY}px`;
  document.body.style.position = 'fixed';

  const iframe = document.getElementById("full-screen-iframe");
  // call run editor function
  runEditor(iframe, htmlCode, cssCode, jsCode);
}

//close full screen modal
document.body.addEventListener("click", e => {
  if (e.target.classList.contains("close-iframe")) {
    //close modal
    const modal = document.getElementById("full-screen-modal");
    modal.remove();
    //re-enable body scroll
    const scrollY = document.body.style.top;
    document.body.style.position = '';
    document.body.style.top = '';
    window.scrollTo(0, parseInt(scrollY || '0') * -1);
  }
});


// #### ERROR MODAL (AUTH) ####
//close error modal
document.body.addEventListener("click", e => {
  //if target is close modal button delete modal
  if (e.target.getAttribute("id") === "close-error-modal") {
    e.target.parentElement.remove();
  }
});

// #### CODE EDITOR FUNCTION ####
/**
 * takes value from variables htmlCode, cssCode and jsCode and
 * writes the code inside the iframe
 */
function runEditor(iframe, htmlCode, cssCode, jsCode) {
  const code = `${htmlCode} <style>${cssCode}</style><script>${jsCode}</script>`;
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
function displayAvgRating(container) {
  let val = container.getAttribute("data-avg-rating");
  let integer = parseInt((val.charAt(0)));
  let digits = (val.substring(2, 4));
  let stars = container.querySelectorAll("i");
  stars.forEach(star => {
    if (star.getAttribute("data-value") <= integer + 1) {
      star.style.opacity = "1";
    } else {
      star.style.opacity = "0";
    }
  });
  if (integer < 5) {
    stars[integer].style.clipPath = `polygon(0 0, ${digits}% 0, ${digits}% 100%, 0% 100%)`;
  }
}

// #### Display preview cards ####
//Used on index and post templates
function displayPreviewCards() {
  let previewCards = document.querySelectorAll(".preview-card");
  previewCards.forEach(card => {
    let htmlCode = card.querySelector(".preview-card-body [data-code-html]").value;
    let cssCode = card.querySelector(".preview-card-body [data-code-css]").value;
    let jsCode = card.querySelector(".preview-card-body [data-code-js]").value;
    let iframe = card.querySelector(".preview-card-body iframe");
    runEditor(iframe, htmlCode, cssCode, jsCode);
  });
}

// #### init general functions
// Init addYear On DOM Load
document.addEventListener('DOMContentLoaded', addYear);