//#### Init display preview card ####
document.addEventListener('DOMContentLoaded', ()=>{
    //show avg-rating stars
    starContainers.forEach(container=>{
        displayAvgRating(container);
    })
    // show content on preview cards
    displayPreviewCards()
});
