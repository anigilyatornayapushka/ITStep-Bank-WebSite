const userFullname = document.querySelector(".user-fullname")
const userEmail = document.querySelector(".user-email")
const userGender = document.querySelector(".user-gender")
const userJoin = document.querySelector(".user-join")
const profileImage = document.querySelector("#avatar")

getAccessToken()
.then(token => {
    axios.get("http://127.0.0.1:8000/api/v1/auth/user/", {
        headers: {
            "Authorization": `Bearer ${token}`
        }
    })
    .then(response => {
        let data = response.data

        if (data.gender === 2) {
            profileImage.computedStyleMap.border = "2px solid purple"
        }

        userFullname.innerText = `${data.last_name} ${data.first_name}`
        userFullname.style.cssText = "font-size: 140%"

        userEmail.innerText = `${data.email}`
        userEmail.style.cssText = "color: darkgray"

        let allGenders = ["", "Male", "Female"]
        userGender.innerText += ` ${allGenders[data.gender]}`

        userJoin.innerText += ` ${data.datetime_created.split(" ")[0]}`
    })
})

function loadCards() {
    let allCardsContainer = document.querySelector("#col-2")
    getAccessToken()
    .then(token => {
        axios.get("http://127.0.0.1:8000/api/v1/bank/cards/", {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        })
        .then(response => {
            let data = response.data

            allCardsContainer.innerHTML = ""

            for (i in data) {
                let card = data[i]

                allCardsContainer.innerHTML += `<div class="card" id=card_${i}>
                                                    <p class="bigger-p">Virtual card</p>
                                                    <hr>
                                                    <p class="full-card-number" id="${card.number}">Card number</p>
                                                    <div class="card-info">
                                                        <span class="card-span">${card.number.slice(0, 4)}</span>
                                                        <span class="card-span">${card.number.slice(4, 8)}</span>
                                                        <span class="card-span">${card.number.slice(8, 12)}</span>
                                                        <span class="card-span">${card.number.slice(12, 16)}</span>
                                                    </div>
                                                    <div class="card-info card-cvv-info">
                                                        <span class="card-span card-cvv-span">CVV: ${card.cvv}</span>
                                                    </div>
                                                    <div class='balance'></div>
                                                    <span class="visa">
                                                        <div class="gray-square">
                                                            <div class="square-line"></div>
                                                        </div>
                                                        <div class="sq">
                                                            <div class="square" id="sq1"></div>
                                                            <div class="square" id="sq2"></div>
                                                        </div>
                                                    </span>
                                                </div>`

                let cardElem = allCardsContainer.querySelector(`#card_${i}`)
                let cardBalance = cardElem.querySelector(".balance")

                for (currency in card.balance) {
                    cardBalance.innerHTML += `<div class='currency-box'>
                                                <span class="currency" id="${currency}_${i}">${currency}</span>
                                                <span class="currency" id="${card.number}_balance">${card.balance[currency]}</span>
                                            </div>`
                }
            }

            if (response.data.length < 3) {
                allCardsContainer.innerHTML += `<div class="card">
                                                    <p class="bigger-p">Create virtual card</p>
                                                    <hr>
                                                    <p>Card number</p>
                                                    <div class="card-info">
                                                        <span class="card-span">XXXX</span>
                                                        <span class="card-span">XXXX</span>
                                                        <span class="card-span">XXXX</span>
                                                        <span class="card-span">XXXX</span>
                                                    </div>
                                                    <div class="card-info card-cvv-info">
                                                        <span class="card-span card-cvv-span">CVV: XXX</span>
                                                    </div>
                                                    <span class="visa">
                                                        <div class="gray-square">
                                                            <div class="square-line"></div>
                                                        </div>
                                                        <div class="sq">
                                                            <div class="square" id="sq1"></div>
                                                            <div class="square" id="sq2"></div>
                                                        </div>
                                                    </span>
                                                </div>
                                                <button id="new-card-btn">Create new card</button>`

                const createCardButton = document.querySelector("#new-card-btn")

                createCardButton.addEventListener("click", () => {

                    getAccessToken()
                    .then(token => {
                        axios.post("http://127.0.0.1:8000/api/v1/bank/new-card/", {}, {
                            headers: {
                                "Authorization": `Bearer ${token}`
                            }
                        })
                        .then(response => {
                            let data = response.data
                            console.log(data)
                            loadCards()
                        })
                    })
                })
            }
        })
    })
}

loadCards()
