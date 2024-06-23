function loadForm(){
    const form = document.getElementById("formindex");
    form.style.display = "flex";
    setTimeout(document.getElementById("indextop").style.display = "none",30000);
}
function alllocforms() {
    const form = document.getElementById("invisible");
    document.querySelector(".all-locations").style.filter = "opacity(0%)"
    form.style.display = 'flex';
}
function undofunc() {
    const form = document.getElementById("invisible");
    const z = document.querySelector(".all-locations");
    z.style.filter = "opacity(100%)";
    document.getElementById("header").style.zIndex = "4";
    form.style.display = 'none';
}
