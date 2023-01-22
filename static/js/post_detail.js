// #### STAR BTN CONTROL ####
// Fill stars on hover
starBtns.forEach(btn=>{
    btn.addEventListener('mouseover', (e)=>{
        const val = e.target.getAttribute("value");
        starBtns.forEach(btn=>{
            compareVal(btn, val)
        })
    })
})

starBtns.forEach(btn=>{
    btn.addEventListener('mouseleave', fillUserRating)
})

function fillUserRating(){
    const val = ratingForm.getAttribute("data-rating");
    if(!isNaN(val)){
        starBtns.forEach(btn=>{
            compareVal(btn, val)
        })
    }
}

function compareVal(btn, val){
    if(btn.getAttribute("value") <= val){
        btn.firstChild.classList.remove("fa-regular", "text-secondary");
        btn.firstChild.classList.add("fa-solid");
    } else {
        btn.firstChild.classList.remove("fa-solid");
        btn.firstChild.classList.add("fa-regular", "text-secondary");
    }
}

// #### CODE EDITOR BUTTON CONTROL ####
codeEditorBtns.forEach(btn => {
    btn.addEventListener("click", () => {
        toggleEditor(btn)
    })
})

// toggle open/close code editor
function toggleEditor(codeBtn) {
    const dataCodeType = codeBtn.getAttribute("data-code-type");
    const codeElements = document.querySelectorAll(`[data-code-type=${dataCodeType}]`)


    //Toggle open or close elements (1 element open at the time) when width is less than 576px
    if (!mediumMediaQuery.matches) {
        document.querySelectorAll("[data-code-type]").forEach(el => {
            if (el.getAttribute("data-code-type") === dataCodeType) {
                if (el.getAttribute("data-open") === "true") {
                    el.setAttribute("data-open", "false")
                } else {
                    el.setAttribute("data-open", "true")
                }
            } else {
                el.setAttribute("data-open", "false")
            }
        })
    } else {
        //Toggle open or close elements (up to 3 elements open at the time) when width is over 576px
        if (codeBtn.getAttribute("data-open") === "false") {
            codeElements.forEach(el => {
                el.setAttribute("data-open", "true")
            });
        } else {
            codeElements.forEach(el => {
                el.setAttribute("data-open", "false")
            });
        }
    }

    //check if there is an open element
    let openElements = false;
    codeEditorBtns.forEach(btn => {
        if (btn.getAttribute("data-open") === "true") {
            openElements = true;
        }
    })

    if (openElements) {
        codeEditor.setAttribute("data-open", "true");
    } else {
        codeEditor.setAttribute("data-open", "false");
    }
};

function codeEditorWindowResize(mediumMediaQuery) {
    let openElements = false;
    codeEditorBtns.forEach(btn => {
        if (btn.getAttribute("data-open") === "true") {
            openElements = true;
        }
    })

    if (!mediumMediaQuery.matches && codeEditor !== null && openElements) {
        document.querySelectorAll("[data-code-type]").forEach(el => {
            if (el.getAttribute("data-code-type") === "html") {
                el.setAttribute("data-open", "true")
            } else {
                el.setAttribute("data-open", "false")
            }
        })
    }
}

mediumMediaQuery.addEventListener('change', codeEditorWindowResize);


//#### Init post detail functions #### 
document.addEventListener('DOMContentLoaded', () => {
    let iframe = document.querySelector(".code-editor-iframe iframe");
    let htmlCode = document.getElementById("htmlCode").value
    let cssCode = document.getElementById("cssCode").value
    let jsCode = document.getElementById("jsCode").value

    //get the users rating
    fillUserRating();
    // get the avg rating
    displayAvgRating(starContainer);
    // run code editor
    runEditor(iframe, htmlCode, cssCode, jsCode)

});