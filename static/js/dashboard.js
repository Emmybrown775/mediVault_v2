$(function () {
	initCharts();
});

function bsEvents(){
	$('.onboarding-modal').modal('show');
}

function initDailyEnrollmentsChart() {
    fetch(`/chart_data`)
        .then(response => response.json())
        .then(data => {
            var ctx = $('#enrollments-chart');
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.labels, // Dates
                    datasets: [{
                        label: 'Daily Enrollments',
                        data: data.data, // Counts
                        backgroundColor: 'rgba(75, 192, 192, 0.7)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1,
                    }],
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    },
                    legend: {
                        display: true,
                        position: 'bottom',
                    },
                },
            });
        })
        .catch(error => console.error('Error fetching daily enrollments:', error));
}

// Call the function with a hospital ID
$(document).ready(() => initDailyEnrollmentsChart()); // Replace <hospital_id> dynamically
