const numberSelect = document.querySelector("select[name='number']")
const form = document.querySelector("form")

getAccessToken()
.then(token => {
    axios.get("http://127.0.0.1:8000/api/v1/bank/cards/", {
        headers: {
            Authorization: `Bearer ${token}`
        }
    })
    .then(response => {
        for (card of response.data) {
            numberSelect.innerHTML += `<option>${card.number}</option>`
        }
    })
})

const btn = document.querySelector("button")

form.addEventListener("submit", event => {
    event.preventDefault()

    let formdata = new FormData(form)

    getAccessToken()
    .then(token => {
        axios.post("http://127.0.0.1:8000/api/v1/bank/currency-convertation/", formdata, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        })
        .then(resp => {
            btn.style.cssText = "background: darkgreen"
            setTimeout(() => {
                btn.style.cssText += "background: white; transition: 1s"
                setTimeout(() => {
                    btn.style = null
                }, 1000)
            }, 50)
        })
        .catch(errors => {
            btn.style.cssText = "background: darkred"
            setTimeout(() => {
                btn.style.cssText += "background: white; transition: 1s"
                setTimeout(() => {
                    btn.style = null
                }, 1000)
            }, 50)
        })
    })
})
