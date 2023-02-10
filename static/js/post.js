/* jshint esversion: 11 */
//activates fullScreen function with each btn
fullScreenBtns.forEach(btn => {
  btn.addEventListener("click", e => {
    fullScreen(e.target);
  });
});

//#### Init display preview card ####
document.addEventListener('DOMContentLoaded', () => {
  //show avg-rating stars
  starContainers.forEach(container => {
    displayAvgRating(container);
  });
  // show content on preview cards
  displayPreviewCards();
});