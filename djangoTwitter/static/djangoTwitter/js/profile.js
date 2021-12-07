$(".grid").masonry({
    itemSelector: '.tweets',
    gutter: 0,
})
var username = window.location.href.split('=')
console.log(username)
$.ajax({
    url: `/sentiment/${username[1]}`,
    method: 'GET',
    success: function (e) {
        Chart.defaults.global.legend.display = false;

        var sentiment = e
        var ctx = document.getElementById('tweetBySentiment').getContext('2d');
        var chart = new Chart(ctx, {
            // The type of chart we want to create
            type: 'horizontalBar',

            // The data for our dataset
            data: {
                labels: ['Great', 'Good', 'Neutral', 'Bad', 'Terrible'],
                datasets: [{
                    backgroundColor: ['rgb(66,170,95)', 'rgb(94,189,166)', 'rgb(116, 167, 180)', 'rgb(226, 105, 64)', 'rgb(207,63,63)'],
                    borderColor: ['rgb(66,170,95)', 'rgb(94,189,166)', 'rgb(116, 167, 180)', 'rgb(226, 105, 64)', 'rgb(207,63,63)'],
                    data: sentiment
                }]
            },

            // Configuration options go here
            options: {
                legend: {
                    display: false,
                    position: 'right',

                }
            }
        });
    }
})



