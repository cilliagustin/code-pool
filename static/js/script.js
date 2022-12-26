const navbar = document.querySelector("nav");
const navButton = document.getElementById("hamb");
const overlay = document.getElementById("overlay");


// #### NAVBAR ####
// #### Navbar collapse ####

navButton.addEventListener("click",()=>{
    if (navbar.getAttribute("data-open") === "false"){
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
  if(mediaQuery.matches) {
    navbar.setAttribute("data-open", "false");
    overlay.setAttribute("data-open", "false");
}
};
mediaQuery.addEventListener('change', windowResize);

// #### FOOTER ####
// add year to footer
function addYear(){
    document.getElementById("footerYear").innerHTML = new Date().getFullYear();
}

window.onload = addYear



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
      if(this.isDeleting) {
        this.txt = fullTxt.substring(0, this.txt.length - 1);
      } else {
        this.txt = fullTxt.substring(0, this.txt.length + 1);
      }
  
      // Insert txt into element
      this.titleWord.innerHTML = this.txt;
  
      // Initial Type Speed
      let typeSpeed = 300;
  
      if(this.isDeleting) {
        typeSpeed /= 2;
      }
  
      // If word is complete
      if(!this.isDeleting && this.txt === fullTxt) {
        // Make pause at end
        typeSpeed = 3000;
        // Set delete to true
        this.isDeleting = true;
      } else if(this.isDeleting && this.txt === '') {
        this.isDeleting = false;
        // Move to next word
        this.wordIndex++;
        // Pause before start typing
        typeSpeed = 500;
      }
  
      setTimeout(() => this.type(), typeSpeed);
    }
  }
  
  
  // Init On DOM Load
  document.addEventListener('DOMContentLoaded', init);
  
  // Init App
  function init() {
    const titleWord = document.getElementById("title-word");
    const words = ["code", "ideas", "knowledge"];
    // Init TypeWriter
    new TypeWriter(titleWord, words);
  }


