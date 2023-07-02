const allTransactionsBox = document.querySelector(".all-transactions-container")
const allActions = document.querySelectorAll(".action-p")


let page = 1
let filter = ""

actionPrevious = () => loadTransactions("prev")
actionAll = () => loadTransactions("all")
actionConverted = () => loadTransactions("conv")
actionReceived = () => loadTransactions("rec")
actionSpent = () => loadTransactions("spent")
actionNext = () => loadTransactions("next")

allActions[1].addEventListener("click", actionAll)
allActions[2].addEventListener("click", actionConverted)
allActions[3].addEventListener("click", actionReceived)
allActions[4].addEventListener("click", actionSpent)

function loadTransactions(action) {
  allActions[0].addEventListener("click", actionPrevious)
  allActions[5].addEventListener("click", actionNext)
  switch (action) {
    case "prev":
      page --
      break
    case "all":
      page = 1
      filter = ""
      break
    case "conv":
      page = 1
      filter = "converted"
      break
    case "rec":
      page = 1
      filter = "received"
      break
    case "spent":
      page = 1
      filter = "spent"
      break
    case "next":
      page ++
      break
  }
  allTransactionsBox.innerHTML = ""
  getAccessToken()
    .then(token => {
      axios.get(`http://127.0.0.1:8000/api/v1/bank/transaction/all/?page=${page}&filter=${filter}`,
      {
        params: {
          filter: filter
        },
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
      .then(resp => {
        if (!resp.data.previous) {
          allActions[0].style.cssText = "color: gray; text-decoration: none; cursor: default"
          allActions[0].removeEventListener("click", actionPrevious)
        } else {
          allActions[0].style.cssText = null
        }
        if (!resp.data.next) {
          allActions[5].style.cssText = "color: gray; text-decoration: none; cursor: default"
          allActions[5].removeEventListener("click", actionNext)
        } else {
          allActions[5].style.cssText = null
        }
        for (transaction of resp.data.results) {
          let sender = transaction.sender
          if (sender == null) {
            sender = "Real number"
          }
          let receiver = transaction.receiver
          if (receiver == null) {
            receiver = "Real number"
          }
          allTransactionsBox.innerHTML += `
            <p class="transaction">
              <span class="number-sender">
                <span>
                  ${sender}
                </span>
                <span>
                  ->
                </span>
              </span>
              <span class="balance">
                <span>
                  ${receiver}
                </span>
                <span>
                  ${transaction.balance}
                  ${transaction.currency}
                </span>
              </span>
            </p>`
        }
      })
    })
}

loadTransactions()
