function formatDate(date) {
    return date.getDate() + "." + (date.getMonth() + 1) + "." + date.getFullYear();
}


function addZeros(i) {
    if (i < 10) {
        return "0" + i;
    } else {
        return "" + i;
    }
}

function formatDateForDjango(date) {
    return "" + date.getFullYear() + "/" + addZeros(date.getMonth() + 1) + "/" + addZeros(date.getDate()) + "/";

}

function getNow() {
    return new Date();
}

function getNowFormatted() {
    return formatDate(getNow());
}

function getJSONScript(elementId) {
    return JSON.parse(document.getElementById(elementId).textContent);
}

