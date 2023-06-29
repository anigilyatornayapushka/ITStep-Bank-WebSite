const eye = document.querySelector("#password-eye")
const inputEmail = document.querySelector("#email-input")
const inputPswrd = document.querySelector("#password-input")

eye.addEventListener("click", () => {

    if (inputPswrd.type === "text") {
        inputPswrd.type = "password"
        eye.className = "bi bi-eye-slash"
    } else {
        inputPswrd.type = "text"
        eye.className = "bi bi-eye"
    }
})

inputEmail.addEventListener("focus", () => {
    inputEmail.style.border = "none"
})

inputPswrd.addEventListener("focus", () => {
    inputPswrd.style.border = "none"
})

let fingerprintDisplay = document.querySelector("#fingerprint-display")
let gradientDisplay = document.querySelector("#gradient-print")

let fingerPrintActive = false
let firstTry = false

function defineFingerPrintAnimation(fingerprintDisplay, gradientDisplay) {
    fingerprintDisplay.addEventListener("mousedown", event => {

        fingerPrintActive = true
        firstTry = true
        gradientDisplay.style.cssText = `height: 47px; transition: 1.5s;
                                         background: ${gradientDisplay.style.background}`
        doLoginTimeOut = setTimeout(() => {
            doLogin()
        }, 1600)
    })

    fingerprintDisplay.addEventListener("mouseup", () => {
        if (firstTry) {
            fingerPrintActive = false
            gradientDisplay.style.cssText = `height: 0px; transition: 0.2s;
                                             background: ${gradientDisplay.style.background}`
            clearTimeout(doLoginTimeOut)
        }
    })

    fingerprintDisplay.addEventListener("mouseout", () => {
        if (firstTry) {
            fingerPrintActive = false
            gradientDisplay.style.cssText = `height: 0px; transition: 0.2s;
                                             background: ${gradientDisplay.style.background}`
            clearTimeout(doLoginTimeOut)
        }
    })
}
defineFingerPrintAnimation(fingerprintDisplay, gradientDisplay)

function loginAgain() {
    let container = document.querySelector("#divFour")

    let fingerprintDisplay = container.querySelector("#fingerprint-display")
    let gradientDisplay = document.querySelector("#gradient-print")

    gradientDisplay.style.cssText = null

    let wall = container.querySelector(".login-result-wall")
    wall.style.cssText = null

    setTimeout(() => {
        let text = document.querySelector("#divFour p")

        let extra = container.querySelector(".login-result")
        container.removeChild(extra)

        text.innerHTML = "Click and hold to login!"
        text.style = null

        defineFingerPrintAnimation(fingerprintDisplay, gradientDisplay)
    }, 1050)
}

const rememberMeChecker = document.querySelector("#rememberMe")

function doLogin() {
    let gradientDisplay = document.querySelector("#gradient-print")

    let container = document.querySelector("#divFour")
    let wall
    let remember

    if (rememberMeChecker.checked) {
        remember = true
    } else {
        remember = false
    }

    const fpPromise = import('https://openfpcdn.io/fingerprintjs/v3')
    .then(FingerprintJS => FingerprintJS.load())

    fpPromise
    .then(fp => fp.get())
    .then(result => {
        const visitorId = result.visitorId


        let formdata = new FormData()
        formdata.append("email", inputEmail.value)
        formdata.append("password", inputPswrd.value)
        formdata.append("fingerprint", visitorId)
        formdata.append("remember_me", remember)

        axios.post("http://127.0.0.1:8000/api/v1/auth/token/", formdata)
        .then(() => {
            container.innerHTML += `<div class="login-result">
                                    <i class="bi bi-check2-circle"></i>
                                    <div class="login-result-wall"></div>
                                </div>`
            wall = container.querySelector(".login-result-wall")

            inputEmail.style.border = "1px solid rgb(40, 167, 79)"
            inputPswrd.style.border = "1px solid rgb(40, 167, 79)"

            let text = document.querySelector(".info-p")
            text.style.color = "rgb(40, 167, 79)"
            text.innerText = "You logged in successfully"

            if (gradientDisplay) {
                gradientDisplay.style = ""
            }
            setTimeout(() => {
                if (wall) {
                    wall.style.cssText = "margin-right: -100px"
                }
            }, 200)
            setTimeout(() => {
                loginAgain()
                setTimeout(() => {
                    window.location.href = "/account/"
                }, 1050)
            }, 1500)

            inputEmail.value = ""
            inputPswrd.value = ""
        })
        .catch(() => {
            container.innerHTML += `<div class="login-result bad">
                                    <i class="bi bi-slash-circle"></i>
                                    <div class="login-result-wall bad"></div>
                                </div>`
            wall = container.querySelector(".login-result-wall")

            inputEmail.style.border = "1px solid rgb(220, 53, 69)"
            inputPswrd.style.border = "1px solid rgb(220, 53, 69)"

            let text = document.querySelector(".info-p")
            text.style.color = "rgb(220, 53, 69)"
            text.innerText = "User was not found"

            if (gradientDisplay) {
                gradientDisplay.style = ""
            }
            setTimeout(() => {
                if (wall) {
                    wall.style.cssText = "margin-right: -100px"
                }
            }, 200)
            setTimeout(() => {
                loginAgain()
            }, 1500)
        })
    })
}
