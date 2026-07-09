const form = document.getElementById("SubmitForm");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(form)

    window.location.href = `/blogs?title=${formData.get("title")}`;
})