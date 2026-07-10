import showModal from "../js/show_modal.js"

const form = document.getElementById("updateProfileForm");
const previewImage = document.getElementById("previewImage");
const profilePicture = document.getElementById("profilePicture");

console.log(previewImage.src)

// live image preview
profilePicture.addEventListener("change", () => {
    const picture = profilePicture.files[0];

    if (picture) {
        previewImage.src = URL.createObjectURL(picture);
    }
})

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    try {
        const formData = new FormData(form);
        const response = await fetch("/api/users/", {
            method: "PATCH",
            body: formData
        })
        const responseData = await response.json();

        if (response.ok) {
            document.getElementById("SuccessModalBody").textContent = "Profile updated successfully!"
            showModal("SuccessModal");

            document.getElementById("SuccessModal").addEventListener("hidden.bs.modal", () => {
                window.location.href = "/profile"
            })
        } else {
            throw responseData.error
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
