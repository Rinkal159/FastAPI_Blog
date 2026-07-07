import showModal from "../js/show_modal.js";

const form = document.getElementById("loginForm")

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    try {
        const formData = new FormData(form);
        

        const response = await fetch("/api/auth/login", {
            method: "POST",
            body: formData
        })

        const responseData = await response.json()


        if (response.ok) {
            localStorage.setItem("access_token", responseData.access_token);

            const response = await fetch("/api/users", {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("access_token")}`
                }
            })

            const user = await response.json();

            document.getElementById("SuccessModalBody").textContent = `${user.name}, you've been logged in successfully!`
            showModal("SuccessModal")


            document.getElementById("SuccessModal").addEventListener("hidden.bs.modal", () => {
                window.location.href= "/"
            }, {once: true})

            
        } else {
            throw responseData.error
        }

    } catch (e) {
        if (Array.isArray(e)) {
            document.getElementById("ErrorModalBody").innerHTML = `<ul class=list-unstyled>
                ${e.map((val) => `<li><span class="fw-bold">${val.field}</span> - ${val.error_message}</li>`).join("")}
            </ul>`
        } else {
            document.getElementById("ErrorModalBody").innerHTML = e
        }

        showModal("ErrorModal")
    }
})