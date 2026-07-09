import showModal from "../js/show_modal.js";

const form = document.getElementById("changePasswordForm");
const new_password = document.getElementById("newPassword")
const confirm_password = document.getElementById("confirmPassword")
const password_error = document.getElementById("passwordError")

confirm_password.addEventListener("keyup", () => {
    if (new_password.value != confirm_password.value) {
        password_error.classList.remove("d-none");
    } else {
        password_error.classList.add("d-none");
    }
})

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    if (confirm_password.value != new_password.value){
        throw new Error("New password and Confirm password do not match.")
    }

    const formData = new FormData(form)
    const passwordData = {
        current_password: formData.get("currentPassword"),
        new_password: formData.get("newPassword")
    }

    try {
        const response = await fetch("/api/users/password", {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(passwordData)
        })

        const responseData = await response.json();

        if (response.ok) {
            document.getElementById("SuccessModalBody").textContent = "Password is updated successfully!"

            showModal("SuccessModal");

            document.getElementById("SuccessModal").addEventListener("hidden.bs.modal", () => {
                window.location.href = "/profile"
            })
        } else {
            throw responseData.error
        }

    } catch (e) {
        if (Array.isArray(e)) {
            document.getElementById("ErrorModalBody").innerHTML = `<ul>
                ${e.map((val) => `<li><span class="fw-bold">${val.field}</span> : ${val.error_message}</li>`)}
            </ul>`
        } else {
            document.getElementById("ErrorModalBody").innerHTML = e;
        }

        showModal("ErrorModal")
    }
})