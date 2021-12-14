
function devideParas(){
    let elements = document.getElementsByClassName('toModify')
    for (let element in elements){
        let str = element.innerHTML
        let replacement = '</p><p>'
        element.innerHTML = str.split('\n').join(replacement)
    }
}