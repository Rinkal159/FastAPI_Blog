import showModal from "../js/show_modal.js";
import hideModal from "../js/hide_modal.js";

const form = document.getElementById("EditBlogModalForm");
const title = document.getElementById("title")

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    try {
        const formData = new FormData(form);

        const blogData = {
            title: formData.get("title"),
            content: formData.get("content")
        }

        const response = await fetch(`/api/blogs/${formData.get("post_id")}`, {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(blogData)
        })

        const responseData = await response.json()

        if (response.ok) {
            hideModal("EditBlogModal");

            document.getElementById("SuccessModalBody").textContent = `"${title.value}" has been updated successfully!`
            showModal("SuccessModal");

            // redirects to same current page when user closes the modal
            document.getElementById("SuccessModal").addEventListener("hidden.bs.modal", () => {
                window.location.href = `/blogs/${formData.get("post_id")}`
            }, { once: true })

        } else {
            throw responseData.error;
        }


    } catch (e) {
        if (Array.isArray(e)) {
            document.getElementById("ErrorModalBody").innerHTML = `<ul>
                ${e.map((val) => `<li><span class="fw-bold">${val.field}</span> : ${val.error_message}</li>`).join("")}
            </ul>`
        } else {
            document.getElementById("ErrorModalBody").innerHTML = e;
        }

        showModal("ErrorModal");
    }
})