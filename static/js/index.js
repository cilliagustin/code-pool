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



//#### Init index functions ####
document.addEventListener('DOMContentLoaded', ()=>{
    // Typewriter
    initTypewriter()
    // show content on preview cards
    displayPreviewCards()
});
