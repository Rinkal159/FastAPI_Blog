export default function hideModal(modalId) {
    const modal = bootstrap.Modal.getOrCreateInstance(
        document.getElementById(modalId)
    )

    if (modal) {
        modal.hide()
    }
}