function TicketForm() {
    const form = document.getElementById('ticket-form');

    if (form.style.display === 'none' || form.style.display === '') {
        form.style.display = 'block';
    } else {
        form.style.display = 'none';
    }        
}