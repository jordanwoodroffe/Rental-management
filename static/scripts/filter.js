/**
 * Filters users by any user fields
 */
function filterUsers() {
    let search = document.getElementById('user-filter').value;
    let users = document.getElementsByClassName('user');
    for (let i = 0; i < users.length; i++) {
        let username = users[i].querySelectorAll(".username")[0].innerHTML;
        let email = users[i].querySelectorAll(".email")[0].innerHTML;
        let fName = users[i].querySelectorAll(".fName")[0].innerHTML;
        let lName = users[i].querySelectorAll(".lName")[0].innerHTML;
        if ((!username.toLowerCase().includes(search.toLowerCase())) &&
            (!email.toLowerCase().includes(search.toLowerCase())) &&
            (!fName.toLowerCase().includes(search.toLowerCase())) &&
            (!lName.toLowerCase().includes(search.toLowerCase()))) {
            users[i].style.display = "none"; // sets to none if does not match any current filter
        } else {
            users[i].style.display = "inline-block"; // otherwise displays user card
        }
    }
}

/**
 * Filters employees by any employee fields
 */
function filterEmployees() {
    let search = document.getElementById('employee-filter').value;
    let typeSearch = document.getElementById('type-filter').value; // get selected status
    let employees = document.getElementsByClassName('employee');
    for (let i = 0; i < employees.length; i++) {
        let username = employees[i].querySelectorAll(".username")[0].innerHTML;
        let email = employees[i].querySelectorAll(".email")[0].innerHTML;
        let fName = employees[i].querySelectorAll(".fName")[0].innerHTML;
        let lName = employees[i].querySelectorAll(".lName")[0].innerHTML;
        let type = employees[i].querySelectorAll(".type")[0].innerHTML;
        if (((!username.toLowerCase().includes(search.toLowerCase())) &&
            (!email.toLowerCase().includes(search.toLowerCase())) &&
            (!fName.toLowerCase().includes(search.toLowerCase())) &&
            (!lName.toLowerCase().includes(search.toLowerCase()))) ||
            (!typeSearch.toLowerCase().includes("all") && !type.toLowerCase().includes(typeSearch.toLowerCase()))) {
            employees[i].style.display = "none"; // sets to none if does not match any current filter
        } else {
            employees[i].style.display = "inline-block"; // otherwise displays user card
        }
    }
}

/**
 * Filters models by id selected
 */
function filterModels() {
    let search = document.getElementById('model_id').value;
    console.log(search)
    let models = document.getElementsByClassName('model');
    for (let i = 0; i < models.length; i++) {
        let model_id = models[i].querySelectorAll(".model_id")[0].innerHTML;
        if (parseInt(model_id) === parseInt(search))
            models[i].style.display = "inline-block";
        else
            models[i].style.display = "none";
    }
}