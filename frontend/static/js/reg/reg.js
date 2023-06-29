const firstNameInput = document.querySelector("#first_name")
const lastNameInput = document.querySelector("#last_name")
const emailInput = document.querySelector("#email")
const passwordInput = document.querySelector("#password")
const passwordRepeatInput = document.querySelector("#password2")

const firstNameValidator = document.querySelector("#first_name_validator")
const lastNameValidator = document.querySelector("#last_name_validator")
const emailValidator = document.querySelector("#email_validator")
const passwordValidator = document.querySelector("#password_validator")
const passwordRepeatValidator = document.querySelector("#password2_validator")

const firstNameIcon = document.querySelector("#first_name_icon")
const lastNameIcon = document.querySelector("#last_name_icon")
const emailIcon = document.querySelector("#email_icon")
const passwordIcon = document.querySelector("#password_icon")
const passwordRepeatIcon = document.querySelector("#password2_icon")

const passwordEye = document.querySelector("#password_eye")
const passwordRepeatEye = document.querySelector("#password2_eye")

const hintsContainer = document.querySelector(".hints-container")

firstNameInput.addEventListener("input", () => {
    if (firstNameInput.value.length > 0) {
        firstNameValidator.className = "bi bi-check-lg"
        firstNameValidator.style.cssText = `color: rgb(49, 203, 210);
                                            font-size: medium;`
        firstNameIcon.style.cssText = "border-bottom: 1px solid rgb(49, 203, 210)"
    } else {
        firstNameIcon.style.cssText = "border-bottom: 1px solid rgb(255, 123, 0);"
        firstNameValidator.className = "bi bi-exclamation-triangle"
        firstNameValidator.style.cssText = "color: rgb(255, 123, 0);"
    }
})

lastNameInput.addEventListener("input", () => {
    if (lastNameInput.value.length > 0) {
        lastNameValidator.className = "bi bi-check-lg"
        lastNameValidator.style.cssText = `color: rgb(49, 203, 210);
                                           font-size: medium;`
        lastNameIcon.style.cssText = "border-bottom: 1px solid rgb(49, 203, 210)"
    } else {
        lastNameValidator.className = "bi bi-exclamation-triangle"
        lastNameValidator.style.cssText = "color: rgb(255, 123, 0);"
        lastNameIcon.style.cssText = "border-bottom: 1px solid rgb(255, 123, 0);"
    }
})

emailInput.addEventListener("input", () => {
    const regex = /^[^\d\s]\w+@(\w+\.\w+)$/;
    const allowedDomains = ["inbox.ru", "mail.ru", "list.ru", "gmail.com"]
    let text = emailInput.value
    let parts = text.split("@")

    if (
        regex.test(text) &&
        allowedDomains.includes(
            parts[parts.length-1]
        )
    ) {
        emailValidator.className = "bi bi-check-lg"
        emailValidator.style.cssText = `color: rgb(49, 203, 210);
                                        font-size: medium;`
        emailIcon.style.cssText = "border-bottom: 1px solid rgb(49, 203, 210)"
    } else {
        emailValidator.className = "bi bi-exclamation-triangle"
        emailValidator.style.cssText = "color: rgb(255, 123, 0);"
        emailIcon.style.cssText = "border-bottom: 1px solid rgb(255, 123, 0);"
    }
})

passwordInput.addEventListener("input", () => {
    const regexOnlyLetters = /^[a-zA-Zа-яА-ЯёЁ]+$/;
    const regexOnlyNumbers = /^[0-9]+$/;
    const regexChars = /^[а-яА-ЯёЁa-zA-Z0-9]+$/;
    let text = passwordInput.value

    if (
        regexChars.test(text) &&
        !regexOnlyNumbers.test(text) &&
        !regexOnlyLetters.test(text) &&
        text.length > 6
    ) {
        passwordIcon.className = "bi bi-lock-fill"
        passwordValidator.className = "bi bi-check-lg"
        passwordValidator.style.cssText = `color: rgb(49, 203, 210);
                                           font-size: medium;`
        passwordIcon.style.cssText = "border-bottom: 1px solid rgb(49, 203, 210)"
        if (text == passwordRepeatInput.value) {
            passwordRepeatIcon.className = "bi bi-lock-fill"
            passwordRepeatValidator.className = "bi bi-check-lg"
            passwordRepeatValidator.style.cssText = `color: rgb(49, 203, 210);
                                                     font-size: medium;`
            passwordRepeatIcon.style.cssText = "border-bottom: 1px solid rgb(49, 203, 210)"
        } else {
            passwordRepeatIcon.className = "bi bi-unlock-fill"
            passwordRepeatValidator.className = "bi bi-exclamation-triangle"
            passwordRepeatValidator.style.cssText = "color: rgb(255, 123, 0);"
            passwordRepeatIcon.style.cssText = "border-bottom: 1px solid rgb(255, 123, 0);"
        }
    } else {
        passwordIcon.className = "bi bi-unlock-fill"
        passwordValidator.className = "bi bi-exclamation-triangle"
        passwordValidator.style.cssText = "color: rgb(255, 123, 0);"
        passwordRepeatIcon.className = "bi bi-unlock-fill"
        passwordRepeatValidator.className = "bi bi-exclamation-triangle"
        passwordRepeatValidator.style.cssText = "color: rgb(255, 123, 0);"
        passwordIcon.style.cssText = "border-bottom: 1px solid rgb(255, 123, 0);"
        passwordRepeatIcon.style.cssText = "border-bottom: 1px solid rgb(255, 123, 0);"
    }
})

passwordRepeatInput.addEventListener("input", () => {
    const regexOnlyLetters = /^[a-zA-Zа-яА-ЯёЁ]+$/;
    const regexOnlyNumbers = /^[0-9]+$/;
    const regexChars = /^[а-яА-ЯёЁa-zA-Z0-9]+$/;
    let text = passwordRepeatInput.value

    if (
        regexChars.test(text) &&
        !regexOnlyNumbers.test(text) &&
        !regexOnlyLetters.test(text) &&
        text.length > 6 &&
        text == passwordInput.value
    ) {
        passwordRepeatIcon.className = "bi bi-lock-fill"
        passwordRepeatValidator.className = "bi bi-check-lg"
        passwordRepeatValidator.style.cssText = `color: rgb(49, 203, 210);
                                                 font-size: medium;`
        passwordRepeatIcon.style.cssText = "border-bottom: 1px solid rgb(49, 203, 210)"
    } else {
        passwordRepeatIcon.className = "bi bi-unlock-fill"
        passwordRepeatValidator.className = "bi bi-exclamation-triangle"
        passwordRepeatValidator.style.cssText = "color: rgb(255, 123, 0);"
        passwordRepeatIcon.style.cssText = "border-bottom: 1px solid rgb(255, 123, 0);"
    }
})

passwordEye.addEventListener("mousedown", () => {
    passwordEye.className = "bi bi-eye"
    passwordInput.type = "text"
})

passwordRepeatEye.addEventListener("mousedown", () => {
    passwordRepeatEye.className = "bi bi-eye"
    passwordRepeatInput.type = "text"
})

passwordEye.addEventListener("mouseout", () => {
    passwordEye.className = "bi bi-eye-slash"
    passwordInput.type = "password"
})

passwordRepeatEye.addEventListener("mouseout", () => {
    passwordRepeatEye.className = "bi bi-eye-slash"
    passwordRepeatInput.type = "password"
})

passwordEye.addEventListener("mouseup", () => {
    passwordEye.className = "bi bi-eye-slash"
    passwordInput.type = "password"
})

passwordRepeatEye.addEventListener("mouseup", () => {
    passwordRepeatEye.className = "bi bi-eye-slash"
    passwordRepeatInput.type = "password"
})

firstNameInput.addEventListener("focus", () => {
    hintsContainer.innerHTML = `<p>Must contain at least one character</p>
                                <p>Use real name</p>`
})

lastNameInput.addEventListener("focus", () => {
    hintsContainer.innerHTML = `<p>Must contain at least one character</p>
                                <p>Use real surname</p>`
})

emailInput.addEventListener("focus", () => {
    hintsContainer.innerHTML = `<p>Allowed domains: mail.ru,
                                inbox.ru, list.ru, gmail.com</p>
                                <p>Main part must start with letter</p>
                                <p>At least two characters in main part</p>`
})

passwordInput.addEventListener("focus", () => {
    hintsContainer.innerHTML = `<p>Password must contain both numbers and letters</p>
                                <p>Minimal length - 7 characters</p>`
})

passwordRepeatInput.addEventListener("focus", () => {
    hintsContainer.innerHTML = `<p>Password must be the same as previous</p>`
})

firstNameInput.addEventListener("blur", () => {
    if (inActive === false) {
        hintsContainer.innerHTML = `<p>Click on some field to view hints</p>`
    }
})

lastNameInput.addEventListener("blur", () => {
    if (inActive === false) {
        hintsContainer.innerHTML = `<p>Click on some field to view hints</p>`
    }
})

emailInput.addEventListener("blur", () => {
    if (inActive === false) {
        hintsContainer.innerHTML = `<p>Click on some field to view hints</p>`
    }
})

passwordInput.addEventListener("blur", () => {
    if (inActive === false) {
        hintsContainer.innerHTML = `<p>Click on some field to view hints</p>`
    }
})

passwordRepeatInput.addEventListener("blur", () => {
    if (inActive === false) {
        hintsContainer.innerHTML = `<p>Click on some field to view hints</p>`
    }
})

const form = document.querySelector(".registration-form")
const btn = document.querySelector("#register")
const agreeCheckbox = document.querySelector("#agree")

btn.addEventListener("click", event => {
    event.preventDefault()

    if (inActive === true || !agreeCheckbox.checked) {
        return;
    } else {
        hintsContainer.innerHTML = ``

        formdata = new FormData(form)
        axios.post("http://127.0.0.1:8000/api/v1/auth/registration/", formdata)
        .then(() => {
            stopLoading()

            let errStyles = "border-bottom: 1px solid rgb(132, 224, 124);"
            let successStyles = "color: rgb(132, 224, 124);"
    
            firstNameIcon.style.cssText = errStyles
            lastNameIcon.style.cssText = errStyles
            emailIcon.style.cssText = errStyles
            passwordIcon.style.cssText = errStyles
            passwordRepeatIcon.style.cssText = errStyles

            firstNameValidator.style.cssText = successStyles
            lastNameValidator.style.cssText = successStyles
            emailValidator.style.cssText = successStyles
            passwordValidator.style.cssText = successStyles
            passwordRepeatValidator.style.cssText = successStyles
            for (data of formdata) {
                if (data[0] == "email") {
                    console.log(data[1])
                    var user_email = data[1]
                }
            }
            hintsContainer.innerHTML = `<h2>Hints</h2>
                                        <p style='color: rgb(15, 126, 15);'>
                                        Thank you for registration</p>
                                        <p style='color: rgb(15, 126, 15);'>
                                        Please 
                                        <a href="/account/activation/${user_email}/"
                                           style="color: rgb(19, 139, 19);">
                                        verify it</a>
                                        </p>
                                        <p style='color: rgb(15, 126, 15);'>
                                        Code was sent on your email</p>
                                        `
            form.reset()
        })
        .catch(errors => {
            stopLoading()

            let errorsMap = errors.response.data

            for (err in errorsMap) {

                for (newError of errorsMap[err]) {
                    if (newError !== "This field may not be blank.") {
                        hintsContainer.innerHTML += `<p style="color: rgb(217, 56, 70)">
                                                     ${newError}</p>`
                    }
                }

                let input = document.querySelector(`#${err}_icon`)
                input.style.cssText = "border-bottom: 1px solid rgb(217, 56, 70);"
            }
        })
    } 
})
