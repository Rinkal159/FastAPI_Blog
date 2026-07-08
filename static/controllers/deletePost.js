import hideModal from "../js/hide_modal.js";
import showModal from "../js/show_modal.js";

const blogId = document.getElementById("post_id").textContent
const blogTitle = document.getElementById("blog_title").textContent
const deleteBtn = document.getElementById("delete");

deleteBtn.addEventListener("click", async () => {
    try {
        const response = await fetch(`/api/blogs/${blogId}`, {
            method: "DELETE"
        })


        if (response.ok) {
            hideModal("DeleteBlogModal")

            document.getElementById("SuccessModalBody").textContent = `"${blogTitle}" has been deleted successfully!`
            showModal("SuccessModal");

            // redirects to '/' page when user closes the modal
            document.getElementById("SuccessModal").addEventListener("hidden.bs.modal", () => {
                window.location.href = '/'
            }, { once: true })

        } else {
            const error = await response.json();
            throw error.error;
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