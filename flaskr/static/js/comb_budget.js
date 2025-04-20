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
        })
        const result = await response.json();
        if (response.ok) {
            document.getElementById('email').value = ""
            alert(result.message); // Show success message
            window.location.href = "/combined_budget";
        } else {
            alert('Error: ' + result.error); // Show error message
        }
    } catch (error) {
        console.error('Error inviting user:', error);
        alert('An error occurred while sending the invitation.');
    }
});


attachTransChatListeners();
attachIncomeChatListeners();

// attach chat listeners on transaction entries
function attachTransChatListeners() {
    document.querySelectorAll('.trans-chat-btn').forEach(button => {
        button.addEventListener('click', (event) => {
            console.log("transaction chat button hit");
            const transactionAmount = event.target.getAttribute('transaction-amount');
            const transactionDate = event.target.getAttribute('transaction-date');
            const transactionCategory = event.target.getAttribute('transaction-category');
            const transactionMemo = event.target.getAttribute('transaction-memo');
            const transactionName = event.target.getAttribute('transaction-name');
            message = '$' + transactionAmount + '<br>' + transactionDate + '<br>' + transactionCategory;
            
            if (transactionName != user_name) { 
                message = transactionName + '<br>' + message;
            }
            if (transactionMemo != '') {
                message = message + '<br>"' + transactionMemo +'"';
            }

            message = '[t]' + message;
            
            // Send the message to the server
            try {
                const response = fetch('/api/send-message', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ message })
                });

                const result = response.json();
                if (!result.success) {
                    console.error('Failed to send message:', result.error);
                }
                else {
                    addMessageToChat(user_name, message);
                }
            } catch (error) {
                console.error('Error sending message:', error);
            }
        });
    });
}

// attach chat listeners on income entries
function attachIncomeChatListeners() {
    document.querySelectorAll('.income-chat-btn').forEach(button => {
        button.addEventListener('click', (event) => {
            console.log("income chat button hit");
            const incomeAmount = event.target.getAttribute('income-amount');
            const incomeDate = event.target.getAttribute('income-date');
            const incomeMemo = event.target.getAttribute('income-memo');
            const incomeName = event.target.getAttribute('income-name');
            message = '$' + incomeAmount + '<br>' + incomeDate;

            if (incomeName != user_name) { 
                message = incomeName + '<br>' + message;
            }
            if (incomeMemo != '') {
                message = message + '<br>"' + incomeMemo + '"';
            }
            message = '[i]' + message;

            // Send the message to the server
            try {
                const response = fetch('/api/send-message', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ message })
                });

                const result = response.json();
                if (!result.success) {
                    console.error('Failed to send message:', result.error);
                }
                else { 
                    addMessageToChat(user_name, message);
                }
            } catch (error) {
                console.error('Error sending message:', error);
            }
        });
    });
}




// group chat functionality
document.getElementById('chatForm').addEventListener('submit', async (event) => {
    event.preventDefault();

    const chatInput = document.getElementById('chatInput');
    const message = chatInput.value.trim();

    if (message) {
        // Clear the input field
        chatInput.value = '';

        // Send the message to the server
        try {
            const response = await fetch('/api/send-message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message })
            });

            const result = await response.json();
            if (!result.success) {
                console.error('Failed to send message:', result.error);
            }
            else {
                // display message in chat box
                addMessageToChat(user_name, message);
            }
        } catch (error) {
            console.error('Error sending message:', error);
        }
    }
});

// Function to add a message to the chat box
function addMessageToChat(user, message, timestamp) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = user === 'You' ? 'my-message' : 'user-message';
    if (message.slice(0, 3) == "[t]") {
        messageDiv.innerHTML = `${user}:`;
        const transDiv = document.createElement('div');
        transDiv.innerHTML = `${message.slice(3)} <br>`;
        transDiv.style.textAlign = 'center';
        transDiv.style.color = 'rgb(255, 52, 52)';

        chatMessages.appendChild(messageDiv);
        chatMessages.appendChild(transDiv);
    }
    else if (message.slice(0, 3) == "[i]") {
        messageDiv.innerHTML = `${user}:`;
        const transDiv = document.createElement('div');
        transDiv.innerHTML = `${message.slice(3)} <br>`;
        transDiv.style.textAlign = 'center';
        transDiv.style.color = 'rgb(12, 166, 12)';

        chatMessages.appendChild(messageDiv);
        chatMessages.appendChild(transDiv);
    }
    else {
        messageDiv.innerHTML = `${user}: ${message} (${timestamp})`;
        messageDiv.style.marginBottom = '5px';
        chatMessages.appendChild(messageDiv);
    }


    // Scroll to the bottom of the chat box
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Function to fetch and display new messages
async function fetchMessages() {
    console.log("fetching messages")
    try {
        const response = await fetch('/api/get-messages');
        const result = await response.json();

        const scrollOffsetFromBottom = chatMessages.scrollHeight - chatMessages.scrollTop; // calculate scrolled to position

        if (result.success) {
            const chatMessages = document.getElementById('chatMessages');
            const messages = Array.from(chatMessages.children);
            const lastFiveMessagesOnPage = messages.slice(-5);
            const lastFiveMessagesFromDB = result.messages.slice(-5);
            chatMessages.innerHTML = ''; // Clear existing messages

            result.messages.forEach((msg) => {
                addMessageToChat(msg.user, msg.message);
            });

            for (let i = 4; i >= 0; i--) {
                console.log(lastFiveMessagesOnPage[i]);
                console.log(lastFiveMessagesFromDB[i]);
                if (lastFiveMessagesOnPage[i] != lastFiveMessagesFromDB[i]) {
                    addMessageToChat(lastFiveMessagesOnPage[i].user, lastFiveMessagesOnPage[i].message);
                }
            }

            chatMessages.scrollTop = chatMessages.scrollHeight - scrollOffsetFromBottom; // restore scrolled to position
        }
    } catch (error) {
        console.error('Error fetching messages:', error);
    }
}

// Call fetchMessages when the page loads
window.onload = fetchMessages;

// Poll for new messages every 5 seconds
setInterval(fetchMessages, 5000);


// copied over from home.js

// Displays past and future years in the year select dropdown
let yearSelect = document.getElementById("year");
let currentYear = new Date().getFullYear();
let startYear = currentYear - 10; // Start from 10 years ago
let endYear = currentYear;

yearSelect.innerHTML = "";

for (let year = startYear; year <= endYear; year++) {
    let option = document.createElement("option");
    option.value = year;
    option.textContent = year;
    if (year === chosen_year) {
        option.selected = true; // Default to current year
    }
    yearSelect.appendChild(option);
}


// Displays the subcategory input field when the "Add Subcategory" button is clicked
const dropdown = document.getElementById("categoryDropdown");
dropdown.style.display = "block";
const input = document.getElementById("categoryInput");
const button = document.getElementById("toggleCategoryBtn");
const categorySelect = document.getElementById("category-list");
const categoryInput = document.getElementById("add-category");

const hiddenCategory = document.getElementById("hidden-category");
hiddenCategory.value = categorySelect.value;

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



// Swaps visibility of Add Expense and Add Income buttons/elements
const addExpense = document.getElementById("addExpenseButton");
const addIncome = document.getElementById("addIncomeButton");

const transactionForm = document.getElementById("transactionForm");
const incomeForm = document.getElementById("incomeForm");

const transactionTable = document.getElementById("transactionTable");
const incomeTable = document.getElementById("incomeTable");

const transactionSuccessMessage = document.getElementById("transactionSuccessMessage");
const incomeSuccessMessage = document.getElementById("incomeSuccessMessage");

const failDateMessage = document.getElementById("failDateMessage");
const failAmountMessage = document.getElementById("failAmountMessage");


addIncome.addEventListener("click", function() {
    expense_income = 1;

    transactionForm.style.display = "none";
    incomeForm.style.display = "block";

    addExpense.style.display = "block";
    addIncome.style.display = "none";
    addExpense.style.justifyContent = "center";

    transactionTable.style.display = "none";
    incomeTable.style.display = "block";
    
    incomeSuccessMessage.style.display = "none";
    failDateMessage.style.display = "none";
    failAmountMessage.style.display = "none";
});

addExpense.addEventListener("click", function() {
    expense_income = 0;

    transactionForm.style.display = "block";
    incomeForm.style.display = "none";

    addExpense.style.display = "none";
    addIncome.style.display = "block";
    addIncome.style.justifyContent = "center";

    transactionTable.style.display = "block";
    incomeTable.style.display = "none";

    transactionSuccessMessage.style.display = "none";
    failDateMessage.style.display = "none";
    failAmountMessage.style.display = "none";
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
attachTransDeleteListeners();
attachIncomeDeleteListeners();
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

    fetch("/api/group-submit-transaction", {
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
                else if (data.return_value === 2) {
                    document.getElementById("transactionFeedbackMessage").innerText = "Amount is not a number!";
                }
                else {
                    document.getElementById("transactionFeedbackMessage").innerText = "Date is invalid!";
                }
            }
        })
});

// update transaction table
function updateTransactionTable(transactions) {
    console.log("updating transactions");
    const tableBody = document.querySelector("#transactionTable table");

    tableBody.querySelectorAll("tr:not(:first-child)").forEach(row => row.remove());

    transactions.forEach(transaction => {
        const formattedDate = formatDate(transaction[3]);
        const formattedAmount = formatAmount(transaction[1]);
        const capitalizedCategory = transaction[2].charAt(0).toUpperCase() + transaction[2].slice(1);

        const row = `
            <tr>
                <td>${transaction[9]}</td>
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

    attachTransDeleteListeners();
    attachTransChatListeners();
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
    fetch("/api/group-update-transaction-table")
        .then(response => response.json())
        .then(data => {
            updateTransactionTable(data.trans_list);
        });
}

// attach delete listeners on table entries
function attachTransDeleteListeners() {
    document.querySelectorAll('.delete-trans-btn').forEach(button => {
        button.addEventListener('click', (event) => {
            console.log("delete button hit");
            const transactionId = event.target.getAttribute('transaction-id');
            fetch('/api/group-delete-transaction', {
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



// submit income 
const submitIncomeBtn = document.getElementById("submitIncomeBtn");
submitIncomeBtn.addEventListener("click", function() {
    event.preventDefault();
    console.log("submit income button hit")
    const formData = {
        amount: document.getElementById("incomeAmount").value,
        date: document.getElementById("incomeDate").value,
        memo: document.getElementById("incomeMemo").value    };

    fetch("/api/group-submit-income", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
        .then(data => {
            console.log(data);
            if (data.success) {
                console.log("income added succesfully")
                document.getElementById("incomeFeedbackMessage").innerText = "Income added!";
                document.getElementById("incomeAmount").value = "",
                document.getElementById("incomeDate").value = "",
                document.getElementById("incomeMemo").value = ""
                // hide category inpiut, display dropdown

                updateStats();
                fetchUpdatedIncome();
            }
            else {
                //assign each form input to the value of data.amount, data.date, etc.
                document.getElementById("incomeAmount").value = data.amount,
                document.getElementById("incomeDate").value = data.date,
                document.getElementById("incomeMemo").value = data.memo
                //document.getElementById("hidden-category").value = data.category
                if (data.return_value === 1) {
                    document.getElementById("incomeFeedbackMessage").innerText = "Date is in the future!";
                }
                else if (data.return_value === 2) {
                    document.getElementById("incomeFeedbackMessage").innerText = "Amount is not a number!";
                }
                else {
                    document.getElementById("incomeFeedbackMessage").innerText = "Date is invalid!";
                }
            }
        })
});


// update transaction table
function updateIncomeTable(income) {
    console.log("updating income");
    const tableBody = document.querySelector("#incomeTable table");

    tableBody.querySelectorAll("tr:not(:first-child)").forEach(row => row.remove());

    income.forEach(income => {
        const formattedDate = formatDate(income[2]);
        const formattedAmount = formatAmount(income[1]);

        const row = `
            <tr>
                <td>${income[8]}</td>
                <td>${formattedDate}</td>
                <td>${formattedAmount}</td>
                <td>${income[3]}</td>
                <td>
                    <button 
                        class="delete-income-btn" 
                        income-id="${income[0]}">
                        Delete
                    </button>
                </td>
            </tr>
        `;
        tableBody.innerHTML += row;
    });

    attachIncomeDeleteListeners();
    attachIncomeChatListeners();
}

function fetchUpdatedIncome() {
    console.log("fetching updated income")
    fetch("/api/group-update-income-table")
        .then(response => response.json())
        .then(data => {
            updateIncomeTable(data.income_list);
        });
}

// attach delete listeners on table entries
function attachIncomeDeleteListeners() {
    document.querySelectorAll('.delete-income-btn').forEach(button => {
        button.addEventListener('click', (event) => {
            console.log("delete button hit");
            const incomeId = event.target.getAttribute('income-id');
            fetch('/api/group-delete-income', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    income_id: incomeId
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






// change date
const submitDateBtn = document.getElementById("submitDateBtn");
submitDateBtn.addEventListener("click", function() {
    const formData = {
        month: document.getElementById("month").value,
        year: document.getElementById("year").value
    };

    fetch("/api/group-submit-date", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        }
    })
    .then(data => {
        updateStats()
        fetchUpdatedTransactions()
    })
});






// update stats
function updateStats() {
    console.log("updating stats and table")
    fetch("/api/group-update-stats", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({})  
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        }
    })
    .then(data => {
        updateStatBox(".stats .stat-box:nth-child(1)", data.total_values[0], data.total_diffs[0], data.total_diff_percs[0]);
        updateStatBox(".stats .stat-box:nth-child(2)", data.total_values[1], data.total_diffs[1], data.total_diff_percs[1]);
        updateStatBox(".stats .stat-box:nth-child(3)", data.total_values[2], data.total_diffs[2], data.total_diff_percs[2]);
    })
}

function updateStatBox(selector, value, diff, diffPerc) {
    const box = document.querySelector(selector);

    const formattedValue = (Number.isInteger(value))
        ? `$${value}.00`
        : (value.toString().includes('.') && value.toString().split('.')[1].length === 1)
            ? `$${value}0`
            : `$${value}`;

    box.querySelector("p:nth-of-type(1)").innerHTML = formattedValue;

    if (diff !== 0) {
        const formattedDiff = (diff.toString().includes('.') && diff.toString().split('.')[1].length === 1)
            ? `${diff}0` : diff;
        box.querySelector("p:nth-of-type(2)").innerHTML = `${formattedDiff} (${diffPerc}%)`;
    } else {
        box.querySelector("p:nth-of-type(2)").innerHTML = "-";
    }
}
