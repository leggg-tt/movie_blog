/**
 * visualization.js - Movie data visualization script
 */

$(document).ready(function() {
    // Set loading status
    $('.chart-loading').show();

    // Chart theme colors
    const chartColors = {
        rating: [
            'rgba(255, 99, 132, 0.8)',
            'rgba(255, 159, 64, 0.8)',
            'rgba(255, 205, 86, 0.8)',
            'rgba(75, 192, 192, 0.8)',
            'rgba(54, 162, 235, 0.8)'
        ],
        ratingBorder: [
            'rgb(255, 99, 132)',
            'rgb(255, 159, 64)',
            'rgb(255, 205, 86)',
            'rgb(75, 192, 192)',
            'rgb(54, 162, 235)'
        ],
        popular: 'rgba(54, 162, 235, 0.8)',
        popularBorder: 'rgb(54, 162, 235)'
    };

    // Common chart options
    const chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        animation: {
            duration: 1000,
            easing: 'easeOutQuart'
        },
        plugins: {
            legend: {
                display: false
            }
        }
    };

    // Get rating distribution data
    $.getJSON(RATINGS_DATA_URL, function(data) {
        // Hide loading status
        $('#ratings-chart').closest('.chart-container').find('.chart-loading').fadeOut();

        if (data.ratings.every(val => val === 0)) {
            // Display no data message
            $("#no-ratings-message").removeClass("d-none");
            return;
        }

        const ctx = document.getElementById('ratings-chart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['1 star', '2 stars', '3 stars', '4 stars', '5 stars'],
                datasets: [{
                    label: 'Number of ratings',
                    data: data.ratings,
                    backgroundColor: chartColors.rating,
                    borderColor: chartColors.ratingBorder,
                    borderWidth: 1,
                    borderRadius: 6
                }]
            },
            options: {
                ...chartOptions,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            precision: 0,
                            font: {
                                family: "'Poppins', sans-serif"
                            }
                        },
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        }
                    },
                    x: {
                        ticks: {
                            font: {
                                family: "'Poppins', sans-serif"
                            }
                        },
                        grid: {
                            display: false
                        }
                    }
                },
                plugins: {
                    title: {
                        display: true,
                        text: 'Movie Rating Distribution',
                        font: {
                            size: 16,
                            family: "'Poppins', sans-serif",
                            weight: 'bold'
                        },
                        padding: {
                            bottom: 20
                        }
                    },
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        titleFont: {
                            family: "'Poppins', sans-serif",
                            size: 14
                        },
                        bodyFont: {
                            family: "'Poppins', sans-serif"
                        },
                        padding: 12,
                        cornerRadius: 8,
                        displayColors: false
                    }
                }
            }
        });
    }).fail(function() {
        // Hide loading status and display no data message on failure
        $('#ratings-chart').closest('.chart-container').find('.chart-loading').fadeOut();
        $("#no-ratings-message").removeClass("d-none");
    });

    // Get most popular films data
    $.getJSON(POPULAR_FILMS_DATA_URL, function(data) {
        // Hide loading status
        $('#popular-films-chart').closest('.chart-container').find('.chart-loading').fadeOut();

        if (!data.labels || data.labels.length === 0) {
            // Display no data message
            $("#no-films-message").removeClass("d-none");
            return;
        }

        const ctx = document.getElementById('popular-films-chart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Number of reviews',
                    data: data.data,
                    backgroundColor: chartColors.popular,
                    borderColor: chartColors.popularBorder,
                    borderWidth: 1,
                    borderRadius: 6
                }]
            },
            options: {
                ...chartOptions,
                indexAxis: 'y',
                scales: {
                    x: {
                        beginAtZero: true,
                        ticks: {
                            precision: 0,
                            font: {
                                family: "'Poppins', sans-serif"
                            }
                        },
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        }
                    },
                    y: {
                        ticks: {
                            font: {
                                family: "'Poppins', sans-serif"
                            }
                        },
                        grid: {
                            display: false
                        }
                    }
                },
                plugins: {
                    title: {
                        display: true,
                        text: 'Most Popular Movies (by Reviews)',
                        font: {
                            size: 16,
                            family: "'Poppins', sans-serif",
                            weight: 'bold'
                        },
                        padding: {
                            bottom: 20
                        }
                    },
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        titleFont: {
                            family: "'Poppins', sans-serif",
                            size: 14
                        },
                        bodyFont: {
                            family: "'Poppins', sans-serif"
                        },
                        padding: 12,
                        cornerRadius: 8,
                        displayColors: false
                    }
                }
            }
        });
    }).fail(function() {
        // Hide loading status and display no data message on failure
        $('#popular-films-chart').closest('.chart-container').find('.chart-loading').fadeOut();
        $("#no-films-message").removeClass("d-none");
    });
});
