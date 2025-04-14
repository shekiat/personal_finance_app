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

// Budget tables functionality

// executes on the click of anything
document.addEventListener("click", function (e) {
    // Check if the input field is visible
    if (input.style.display === "block") {
        // If the clicked element is not the category input save input to hiddenCategory
        if (!categoryInput.contains(e.target) && !button.contains(e.target)) {
            hiddenCategory.value = categoryInput.value; 
        }
    }
    else if (dropdown.style.display === "block") {
        // If the clicked element is not the category input save input to hiddenCategory
        if (!categorySelect.contains(e.target) && !button.contains(e.target)) {
            hiddenCategory.value = categorySelect.value; 
        }
    }
    else {
        // if clicked button is not the submit transaction/income button, remove transaction/income added/error message
        if (!categorySelect.contains(e.target) && !button.contains(e.target)) {
            hiddenCategory.value = categorySelect.value; 
        }
    }

    document.getElementById("transactionFeedbackMessage").innerText = "";
    
    console.log(categorySelect.value)
    console.log(categoryInput.value)
    console.log(hiddenCategory.value)
});

console.log(categorySelect.value)
console.log(categoryInput.value)
console.log(hiddenCategory.value)

// when the toggle category (dropdown/input) button is pressed, change form elements and hidden category value
document.getElementById("toggleCategoryBtn").addEventListener("click", function() {
    console.clear()

    if (dropdown.style.display === "none") {
        dropdown.style.display = "block";
        input.style.display = "none";
        button.textContent = "Add Category";

        // Set the hidden category value to the selected dropdown value
        hiddenCategory.value = categorySelect.value;
        console.log(categorySelect.value)
        console.log(categoryInput.value)
        console.log(hiddenCategory.value)
    } else {
        dropdown.style.display = "none";
        input.style.display = "block";
        button.textContent = "Choose Existing Category";

        // Set the hidden category value to the input value
        hiddenCategory.value = categoryInput.value;
        console.log(categorySelect.value)
        console.log(categoryInput.value)
        console.log(hiddenCategory.value)
    }
});


// executes on the click of anything
document.addEventListener("click", function (e) {
    // Check if the input field is visible
    if (input.style.display === "block") {
        // If the clicked element is not the category input save input to hiddenCategory
        if (!categoryInput.contains(e.target) && !button.contains(e.target)) {
            hiddenCategory.value = categoryInput.value; 
        }
    }
    else if (dropdown.style.display === "block") {
        // If the clicked element is not the category input save input to hiddenCategory
        if (!categorySelect.contains(e.target) && !button.contains(e.target)) {
            hiddenCategory.value = categorySelect.value; 
        }
    }
    else {
        // if clicked button is not the submit transaction/income button, remove transaction/income added/error message
        if (!categorySelect.contains(e.target) && !button.contains(e.target)) {
            hiddenCategory.value = categorySelect.value; 
        }
    }

    document.getElementById("transactionFeedbackMessage").innerText = "";
    
    console.log(categorySelect.value)
    console.log(categoryInput.value)
    console.log(hiddenCategory.value)
});

console.log(categorySelect.value)
console.log(categoryInput.value)
console.log(hiddenCategory.value)

// when the toggle category (dropdown/input) button is pressed, change form elements and hidden category value
document.getElementById("toggleCategoryBtn").addEventListener("click", function() {
    console.clear()

    if (dropdown.style.display === "none") {
        dropdown.style.display = "block";
        input.style.display = "none";
        button.textContent = "Add Category";

        // Set the hidden category value to the selected dropdown value
        hiddenCategory.value = categorySelect.value;
        console.log(categorySelect.value)
        console.log(categoryInput.value)
        console.log(hiddenCategory.value)
    } else {
        dropdown.style.display = "none";
        input.style.display = "block";
        button.textContent = "Choose Existing Category";

        // Set the hidden category value to the input value
        hiddenCategory.value = categoryInput.value;
        console.log(categorySelect.value)
        console.log(categoryInput.value)
        console.log(hiddenCategory.value)
    }
});


// Displays the success message when the transaction/income form is submitted
function showSuccessMessage() {
    document.getElementById("successMessage").style.display = "block"; // Show the success message
}

// Displays the success message when the transaction/income form is submitted
function showIncomeSuccessMessage() {
    document.getElementById("incomeSuccessMessage").style.display = "block"; // Show the success message
}

// Displays fail message based on reason
function showFailAmountMessage() {
    document.getElementById("failAmountMessage").style.display = "block"; // Show the success message
}

function showFailDateMessage() {
    document.getElementById("failDateMessage").style.display = "block"; // Show the success message
}

// button listeners for jsonify
attachDeleteListeners()
// submit transaction
const submitTransBtn = document.getElementById("submitTransBtn");
submitTransBtn.addEventListener("click", function() {
    event.preventDefault();
    console.log("submit transaction button hit")
    const formData = {
        amount: document.getElementById("transAmount").value,
        date: document.getElementById("transDate").value,
        memo: document.getElementById("transMemo").value,
        category: document.getElementById("hidden-category").value
    };

    fetch("/api/submit-transaction", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log("transaction added succesfully")
                document.getElementById("transactionFeedbackMessage").innerText = "Transaction added!";
                document.getElementById("transAmount").value = "",
                document.getElementById("transDate").value = "",
                document.getElementById("transMemo").value = "",
                document.getElementById("hidden-category").value = ""
                // hide category inpiut, display dropdown

                updateStats();
                fetchUpdatedTransactions();
            }
            else {
                //assign each form input to the value of data.amount, data.date, etc.
                document.getElementById("transAmount").value = data.amount,
                document.getElementById("transDate").value = data.date,
                document.getElementById("transMemo").value = data.memo
                //document.getElementById("hidden-category").value = data.category
                if (data.return_value === 1) {
                    document.getElementById("transactionFeedbackMessage").innerText = "Date is in the future!";
                }
                else {
                    document.getElementById("transactionFeedbackMessage").innerText = "Amount is not a number!";
                }
            }
        })
});

// update transaction table
function updateTransactionTable(transactions) {
    console.log("updating transactions");
    const tableBody = document.querySelector("#groupTransactionTable table");

    tableBody.querySelectorAll("tr:not(:first-child)").forEach(row => row.remove());

    transactions.forEach(transaction => {
        const formattedDate = formatDate(transaction[3]);
        const formattedAmount = formatAmount(transaction[1]);
        const capitalizedCategory = transaction[2].charAt(0).toUpperCase() + transaction[2].slice(1);

        const row = `
            <tr>
                <td>Jim Gorden</td>
                <td>${formattedDate}</td>
                <td>${formattedAmount}</td>
                <td>${capitalizedCategory}</td>
                <td>${transaction[4]}</td>
                <td>
                    <button 
                        class="delete-trans-btn" 
                        transaction-id="${transaction[0]}">
                        Delete
                    </button>
                </td>
            </tr>
        `;
        tableBody.innerHTML += row;
    });

    attachDeleteListeners();
}
function formatDate(date) {
    return date[5] === "1"
        ? `${date.slice(5, 7)}/${date.slice(8, 10)}/${date.slice(0, 4)}`
        : `${date.slice(6, 7)}/${date.slice(8, 10)}/${date.slice(0, 4)}`;
}
function formatAmount(amount) {
    const strAmount = amount.toString();
    return strAmount.includes(".") && strAmount.split(".")[1].length === 1
        ? `$${strAmount}0`
        : `$${strAmount}`;
}

function fetchUpdatedTransactions() {
    console.log("fetching updated transactions")
    fetch("/api/update-transaction-table")
        .then(response => response.json())
        .then(data => {
            console.log(data.transactions);
            updateTransactionTable(data.transactions);
        });
}

// attach delete listeners on table entries
function attachDeleteListeners() {
    document.querySelectorAll('.delete-trans-btn').forEach(button => {
        button.addEventListener('click', (event) => {
            console.log("delete button hit");
            const transactionId = event.target.getAttribute('transaction-id');
            fetch('/api/delete-transaction', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    transaction_id: transactionId
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    event.target.closest('tr').remove();
                    updateStats();
                }
            });
        });
    });
}
