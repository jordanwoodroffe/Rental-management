/**
 * Filters booking history by booking status, and booked car registration number
 */
function filter() {
    let statusSearch = document.getElementById('status-filter').value; // get selected status
    let carSearch = document.getElementById('car-search').value; // get rego input
    let bookings = document.getElementsByClassName('booking'); // get booking cards
    for (let i = 0; i < bookings.length; i++) {
        let status = bookings[i].querySelectorAll(".status-value")[0].innerHTML;
        let rego = bookings[i].querySelectorAll('.car-rego')[0].innerHTML;

        if ((!rego.toLowerCase().includes(carSearch.toLowerCase())) ||
            (!status.toLowerCase().includes(statusSearch.toLowerCase()) && !statusSearch.toLowerCase().includes("all"))) {
            bookings[i].style.display = "none"; // sets to none if does not match any current filter - rego or status
        } else {
            bookings[i].style.display = "inline-block"; // otherwise displays booking card
        }
    }
}
