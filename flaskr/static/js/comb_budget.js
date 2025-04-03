document.getElementById('inviteForm').addEventListener('submit', async (event) => {
    event.preventDefault(); // Prevent default form submission

    const email = document.getElementById('email').value; // Get the email from the input field

    try {
        // Send the email to the backend
        const response = await fetch('/invite-user', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email }) // Send the email as JSON
        });

        const result = await response.json();
        if (response.ok) {
            alert(result.message); // Show success message
        } else {
            alert('Error: ' + result.error); // Show error message
        }
    } catch (error) {
        console.error('Error inviting user:', error);
        alert('An error occurred while sending the invitation.');
    }
});