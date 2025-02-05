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
const input = document.getElementById("categoryInput");
const button = document.getElementById("toggleCategoryBtn");
const categorySelect = document.getElementById("category-list");
const categoryInput = document.getElementById("add-category");

const hiddenCategory = document.getElementById("hidden-category");
hiddenCategory.value = categorySelect.value;

document.addEventListener("click", function (e) {
    // Check if the input field is visible
    if (input.style.display === "block") {
        // If the clicked element is not the category input save input to hiddenCategory
        if (!categoryInput.contains(e.target) && !button.contains(e.target)) {
            hiddenCategory.value = categoryInput.value; 
        }
    }

    console.log(categorySelect.value)
    console.log(categoryInput.value)
    console.log(hiddenCategory.value)
});

console.log(categorySelect.value)
console.log(categoryInput.value)
console.log(hiddenCategory.value)

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




// Displays the success/fail message when the form is submitted
function showSuccessMessage() {
    document.getElementById("successMessage").style.display = "block"; // Show the success message
}


function showFailMessage() {
    document.getElementById("failMessage").style.display = "block"; // Show the success message
}


