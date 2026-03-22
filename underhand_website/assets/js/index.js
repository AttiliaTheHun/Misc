let hallowedAreTheOri = sessionStorage.getItem("hallowedAreTheOri");
if (hallowedAreTheOri === null) {
    hallowedAreTheOri = false;
} else {
    hallowedAreTheOri = hallowedAreTheOri === 'true'; // this is how they parse booleans in JS I guess
    hallowedAreTheOri = !hallowedAreTheOri; // the function toggles to the other state, so by flipping the value, it will toggle to the current state
    toggleFont();
}

function toggleFont() {
    if (hallowedAreTheOri) {
        changeToDefault();
    } else {
        changeToAlteran();
    }
    sessionStorage.setItem("hallowedAreTheOri", hallowedAreTheOri);
}

function changeToAlteran() {
    document.body.style.fontFamily = "Alteran"
    document.querySelector("#font-switch").setAttribute("text", "View in latin script");
    hallowedAreTheOri = true;
}

function changeToDefault() {
    document.body.style.fontFamily = "var(--font-family-main)";
    document.querySelector("#font-switch").setAttribute("text", "View in ancient");
    hallowedAreTheOri = false;
}