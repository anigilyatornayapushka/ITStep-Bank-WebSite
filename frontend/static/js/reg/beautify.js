// const form = document.querySelector(".registration-form")
// const btn = document.querySelector("#register")

let inActive = false;

btn.addEventListener("click", event => {
    event.preventDefault()

    if (inActive === true || !agreeCheckbox.checked) {
        return;
    }
    else {
        inActive = true
        startLoading()
    }
})

function startLoading() {
    let bar1 = document.createElement("div")
    let bar2 = document.createElement("div")
    let bar3 = document.createElement("div")
    let bar4 = document.createElement("div")
    let bar5 = document.createElement("div")

    bar1.className = "bar"
    bar2.className = "bar"
    bar3.className = "bar"
    bar4.className = "bar"
    bar5.className = "bar"

    bar1.style.cssText = `
        height: 2px; width: 0px;
        background: rgb(49, 203, 210);
        position: absolute;
        top: 0px; left: 190px;
    `

    bar2.style.cssText = `
        height: 0px; width: 2px;
        background: rgb(49, 203, 210);
        position: absolute;
        top: 0px; right: 0;
    `

    bar3.style.cssText = `
        height: 2px; width: 0px;
        background: rgb(49, 203, 210);
        position: absolute;
        bottom: 0px; right: 0px;
    `

    bar4.style.cssText = `
        height: 0px; width: 2px;
        background: rgb(49, 203, 210);
        position: absolute;
        bottom: 0px; left: 0;
    `

    bar5.style.cssText = `
        height: 2px; width: 0px;
        background: rgb(49, 203, 210);
        position: absolute;
        top: 0px; left: 0;
    `

    form.append(bar1)

    setTimeout(() => {
        bar1.style.cssText += "width: 190px; transition: width 0.6s;";
    }, 50);

    form.append(bar2)

    setTimeout(() => {
        bar2.style.cssText += "height: 100%; transition: height 0.6s;";
    }, 600);

    form.append(bar3)

    setTimeout(() => {
        bar3.style.cssText += "width: 380px; transition: width 0.6s;";
    }, 1200);

    form.append(bar4)

    setTimeout(() => {
        bar4.style.cssText += "height: 100%; transition: height 0.6s;";
    }, 1800);

    form.append(bar5)

    setTimeout(() => {
        bar5.style.cssText += "width: 190px; transition: width 0.6s;";
    }, 2400);

    setTimeout(() => {
        if (inActive === true) {
            removeBars()
            startLoading()
        }
    }, 3100)
}

function removeBars() {
    let allBars = form.querySelectorAll(".registration-form .bar")
    for (bar of allBars) {
        form.removeChild(bar)
    }
}

function stopLoading() {
    removeBars()
    inActive = false
}

const allValidators = document.querySelectorAll("i[name='inner']")

let allDesciptions = [
    "Length > 0",
    "Length > 0",
    "Starts with letter\nTwo characters in main part\nDomain one of:\n\tmail.ru\n\tlist.ru\n\tinbox.ru\n\tgmail.com",
    "At least one number or one character\nLength > 6",
    "Must be the same as previous"
]

for (let i = 0; i < 5; i++) {
    let validator = allValidators[i]
    validator.title = allDesciptions[i]
}
