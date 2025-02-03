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
document.getElementById("toggleCategoryBtn").addEventListener("click", function() {
    const dropdown = document.getElementById("categoryDropdown");
    const input = document.getElementById("categoryInput");
    const button = document.getElementById("toggleCategoryBtn");

    if (dropdown.style.display === "none") {
        dropdown.style.display = "block";
        input.style.display = "none";
        button.textContent = "Add Category";
    } else {
        dropdown.style.display = "none";
        input.style.display = "block";
        button.textContent = "Choose Existing Category";
    }
});


// Displays the success/fail message when the form is submitted
function showSuccessMessage() {
    document.getElementById("successMessage").style.display = "block"; // Show the success message
}


function showFailMessage() {
    document.getElementById("failMessage").style.display = "block"; // Show the success message
}


