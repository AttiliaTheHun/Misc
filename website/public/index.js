let nastyElvses = sessionStorage.getItem("nastyElvses");
if (nastyElvses === null) {
    nastyElvses = false;
} else {
    nastyElvses = nastyElvses === 'true'; // this is how they parse booleans in JS I guess
    nastyElvses = !nastyElvses; // the function toggles to the other state, so by flipping the value, it will toggle to the current state
    toggleFont();
}

function toggleFont() {
    console.log("toggled")
    if (nastyElvses) {
        changeToDefault();
    } else {
        changeToTengwar();
    }
    sessionStorage.setItem("nastyElvses", nastyElvses);
}

function changeToTengwar() {
    document.body.style.fontFamily = "Tengwar"
    document.querySelector("#font-switch").setAttribute("text", "View in latin script");
    nastyElvses = true;
}

function changeToDefault() {
    document.body.style.fontFamily = "-apple-system, system-ui, sans-serif";
    document.querySelector("#font-switch").setAttribute("text", "View in Tengwar");
    nastyElvses = false;
}
