const navbar = document.querySelector("nav");
const navButton = document.getElementById("hamb");
const overlay = document.getElementById("overlay");


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
