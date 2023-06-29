let xhr = new XMLHttpRequest()
xhr.open("GET", "http://127.0.0.1:8000/api/v1/auth/authentication-check/", false)
xhr.send()

if (xhr.status != 200) {
  window.location.href = "/login/"
}
