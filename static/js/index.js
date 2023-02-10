/* jshint esversion: 11 */
// #### Typewritter effect ####
function initTypewriter() {
  const titleWord = document.getElementById("title-word");
  const words = ["code", "ideas", "knowledge"];
  type(titleWord, words);
}

function type(titleWord, words) {
  let txt = '';
  let wordIndex = 0;
  let isDeleting = false;

  const typing = () => {
    const current = wordIndex % words.length;
    const fullTxt = words[current];

    // Check if deleting
    if (isDeleting) {
      txt = fullTxt.substring(0, txt.length - 1);
    } else {
      txt = fullTxt.substring(0, txt.length + 1);
    }

    // Insert txt into element
    titleWord.innerHTML = txt;

    // Initial Type Speed
    let typeSpeed = 300;

    if (isDeleting) {
      typeSpeed /= 2;
    }

    // If word is complete
    if (!isDeleting && txt === fullTxt) {
      // Make pause at end
      typeSpeed = 2000;
      // Set delete to true
      isDeleting = true;
    } else if (isDeleting && txt === '') {
      isDeleting = false;
      // Move to next word
      wordIndex++;
      // Pause before start typing
      typeSpeed = 500;
    }

    setTimeout(typing, typeSpeed);
  };

  typing();
}

//activates fullScreen function with each btn
fullScreenBtns.forEach(btn => {
  btn.addEventListener("click", e => {
    fullScreen(e.target);
  });
});

//#### Init index functions ####
document.addEventListener('DOMContentLoaded', () => {
  // Typewriter
  initTypewriter();
  //show avg-rating stars
  starContainers.forEach(container => {
    displayAvgRating(container);
  });
  // show content on preview cards
  displayPreviewCards();
});