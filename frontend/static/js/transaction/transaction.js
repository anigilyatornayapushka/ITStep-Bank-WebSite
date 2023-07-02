let allNumbers = []
let allCards = []

getAccessToken()
.then(token => {
    axios.get("http://127.0.0.1:8000/api/v1/bank/cards/", {
        headers: {
            "Authorization": `Bearer ${token}`
        }
    })
    .then(response => {
        for (card of response.data) {
            allNumbers.push(card.number)
            allCards.push(card)
        }
    })
})

const senderNumber = document.querySelector("#card_sender")
const senderNumberValidator = document.querySelector("#card_sender_validator")

senderNumber.addEventListener("input", () => {
    if (allNumbers.includes(senderNumber.value)) {
        for (card of allCards) {
            if (card.number == senderNumber.value) {
                senderNumberValidator.innerHTML = ""
                for (currency in card.balance) {
                    senderNumberValidator.innerHTML += `<span>${card.balance[currency]} ${currency}</span>`
                }
                break
            }
        }
    } else {
        senderNumberValidator.innerHTML = "<span>You have not such card number</span>"
    }
})

const receiverNumber = document.querySelector("#card_receiver")
const receiverNumberValidator = document.querySelector("#card_receiver_validator")

let numbersBlackList = []

receiverNumber.addEventListener("input", () => {
    if (receiverNumber != senderNumber && receiverNumber.value.length === 16 && !numbersBlackList.includes(receiverNumber.value) && /^\d{16}$/.test(receiverNumber.value) && /^\d{16}$/.test(senderNumber.value)) {
        getAccessToken()
        .then(token => {
            axios.get(`http://127.0.0.1:8000/api/v1/bank/card-owner/`, {
                params: {
                    "number": receiverNumber.value
                },
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            })
            .then(response => {
                receiverNumberValidator.innerHTML = `<span>${response.data.fullname}</span>`
            })
            .catch(error => {
                numbersBlackList.push(receiverNumber.value)
                receiverNumberValidator.innerHTML = "<span>??? ???</span>"
            })
        })
    } else {
        receiverNumberValidator.innerHTML = "<span>??? ???</span>"
    }
})

const btnSend = document.querySelector("button")

btnSend.addEventListener("click", event => {
    event.preventDefault()

    if (receiverNumber != senderNumber && receiverNumber.value.length === 16 && senderNumber.value.length === 16 && !numbersBlackList.includes(receiverNumber.value)) {
        let formdata = new FormData(document.querySelector("form"))
    
        getAccessToken()
        .then(token => {
            axios.post("http://127.0.0.1:8000/api/v1/bank/transaction/", formdata,
            {
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            })
            .then(resp => {
                btnSend.style.cssText = "background: darkgreen"
                setTimeout(() => {
                    btnSend.style.cssText = "background: white; transition: 1.5s"
                    setTimeout(() => {
                        btnSend.style.cssText = null
                    }, 1500)
                }, 50)
            })
            .catch(err => {
                btnSend.style.cssText = "background: darkred"
                setTimeout(() => {
                    btnSend.style.cssText = "background: white; transition: 1.5s"
                    setTimeout(() => {
                        btnSend.style.cssText = null
                    }, 1500)
                }, 50)
            })
        })
    }

})
