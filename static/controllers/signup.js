import showModal from "../js/show_modal.js"

const form = document.getElementById("signupForm")
const password = document.getElementById("password")
const confirmPassword = document.getElementById("confirmPassword")
const passwordError = document.getElementById("passwordError")
const name = document.getElementById("name")
const profilePicture = document.getElementById("profilePicture")
const previewImage = document.getElementById("previewImage")

console.log("HELLO");

// live checking
confirmPassword.addEventListener("keyup", () => {
    if (password.value != confirmPassword.value) {
        passwordError.classList.remove("d-none")
    } else {
        passwordError.classList.add("d-none")
    }
})


// live profile picture preview
profilePicture.addEventListener("change", () => {
    const pictureFile = profilePicture.files[0];

    if (pictureFile) {
        previewImage.src = URL.createObjectURL(pictureFile)
    }
})


form.addEventListener("submit", async (e) => {
    e.preventDefault();

    try {

        if (password.value != confirmPassword.value) {
            throw new Error("Password and Confirm Password do not match")
        }


        const formData = new FormData(form)

        const response = await fetch("/api/auth/signup", {
            method: "POST",
            body: formData
        })


        if (response.ok) {
            document.getElementById("SuccessModalBody").textContent = `${name.value}, You've been signed up successfully!`
            showModal("SuccessModal")

            // redirects to 'login' page when user closes the modal
            document.getElementById("SuccessModal").addEventListener("hidden.bs.modal", () => {
                window.location.href = "/login"
            }, { once: true })

        } else {
            const error = await response.json()
            throw error.error
        }


    } catch (e) {

        if (Array.isArray(e)) { // 422 error
            document.getElementById("ErrorModalBody").innerHTML = `<ul class="list-unstyled">
            ${e.map(val => `<li><span class="fw-bold">${val.field}</span> - ${val.error_message}</li>`).join("")}
            </ul>`

        } else { // general error
            document.getElementById("ErrorModalBody").innerHTML = e
        }

        showModal("ErrorModal")
    }
})