const inputGaps = document.querySelectorAll(".square")
const hintsContainer = document.querySelector(".hints-container")

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
    hintsContainer.innerHTML = ""

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

function getCode() {
    let code = ""
    for (gap of inputGaps) {
        code += gap.value
    }
    return code
}

const btn = document.querySelector("#verify")
const codeInput = document.querySelector(".get-email-input")
const hints = document.querySelector(".hints-container")

btn.addEventListener("click", event => {
    event.preventDefault()

    hints.innerHTML = ""

    let urlParts = window.location.href.split("/")
    let email = urlParts[urlParts.length-2]

    axios.post("http://127.0.0.1:8000/api/v1/auth/account/activation/", {
        "code": getCode(),
        "email": email
    })
    .then(response => {
        hints.innerHTML += `<p style="color: darkgreen;">${response.data.data}</p>`
    })
    .catch(error => {
        for (field in error.response.data) {
            for (err of error.response.data[field]) {
                if (field == "code") {
                    for (gap of inputGaps) {
                        gap.style.cssText = "border: 1px solid rgb(217, 56, 70)"
                    }
                }
                hints.innerHTML += `<p style="color: rgb(217, 56, 70)">${err}</p>`
            }
        }
    })
})
