export default function showModal(modalId) {
    const modal = bootstrap.Modal.getOrCreateInstance(
        document.getElementById(modalId)
    )

    modal.show();
    return modal;
}