const form = document.querySelector(".change-password")

const oldPsw = document.querySelector("#oldPsw")
const newPsw = document.querySelector("#newPsw1")
const newPswRep = document.querySelector("#newPsw2")

const validationPsw = document.querySelectorAll(".validationPsw p")

const btn = document.querySelector("input[type='submit']")

let userInfo

getAccessToken()
.then(token => {
    axios.get("http://127.0.0.1:8000/api/v1/auth/user/", {
        headers: {
            "Authorization": `Bearer ${token}`
        }
    })
    .then(response => {
        userInfo = response.data
    })
})

form.addEventListener("submit", event => {
    event.preventDefault()

    getAccessToken()
    .then(token => {
        if (isPswValid(newPsw.value, newPswRep.value) === true) {
            let formdata = new FormData(form)

            btn.value = "Please wait a little"
            btn.style.cssText = `background: darkblue;`
            setTimeout(() => {
                btn.style.cssText += `background: rgb(87, 189, 104);
                                      transition: 1s;`
            }, 50)
    
            axios.post("http://127.0.0.1:8000/api/v1/auth/new-password/", formdata, {
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            })
            .then(response => {
                btn.value = "Success"
                btn.style.cssText = `background: darkgreen;`
                setTimeout(() => {
                    btn.style.cssText += `background: rgb(87, 189, 104);
                                          transition: 2.5s;`
                }, 50)
                for (input of document.querySelectorAll("input[type='password']")) {
                    input.value = null
                }
            })
            .catch(errors => {
                btn.value = "Fail"
                btn.style.cssText = `background: darkred;`
                setTimeout(() => {
                    btn.style.cssText += `background: rgb(87, 189, 104);
                                          transition: 2.5s;`
                }, 50)
                for (input of document.querySelectorAll("input[type='password']")) {
                    input.value = null
                }
            })
        }
    })
})

function isPswValid(pswrd1, pswrd2) {
    let pswrd = pswrd1

    let regexHasNumber = /[0-9]/
    let regexHasLetter = /[a-zA-Zа-яА-ЯёЁ]/
    let regexBoth = /^[a-zA-Zа-яА-ЯёЁ0-9]+$/

    if (pswrd != pswrd2) {
        return false
    }
    if (pswrd.toLowerCase().includes(userInfo.first_name.toLowerCase()) || pswrd.toLowerCase().includes(userInfo.last_name.toLowerCase())) {
        return false
    }
    if (pswrd.toLowerCase().includes(userInfo.email.split("@")[0].toLowerCase())) {
        return false
    }
    if (pswrd.length < 7) {
        return false
    }
    if (!regexBoth.test(pswrd) || !regexHasNumber.test(pswrd) || !regexHasLetter.test(pswrd)) {
        return false
    }
    return true
}

newPsw.addEventListener("input", () => {
    let pswrd = newPsw.value

    let regexHasNumber = /[0-9]/
    let regexHasLetter = /[a-zA-Zа-яА-ЯёЁ]/
    let regexBoth = /^[a-zA-Zа-яА-ЯёЁ0-9]+$/

    let hasError = false

    if (pswrd != newPswRep.value) {
        newPswRep.style.border = "1px solid darkred"
    } else {
        newPswRep.style.border = "1px solid gray"
    }

    if (pswrd.toLowerCase().includes(userInfo.first_name.toLowerCase()) || pswrd.toLowerCase().includes(userInfo.last_name.toLowerCase())) {
        validationPsw[0].style.color = "darkred"
        hasError = true
    } else {
        validationPsw[0].style.color = "darkgreen"
    }

    if (pswrd.toLowerCase().includes(userInfo.email.split("@")[0].toLowerCase())) {
        validationPsw[1].style.color = "darkred"
        hasError = true
    } else {
        validationPsw[1].style.color = "darkgreen"
    }

    if (pswrd.length < 7) {
        validationPsw[2].style.color = "darkred"
        hasError = true
    } else {
        validationPsw[2].style.color = "darkgreen"
    }

    if (!regexBoth.test(pswrd) || !regexHasNumber.test(pswrd) || !regexHasLetter.test(pswrd)) {
        validationPsw[3].style.color = "darkred"
        hasError = true
    } else {
        validationPsw[3].style.color = "darkgreen"
    }

    if (hasError === true) {
        newPsw.style.border = "1px solid darkred"
    } else {
        newPsw.style.border = "1px solid darkgreen"
    }
})

newPswRep.addEventListener("input", () => {
    let pswrd = newPswRep.value

    if (pswrd === newPsw.value) {
        newPswRep.style.border = "1px solid darkgreen"
    } else {
        newPswRep.style.border = "1px solid darkred"
    }
})
