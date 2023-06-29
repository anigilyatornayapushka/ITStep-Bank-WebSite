const btnContinue = document.querySelector("#continue")
const emailInput = document.querySelector("#email")
const genderInput = document.querySelector("#gender")
const fullnameInput = document.querySelector("#fullname")

const maleHint = document.querySelector("#male-hint")
const femaleHint = document.querySelector("#female-hint")

maleHint.addEventListener("click", () => {
    genderInput.value = "Male"
    maleHint.style.display = "none"
    femaleHint.style.display = "none"
})

femaleHint.addEventListener("click", () => {
    genderInput.value = "Female"
    maleHint.style.display = "none"
    femaleHint.style.display = "none"
})

genderInput.addEventListener("focus", () => {
    genderInput.value = ""
    maleHint.style.display = "inline-block"
    femaleHint.style.display = "inline-block"
})

function toName(str) {
    return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase()
}

let btnActive = false

let userEmail

btnContinue.addEventListener("click", () => {
    if (btnActive === true) {
        return
    }

    btnActive = true

    let fullnameSplit = fullnameInput.value.split(" ")
    if (fullnameSplit.length != 2) {
        btnActive = false
        return
    }

    let gender = genderInput.value.toLowerCase()

    if (gender === "male") {
        gender = 1
    } else if (gender === "female") {
        gender = 2
    } else {
        btnActive = false
        return
    }

    let lastName = toName(fullnameSplit[0])
    let firstName = toName(fullnameSplit[1])

    let data = {
        "email": emailInput.value,
        "last_name": lastName,
        "first_name": firstName,
        "gender": gender
    }

    btnContinue.style.cssText = "background: rgb(133, 160, 224)"
    btnContinue.innerText = "Please wait a little"
    setTimeout(() => {
        btnContinue.style.cssText += "background: none; transition: 1.5s"
    }, 100)

    setTimeout(() => {
        axios.post("http://127.0.0.1:8000/api/v1/auth/password-recovery/", data)
        .then(() => {
            userEmail = emailInput.value

            emailInput.value = ""
            fullnameInput.value = ""
            genderInput.value = ""
            maleHint.style.display = "inline-block"
            femaleHint.style.display = "inline-block"
            btnContinue.style.cssText = "background: rgb(40, 167, 79)"
            btnContinue.innerText = "Continue"
            setTimeout(() => {
                btnContinue.style.cssText += "background: none; transition: 1.5s"
            }, 100)
            setTimeout(() => {
                btnContinue.style = null
                enterCodeOne()
            }, 1500)
        })
        .catch(() => {
            emailInput.value = ""
            fullnameInput.value = ""
            genderInput.value = ""
            maleHint.style.display = "inline-block"
            femaleHint.style.display = "inline-block"
            btnContinue.style.cssText = "background: rgb(220, 53, 69)"
            btnContinue.innerText = "Continue"
            setTimeout(() => {
                btnContinue.style.cssText += "background: none; transition: 1.5s"
            }, 100)
            setTimeout(() => {
                btnContinue.style = null
                setTimeout(() => {
                    btnActive = false
                }, 3000);
            }, 1600)
        })
    }, 1200)
})

function enterCodeOne() {
    let container = document.querySelector(".center-bottom")

    let wall = document.createElement("div")
    wall.className = "wall"

    container.append(wall)

    setTimeout(() => {
        wall.style.height = "100%"
        setTimeout(() => {
            enterCodeTwo()
            setTimeout(() => {
                let wall = container.querySelector(".wall")
                wall.style = ""
                setTimeout(() => {
                    container.removeChild(wall)
                    btnActive = false
                }, 3000)
            }, 100)
        }, 3000)
    }, 50)
}

function enterCodeTwo() {
    let container = document.querySelector(".center-bottom")

    let req = container.querySelector(".req-format")
    if (req) {
        container.removeChild(req)
        container.innerHTML += `<p>Enter code here</p>
                                <div class="beautiful-input-box">
                                    <div>
                                        <input type="text" class="square" maxlength="6" name="code">
                                    </div>
                                    <div>
                                        <input type="text" class="square" maxlength="5">
                                    </div>
                                    <div>
                                        <input type="text" class="square" maxlength="4">
                                    </div>
                                    <div>
                                        <input type="text" class="square" maxlength="3">
                                    </div>
                                    <div>
                                        <input type="text" class="square" maxlength="2">
                                    </div>
                                    <div>
                                        <input type="text" class="square" maxlength="1">
                                    </div>
                                </div>
                                <button id="reset-psw">Continue</button>`

        let inputGaps = container.querySelectorAll(".square")
    
        for (let i = 0; i < 6; i++) {
            let gap = inputGaps[i]
    
            gap.addEventListener("input", () => {
                wrapWords(i)
            })
            gap.addEventListener("keydown", event => {
                if (event.code === "ArrowRight" && i < 5) {
                    inputGaps[i+1].focus()
                } else if (event.code === "ArrowLeft" && i > 0) {
                    inputGaps[i-1].focus()
                }
            })
        }
    
        function wrapWords(i) {
            let text = inputGaps[i].value
    
            inputGaps[i].style.cssText = "border: 1px solid rgb(180, 180, 180)" 
    
            if (text.length > 1 && i < 9) {
                inputGaps[i+1].value = text.substring(1)
                inputGaps[i].value = text[0]
                inputGaps[i+1].focus()
                wrapWords(i+1)
            } else if (text.length == 1) {
                inputGaps[i].value = text[0]
            } else if (text.length == 0 && i > 0) {
                inputGaps[i-1].focus()
            }
        }
    }

    function getCode() {
        let inputGaps = container.querySelectorAll(".square")
        let code = ""
        for (gap of inputGaps) {
            code += gap.value
        }
        return code
    }

    let btn = container.querySelector("button")

    btn.addEventListener("click", () => {
        let inputGaps = container.querySelectorAll(".square")
        let code = getCode()

        if (code.length === 6) {
            for (gap of inputGaps) {
                gap.value = ""
            }
            btn.innerText = "Plase wait a little"
            btn.style.cssText = "background: rgb(133, 160, 224)"

            changePswrdCode = code
            enterNewPassword()
        }
    })
}

let changePswrdCode

function enterNewPassword() {
    let container = document.querySelector(".center-bottom")

    let wall = document.createElement("div")
    wall.className = "wall"

    container.append(wall)

    setTimeout(() => {
        wall.style.height = "100%"
        setTimeout(() => {
            enterCodeThree()
            setTimeout(() => {
                let wall = container.querySelector(".wall")
                wall.style = ""
                setTimeout(() => {
                    container.removeChild(wall)
                    btnActive = false
                }, 3000)
            }, 100)
        }, 3000)
    }, 50)
}

function enterCodeThree() {
    let container = document.querySelector(".center-bottom")

    let extraOne = container.querySelector("p")
    let extraTwo = container.querySelector(".beautiful-input-box")
    let extraThree = container.querySelector("button")
    if (extraOne && extraTwo && extraThree) {
        container.removeChild(extraOne)
        container.removeChild(extraTwo)
        container.removeChild(extraThree)
        container.innerHTML += `<input class="new-psw-input" type="password" placeholder="new password">
                                <input class="new-psw-input" type="password" placeholder="repeat password">
                                <button class="new-psw-input" id="change-password">Submit</button>`
        let inputPswrdOne = container.querySelectorAll("input")[0]
        let inputPswrdTwo = container.querySelectorAll("input")[1]
        let btn = container.querySelector("button")

        btn.addEventListener("click", () => {

            let data = {
                "code": changePswrdCode,
                "email": userEmail,
                "password": inputPswrdOne.value,
                "password2": inputPswrdTwo.value
            }
            btn.style.cssText = "background: rgb(133, 160, 224)"
            btn.innerText = "Please wait a little"
            setTimeout(() => {
                btn.style.cssText += "background: none; transition: 1.5s"
            }, 100)
            setTimeout(() => {
                axios.post("http://127.0.0.1:8000/api/v1/auth/password-recovery/confirmation/", data)
                .then(() => {
                    btn.style.cssText = "background: rgb(40, 167, 79)"
                    btn.innerText = "Success"
                })
                .catch(() => {
                    btn.style.cssText = "background: rgb(220, 53, 69)"
                    btn.innerText = "Failed"
                    setTimeout(() => {
                        btn.style.cssText += "background: none; transition: 1.5s"
                    }, 100)
                    setTimeout(() => {
                        btn.style = null
                    }, 1600)
                })
            }, 1500)
        })
    }
}
