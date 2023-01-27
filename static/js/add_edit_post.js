// #### SLUGIFY ####
/**
 * Transforms text to slug, deletes special characters
 * turns uppercase to lowercase and deletes doubles "-"
 */
function slugify(title, slug) {
    let str = title.value;
    str = str.replace(/^\s+|\s+$/g, ''); // trim
    str = str.toLowerCase();

    // remove accents, swap ñ for n, etc
    let from = "àáäâèéëêìíïîòóöôùúüûñç·/_,:;";
    let to = "aaaaeeeeiiiioooouuuunc------";
    for (let i = 0, l = from.length; i < l; i++) {
        str = str.replace(new RegExp(from.charAt(i), 'g'), to.charAt(i));
    }

    str = str.replace(/[^a-z0-9 -]/g, '') // remove invalid chars
        .replace(/\s+/g, '-') // collapse whitespace and replace by -
        .replace(/-+/g, '-'); // collapse dashes

    slug.value = str;
}

// Trigger slugify
postTitle.addEventListener('input', () => {
    slugify(postTitle, postSlug)
})


// #### PREVIEW CODE ####
previewCode.addEventListener('click', (e) => {
    e.preventDefault()
    // show hidden iframe
    document.querySelector('.create-edit-iframe-container').classList.add('open');

    //get data
    let htmlCode = document.querySelector('.HTML-code').value;
    let cssCode = document.querySelector('.CSS-code').value;
    let jsCode = document.querySelector('.JS-code').value;
    let iframe = document.querySelector('iframe');
    //call runEditor function
    runEditor(iframe, htmlCode, cssCode, jsCode);
})