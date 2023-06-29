function TokenManager() {
    let accessToken
    let expireAt

    async function setAccessToken() {
        const FingerprintJS = await import('https://openfpcdn.io/fingerprintjs/v3')
        const fp = await FingerprintJS.load()
        const result = await fp.get()
        const visitorId = result.visitorId

        const response = await axios.post("http://127.0.0.1:8000/api/v1/auth/token/refresh/", {
            "fingerprint": visitorId
        })
        .catch(err => window.location.href = "/")

        accessToken = response.data.access
        expireAt = Date.now() + (4 * 60 * 1000)
        return accessToken
    }

    async function getAccessToken() {
        if (!accessToken || Date.now() >= expireAt) {
            return await setAccessToken()
        } else {
            return accessToken
        }
    }

    return getAccessToken;
}

getAccessToken = TokenManager()
