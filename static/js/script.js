const mediumMediaQuery = window.matchMedia('(min-width: 576px)');
const largeMediaQuery = window.matchMedia('(min-width: 768px)');
const navbar = document.querySelector("nav");
const navButton = document.getElementById("hamb");
const overlay = document.getElementById("overlay");
const codeEditor = document.getElementById("code-editor");
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


// ##### CREATE/EDIT POSTS #####

// #### SLUGIFY ####
function slugify(title, slug) {
  let str = title.value;

  str = str.replace(/^\s+|\s+$/g, ''); // trim
  str = str.toLowerCase();

  // remove accents, swap ñ for n, etc
  let from = "àáäâèéëêìíïîòóöôùúüûñç·/_,:;";
  let to   = "aaaaeeeeiiiioooouuuunc------";
  for (let i=0, l=from.length ; i<l ; i++) {
      str = str.replace(new RegExp(from.charAt(i), 'g'), to.charAt(i));
  }

  str = str.replace(/[^a-z0-9 -]/g, '') // remove invalid chars
      .replace(/\s+/g, '-') // collapse whitespace and replace by -
      .replace(/-+/g, '-'); // collapse dashes

  slug.value = str;
}

postTitle.addEventListener('input', ()=>{
  slugify(postTitle, postSlug)
})


// #### PREVIEW CODE ####
previewCode.addEventListener('click', (e)=>{
  e.preventDefault()
  document.querySelector('.create-edit-iframe-container').classList.add('open');

  let htmlCode = document.querySelector('.HTML-code').value;
  let cssCode = document.querySelector('.CSS-code').value;
  let jsCode = document.querySelector('.JS-code').value;
  let iframe = document.querySelector('iframe');
  runEditor(iframe, htmlCode, cssCode, jsCode);
})
