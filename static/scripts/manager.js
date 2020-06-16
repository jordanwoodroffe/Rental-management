window.onload = function() {
    // Bar chart
    var barctx = document.getElementById('barChart').getContext('2d');
    var barChart = new Chart(barctx, {
        type: 'bar',
        data: {
            labels: ['1', '2', '3', '4', 'This week'],
            datasets: [{
                label: 'New customers per week',
                data: [12, 19, 3, 5, 2, 3],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)'                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)'                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            },
            legend: {
                display: false,
            }
        }
    });

    var piectx = document.getElementById('pieChart').getContext('2d');
    // Pie chart
    var pieChart = new Chart(piectx, {
        type: 'doughnut',
        data: {
            datasets: [{
                data: [5, 40],
                backgroundColor: [
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                ],
                borderColor: [
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                ],
                borderWidth: 1
            }],

            // These labels appear in the legend and in the tooltips when hovering different arcs
            labels: [
                'In service',
                'Available'
            ]
        }
    });

    var linectx = document.getElementById('lineChart').getContext('2d');
    var stackedLine = new Chart(linectx, {
        type: 'line',
        data: {
            datasets: [{
                data: [10, 20, 30, 40, 30, 50, 20, 30, 40, 30, 50, 20, 30, 40, 30, 50, 20, 30, 40, 30, 50, 20, 30, 40, 30, 50],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                ],
                borderColor: [
                    'rgba(255, 99, 132, 0.2)',
                ],
                borderWidth: 3,
                fill: false
            }],

            // These labels appear in the legend and in the tooltips when hovering different arcs
            labels: [
                'Red',
                'Yellow',
                'Blue',
                'Green',
                'Pink',
                'Black',
                'Yellow',
                'Blue',
                'Green',
                'Pink',
                'Yellow',
                'Blue',
                'Green',
                'Pink',
                'Yellow',
                'Blue',
                'Green',
                'Pink',
            ]
        },
        options: {
            scales: {
                yAxes: [{
                    stacked: true
                }],
                xAxes: [{
                    ticks: {
                        autoSkip: true,
                        maxTicksLimit: 5
                        }
                }]
            },
            legend: {
                display: false,
            }
        }
    });
}

