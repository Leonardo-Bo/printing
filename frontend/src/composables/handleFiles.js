export function getFileName(value) {
    return value.split('/').at(-1)
}

export function getFileSize(value) {
    let ext
    if (value < 512000) {
        value = value / 1024.0
        ext = 'kB'
    } 
    else if (value < 4194304000) {
        value = value / 1048576.0
        ext = 'MB'
    }
    else {
        value = value / 1073741824.0
        ext = 'GB'
    }
    return Math.round(value * 10) / 10 + ext    
}

export function getCopyImage(str) {
    // Create new element
    var el = document.createElement('textarea');
    // Set value (string to be copied)
    el.value = '<img src="' + str + '" width=300px class="center-img">';
    // Set non-editable to avoid focus and move outside of view
    el.setAttribute('readonly', '');
    el.style = {position: 'absolute', left: '-9999px'};
    document.body.appendChild(el);
    // Select text inside element
    el.select();
    // Copy text to clipboard
    document.execCommand('copy');
    // Remove temporary element
    document.body.removeChild(el);

}