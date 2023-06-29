const progressBar = document.querySelector("input[type='range']")
const percentageOfProgressBar = document.querySelector("#percentageEnd")

const sender = document.querySelector("#card_sender")
const receiver = document.querySelector("#card_receiver")
const balance = document.querySelector("#amount")
const currency = document.querySelector("#currency")

const senderValidator = document.querySelector("#innerDivOne")
const receiverValidator = document.querySelector("#innerDivTwo")
const balanceValidator = document.querySelector("#divSeven")

const iAmNotRoborChecker = document.querySelector("#captcha-checkbox")

progressBar.addEventListener("input", () => {
    percentageOfProgressBar.innerText = progressBar.value
    if (progressBar.value === "100") {
        replenishBalance()
    }
})

receiver.addEventListener("input", () => {
    while (receiver.value.includes(" ")) {
        receiver.value = receiver.value.replace(" ", "")
    }
    {if (!allUserNumbers.includes(receiver.value)) {
            receiverValidator.innerHTML = `
                <p class="hints">* Warning</p>
                <p class="hints">You have not card</p>
                <p class="hints">with such number</p>`
        } else { 
            receiverValidator.innerHTML = `<span class="good-p2">OK</span>`
        }}
})

sender.addEventListener("input", () => {
    if (sender.validity.valid) {
        senderValidator.innerHTML = `<span class="good-p1">OK</span>`
    }
})

let allUserNumbers = []

getAccessToken()
.then(token => {
    axios.get("http://127.0.0.1:8000/api/v1/bank/cards/", {
        headers: {
            "Authorization": `Bearer ${token}`
        }
    })
    .then(resp => {
        for (card of resp.data) {
            allUserNumbers.push(card.number)
        }
    })
})

const resultTxt = document.querySelector("#result")

function replenishBalance() {
    if (!iAmNotRoborChecker.checked) {
        return
    }

    if (sender.validity.valid && receiver.validity.valid && balance.validity.valid && currency.validity.valid) {
        resultTxt.innerText = "Wait a little bit"
        resultTxt.style.color = "darkblue"
        
        getAccessToken()
        .then(token => {
            axios.post("http://127.0.0.1:8000/api/v1/bank/balance-replenishment/", {
                "real_number": sender.value,
                "virt_number": receiver.value,
                "balance": balance.value,
                "currency": currency.value
            }, {
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            })
            .then(() => {
                resultTxt.innerText = "Success"
                resultTxt.style.color = "darkgreen"
                progressBar.value = 0
                sender.value = ""
                receiver.value = ""
                balance.value = ""
                currency.value = "KZT"
                iAmNotRoborChecker.checked = false
                setTimeout(() => {
                    resultTxt.innerText = "Scroll to the end to finish replenishment"
                    resultTxt.style.color = null
                }, 1000)
                senderValidator.innerHTML = `<p class="hints">* Required</p><p class="hints">Number of your</p>
                                               <p class="hints">real card</p>`
                receiverValidator.innerHTML = `<p class="hints">* Required</p><p class="hints">Number of your</p>
                                             <p class="hints">virtual card</p>`
            })
            .catch(errors => {
                console.log(errors)
                resultTxt.innerText = "Invalid data"
                resultTxt.style.color = "darkred"
                progressBar.value = 0
                setTimeout(() => {
                    resultTxt.innerText = "Scroll to the end to finish replenishment"
                    resultTxt.style.color = null
                }, 1000)
            })
        })
    }
}
