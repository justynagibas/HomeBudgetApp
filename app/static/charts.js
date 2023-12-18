function pie_chart(div_id, data, labels){
    const ctx = document.getElementById(div_id).getContext('2d');

    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                label: ' Amount spent: ',
                data: data,
                borderWidth: 1
            }]
        },
        options: {
            plugins: {
                legend: {
                    display: false
                },
            },
        }
    });
}

function progress_bar(div_id, percentage_in, color) {
    const ctx = document.getElementById(div_id).getContext('2d');
    var percentage = percentage_in <=100 ? percentage_in : 100;

    var stackedBarChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Category 1'],
            datasets: [
                {
                    label: 'Done',
                    data: [percentage],
                    backgroundColor: color,
                    borderWidth:0,
                    borderColor: color,
                    borderSkipped: false,
                },
                {
                    label: 'Remaining',
                    data: [100 - percentage],
                    backgroundColor: 'rgba(255, 255, 255, 0)',
                    borderWidth: 1,
                    borderColor: color,
                    borderSkipped: false,
                },
            ],
        },
        options: {
            maintainAspectRatio: false, // Disable the aspect ratio to allow resizing
            responsive: true, // Enable responsiveness
            indexAxis: 'y',
            animation: {
                duration: 0
            },
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


function categoryHistoryChart(div_id, catHistLabels, catHistData){
  const ctx = document.getElementById(div_id).getContext('2d');

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: catHistLabels,
      datasets: [{
        label: 'Planned expenses',
        data: catHistData.map(row => row[0]),
        borderWidth: 1,
        backgroundColor: 'rgba(54, 162, 235, 1)', // Fully opaque color
        borderColor: 'rgba(54, 162, 235, 1)',
      },
      {
        label: 'Actual expenses',
        data: catHistData.map(row => row[1]),
        borderWidth: 1,
        backgroundColor: 'rgba(255, 99, 132, 1)', // Fully opaque color
        borderColor: 'rgba(255, 99, 132, 1)',
      }
      ]
    },
    options: {
      layout: {
            padding: 20
        },
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
}