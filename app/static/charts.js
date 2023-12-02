function pie_chart(div_id, data, labels){
    const ctx = document.getElementById(div_id).getContext('2d');

    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
            datasets: [{
                label: '# of Votes',
                data: [12, 19, 3, 5, 2, 3],
                borderWidth: 1
            }]
        },
        options: {
            plugins: {
                legend: {
                    display: false
                },
            },
            events: []
        }
    });
}

function progress_bar(div_id, percentage, color) {
    const ctx = document.getElementById(div_id).getContext('2d');

    var stackedBarChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Category 1'],
            datasets: [
                {
                    label: 'Done',
                    data: [percentage],
                    backgroundColor: color,
                    borderWidth: 0,
                    borderSkipped: false,
                },
                {
                    label: 'Remaining',
                    data: [100 - percentage],
                    backgroundColor: 'rgba(255, 255, 255, 0)',
                    borderWidth: 0,
                    borderSkipped: false,
                },
            ],
        },
        options: {
            maintainAspectRatio: false, // Disable the aspect ratio to allow resizing
            responsive: true, // Enable responsiveness
            indexAxis: 'y',
            scales: {
                x: {
                    stacked: true,
                    display: false,
                },
                y: {
                    stacked: true,
                    display: false,
                }
            },
            plugins: {
                legend: {
                    display: false,
                },
            },
            events: []
        }
    });
}
