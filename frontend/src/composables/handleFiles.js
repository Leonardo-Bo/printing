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

// const getFileName = (value) => {
//     return value.split('/').at(-1)
// }

// const getFileSize = (value) => {
//     let ext
//     if (value < 512000) {
//         value = value / 1024.0
//         ext = 'kB'
//     } 
//     else if (value < 4194304000) {
//         value = value / 1048576.0
//         ext = 'MB'
//     }
//     else {
//         value = value / 1073741824.0
//         ext = 'GB'
//     }
//     return Math.round(value * 10) / 10 + ext
// }

// export default { getFileName, getFileSize }