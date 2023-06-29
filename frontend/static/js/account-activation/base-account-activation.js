const btn = document.querySelector("#verify")
const input = document.querySelector(".get-email-input")
const block = document.querySelector(".verification-block")

function emailIsValid(email) {
    const regex = /^[^\d\s]\w+@(\w+\.\w+)$/;
    const allowedDomains = ["inbox.ru", "mail.ru", "list.ru", "gmail.com"]

    let parts = email.split("@")

    return regex.test(email) && allowedDomains.includes(parts[parts.length-1])
}

btn.addEventListener("click", () => {
    let email = input.value

    if (emailIsValid(email)) {
        window.location.href = `/account/activation/${email}/`
    }
})

input.addEventListener("input", () => {
    if (emailIsValid(input.value)) {
        input.style.cssText = "border: 1px solid rgb(132, 224, 123);"
    } else {
        input.style.cssText = "border: 1px solid rgb(217, 56, 70);"
    }
})

input.addEventListener("focus", () => {
    let divSix = document.createElement("div")
    divSix.id = "divSix"
    divSix.className = "content"
    divSix.innerText = `Email must start with letter
                        Containt at least 2 characters in main part
                        Allowed domains: mail.ru, list.ru, inbox.ru, gmail.com`
    block.append(divSix)
})

input.addEventListener("blur", () => {
    let divSix = document.querySelector("#divSix")
    block.removeChild(divSix)
})
