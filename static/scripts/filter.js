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

/**
 * Filter rental history by user, rego, or status
 */
function filterHistory() {
    let statusSearch = document.getElementById('status-filter').value; // get selected status
    let carSearch = document.getElementById('car-search').value; // get rego input
    let bookings = document.getElementsByClassName('booking'); // get booking cards
    let userSearch = document.getElementById('user-filter').value;
    for (let i = 0; i < bookings.length; i++) {
        let status = bookings[i].querySelectorAll(".status-value")[0].innerHTML;
        let rego = bookings[i].querySelectorAll('.car-rego')[0].innerHTML;
        let username = bookings[i].querySelectorAll(".username")[0].innerHTML;
        let email = bookings[i].querySelectorAll(".email")[0].innerHTML;
        let fName = bookings[i].querySelectorAll(".fName")[0].innerHTML;
        let lName = bookings[i].querySelectorAll(".lName")[0].innerHTML;

        if ((!rego.toLowerCase().includes(carSearch.toLowerCase())) ||
            (!status.toLowerCase().includes(statusSearch.toLowerCase()) && !statusSearch.toLowerCase().includes("all")) ||
            ((!username.toLowerCase().includes(userSearch.toLowerCase())) &&
            (!email.toLowerCase().includes(userSearch.toLowerCase())) &&
            (!fName.toLowerCase().includes(userSearch.toLowerCase())) &&
            (!lName.toLowerCase().includes(userSearch.toLowerCase())))) {
            bookings[i].style.display = "none"; // sets to none if does not match any current filter - rego or status
        } else {
            bookings[i].style.display = "inline-block"; // otherwise displays booking card
        }
    }
}

/**
 * Filter repair reports by rego and status (requested or resolved)
 */
function filterReports() {
    let statusSearch = document.getElementById('status-filter').value; // get selected status
    let carSearch = document.getElementById('car-search').value; // get rego input
    let priority = document.getElementById('priority-filter').value; // get rego input
    let reports = document.getElementsByClassName('report'); // get booking cards
    for (let i = 0; i < reports.length; i++) {
        let status = reports[i].querySelectorAll(".status-value")[0].innerHTML;
        let rego = reports[i].querySelectorAll('.car-rego')[0].innerHTML;
        let p_stat = reports[i].querySelectorAll('.priority-value')[0].innerHTML;
        if ((!rego.toLowerCase().includes(carSearch.toLowerCase())) ||
            (!status.toLowerCase().includes(statusSearch.toLowerCase()) && !statusSearch.toLowerCase().includes("all")) ||
            (!p_stat.toLowerCase().includes(priority.toLowerCase()) && !priority.toLowerCase().includes("all"))) {
            reports[i].style.display = "none"; // sets to none if does not match any current filter - rego or status
        } else {
            reports[i].style.display = "inline-block"; // otherwise displays booking card
        }
    }
}