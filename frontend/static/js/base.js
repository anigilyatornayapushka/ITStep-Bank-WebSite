const logoutBtn = document.querySelector(".navigation-bar .container ul li a#logout-button")


if (logoutBtn) {
    logoutBtn.addEventListener("click", () => {
        getAccessToken()
        .then(token => {
            axios.post("http://127.0.0.1:8000/api/v1/auth/logout/", {}, {
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            })
        })
    })
}
