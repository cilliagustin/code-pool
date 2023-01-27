// #### STAR BTN CONTROL ####
// Fill stars on hover
starBtns.forEach(btn=>{
    btn.addEventListener('mouseover', (e)=>{
        /* gets value of hovered star and pass it
         to compareVal function */
        const val = e.target.getAttribute("value");
        starBtns.forEach(btn=>{
            compareVal(btn, val)
        })
    })
})

/* trigger fillUserRating function when mouse
leaves stars to return to original value */
starBtns.forEach(btn=>{
    btn.addEventListener('mouseleave', fillUserRating)
})

/**
 * Checks the value (data rating) and
 * triggers the compareVal function. If the
 * value is not a number (None) it gives the stars
 * a gray outline and empty icon
 */
function fillUserRating(){
    const val = ratingForm.getAttribute("data-rating");
    if(!isNaN(val)){
        starBtns.forEach(btn=>{
            compareVal(btn, val)
        })
    } else {
        starBtns.forEach(btn=>{
            btn.firstChild.classList.remove("fa-solid");
            btn.firstChild.classList.add("fa-regular", "text-secondary");
        })
    }
}

/** 
 * compares the value given with the value of
 * each button. If the button value is eual or
 * less to the given value gives a yellow outline
 * and filled star icon, otherwise a gray outline
 * and empty star icon
*/
function compareVal(btn, val){
    if(btn.getAttribute("value") <= val){
        btn.firstChild.classList.remove("fa-regular", "text-secondary");
        btn.firstChild.classList.add("fa-solid");
    } else {
        btn.firstChild.classList.remove("fa-solid");
        btn.firstChild.classList.add("fa-regular", "text-secondary");
    }
}

// #### COPY CODE TO CLIPBOARD
copyBtns.forEach(btn=>{
    btn.addEventListener("click", e =>{
        /* Gets code type of target and finds textArea
        with same code type, copies the text to clipboard
        and triggers alert*/
        const codeType = e.target.previousElementSibling.getAttribute("data-code-type");
        const code = document.querySelector(`textarea[data-code-type="${codeType}"]`);
        code.select();
        code.setSelectionRange(0, 99999); // For mobile devices
        navigator.clipboard.writeText(code.value);

        // Alert the copied text

        const alertPlaceholder = document.querySelector("#liveAlertPlaceholder");
        const content = '<div class="alert alert-success alert-dismissible" role="alert"><p>Text copied!</p><button type="button" class="btn-close" data-bs-dismiss="alert" onclick="closePopUp()"></button></div>'
        if (alertPlaceholder.innerHTML.length === 0) {
            createPopUp(content);
        } else {
            closePopUp();
            createPopUp(content);
        }

    })
})

/**
 * Creates alert and set timeout to close it
 */
function createPopUp(content) {
    const alertPlaceholder = document.querySelector("#liveAlertPlaceholder");
    alertPlaceholder.innerHTML = content;
    timeoutToClose = setTimeout(closePopUp, 2000);
}

let timeoutToClose;

/**
 * Clears timeout if exists and deletes content
 */
function closePopUp() {
    clearTimeout(timeoutToClose);
    let popUpContent = document.querySelector("#liveAlertPlaceholder");
    if (popUpContent.innerHTML.length >0) {
        popUpContent.innerHTML = "";
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