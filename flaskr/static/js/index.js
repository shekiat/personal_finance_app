



// Displays past and future years in the year select dropdown
let yearSelect = document.getElementById("year");
let currentYear = new Date().getFullYear();
let startYear = currentYear - 10; // Start from 10 years ago
let endYear = currentYear;

for (let year = startYear; year <= endYear; year++) {
    let option = document.createElement("option");
    option.value = year;
    option.textContent = year;
    if (year === currentYear) {
        option.selected = true; // Default to current year
    }
    yearSelect.appendChild(option);
}

// Displays the subcategory input field when the "Add Subcategory" button is clicked
function showInputField() {
    document.getElementById("subCategoryBtn").style.display = "block"; // Show the input box
}

// Displays the success/fail message when the form is submitted
function showSuccessMessage() {
    document.getElementById("successMessage").style.display = "block"; // Show the success message
}


function showFailMessage() {
    document.getElementById("failMessage").style.display = "block"; // Show the success message
}
