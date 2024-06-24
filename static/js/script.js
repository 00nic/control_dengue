let ctx = document.getElementById('myChart');


let myChart = new Chart(ctx,{
  type: 'bar',
  data: {
    labels: JSON.parse(document.getElementById('labels').textContent),
    datasets: [{
      label: 'caso',
      data: JSON.parse(document.getElementById('values').textContent),
      backgroundColor:[
        'rgba(255, 99, 132, 0.2)',
        'rgba(255, 159, 64, 0.2)',
        'rgba(255, 205, 86, 0.2)',
        'rgba(755, 192, 192, 0.2)',
        'rgba(55, 162, 235, 0.2)',
        'rgba(153, 162, 235, 0.2)',
        'rgba(201, 203, 207, 0.2)',
      ],
      borderColor:[
        black
      ],
      borderWidth: 1
    }]
  },
  options: {
    scales: {
      y: {
        beginAtZero: true
      }
    }
  }
});