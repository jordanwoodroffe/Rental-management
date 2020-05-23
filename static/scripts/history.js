function statusChange() {
    let statusSearch = document.getElementById('status-filter').value;
    let bookings = document.getElementsByClassName('booking');
    for (let i = 0; i < bookings.length; i++) {
        let status = bookings[i].querySelectorAll(".status-value")[0].innerHTML;
        if (statusSearch.toLowerCase().includes("all")) {
            bookings[i].style.display = "inline-block";
        } else {
            if (status.toLowerCase().includes(statusSearch.toLowerCase())) {
                bookings[i].style.display = "inline-block";
            } else {
                bookings[i].style.display = "none";
            }
        }
    }
}

function carChange() {
    let carSearch = document.getElementById('car-search').value;
    let bookings = document.getElementsByClassName('booking');
    for (let i = 0; i < bookings.length; i++) {
        let rego = bookings[i].querySelectorAll('.car-rego')[0].innerHTML;
        if (rego.toLowerCase().includes(carSearch.toLowerCase())) {
            bookings[i].style.display = "inline-block";
        } else {
            bookings[i].style.display = "none";
        }
    }
}

function filter() {
    let statusSearch = document.getElementById('status-filter').value;
    let carSearch = document.getElementById('car-search').value;
    let bookings = document.getElementsByClassName('booking');
    for (let i = 0; i < bookings.length; i++) {
        let status = bookings[i].querySelectorAll(".status-value")[0].innerHTML;
        let rego = bookings[i].querySelectorAll('.car-rego')[0].innerHTML;

        if ((!rego.toLowerCase().includes(carSearch.toLowerCase())) ||
            (!status.toLowerCase().includes(statusSearch.toLowerCase()) && !statusSearch.toLowerCase().includes("all"))) {
            bookings[i].style.display = "none";
        } else {
            bookings[i].style.display = "inline-block";
        }
    }
}
