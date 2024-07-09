window.onload = function loadBg() {
    body = document.getElementById("main-body");
    tempBody1 = document.querySelector(".welcome");
    tempBody2 = document.querySelector(".deptsection")
    tempBody3 = document.querySelector(".viewselected")
    if(tempBody1) {
        body.style.backgroundPosition = "top";
    }
    else if(tempBody2) {
        body.style.backgroundPosition = "center";
    }
    else if(tempBody3) {
        body.style.backgroundPosition = "right top"
    }
}

function uPanel() {
    const node = document.querySelector(".user-link");
    const flex = "flex";
    const none = "none";
    if(node.style.display == none) {
        node.style.display = flex;
    }
    // else if(node.style.display == flex) {
    //     node.style.display = none;
    // }
}

function activateDark() {
    body = document.getElementById("main-body");
    body.style.background = "#000000";
    body.style.color = "#fff";
}

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
function allo() {
    const form = document.querySelector(".create-college");
    document.querySelector(".colleges").style.filter = "opacity(0%)"
    form.style.display = 'flex';
}
function unallo() {
    const form = document.querySelector(".create-college");
    const z = document.querySelector(".colleges");
    z.style.filter = "opacity(100%)";
    document.getElementById("header").style.zIndex = "4";
    form.style.display = 'none';
}
function dropDown() {
    parent = event.currentTarget.parentElement;
    const pp = parent.childNodes;
    drpSymbol = document.querySelectorAll(".drpsymbol");
    const drop = document.querySelectorAll(".dropdown");
    drop.forEach(function(drp) {
        for(let i=0; i<pp.length; i++){
            if(drp == pp[i]){
                if(drp.style.display != "flex") {
                    drp.style.display = "flex";
                    parent.style.height = "auto";
                    drpSymbol.forEach((v)=> {
                        if((v.parentElement == parent) || (v.parentElement.parentElement == parent)){
                            v.innerHTML = "&#x25b2;";
                        }
                    })
                }else{
                    drp.style.display ="none";
                    parent.style.height = "auto";
                    drpSymbol.innerHTML = ";"
                    drpSymbol.forEach((v)=> {
                        if((v.parentElement == parent) || (v.parentElement.parentElement == parent)){
                            v.innerHTML = "&#x25bc;";
                        }
                    })
                }
            }
        }
    })
}

function dropDown2() {
    parent = event.currentTarget.parentElement.parentElement;
    console.log(parent)
    const pp = parent.childNodes;
    drpSymbol = document.querySelectorAll(".drpsymbol");
    const drop = document.querySelectorAll(".dropdown");
    drop.forEach(function(drp) {
        for(let i=0; i<pp.length; i++){
            if(drp == pp[i]){
                if(drp.style.display != "flex") {
                    drp.style.display = "flex";
                    parent.style.height = "auto";
                    drpSymbol.forEach((v)=> {
                        if((v.parentElement == parent) || (v.parentElement.parentElement == parent)){
                            v.innerHTML = "&#x25b2;";
                        }
                    })
                }else{
                    drp.style.display ="none";
                    parent.style.height = "auto";
                    drpSymbol.innerHTML = ";"
                    drpSymbol.forEach((v)=> {
                        if((v.parentElement == parent) || (v.parentElement.parentElement == parent)){
                            v.innerHTML = "&#x25bc;";
                        }
                    })
                }
            }
        }
    })
}

