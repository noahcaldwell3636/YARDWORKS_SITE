google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawChart);

// HOW to import excel or csv data???

function drawChart(data) {
    var data = google.visualization.arrayToDataTable([
    ['Year', 'Sales'],
    ['2013',  1000],
    ['2014',  1170],
    ['2015',  660],
    ['2016',  1030]
    ]);

    var options = {
    title: 'Company Performance',
    hAxis: {title: 'Year',  titleTextStyle: {color: '#333'}},
    vAxis: {minValue: 0}
    };

    var chart = new google.visualization.AreaChart(document.getElementById('chart_div'));
    chart.draw(data, options);
}
