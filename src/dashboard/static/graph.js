
const datay= [200, 221, 258, 282, 313, 325]
const datay2= [3,5,7,6,7,5]
const ctx = document.getElementById('myChart').getContext('2d');
const myChart = new Chart(ctx, {    
    data: {
        labels: ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin'],
        datasets: [{
          type: 'bar',
            label: 'Nombre de threads', 
            data: datay,
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 2,
            yAxisID:'y' ,       
           datalabels:{
              color:'black',
              anchor:'end',
              align:'top',
              font:{
                weight:'bold',
                size:15
              },
            } ,  
        },  
      {
        type:'line',
        label: 'Nombre de relevés',
        data:datay2,
        borderWidth: 5,
        borderColor: 'rgb(58, 5, 17)',
        backgroundColor: 'rgb(58, 5, 17)',
        yAxisID:'y2',
        datalabels:{
          display:true,
          color:'rgb(58, 5, 17)',
          anchor:'start',
          align:'bottom',
          font:{
            size:17,
            weight:'bold'
          },
        } ,  
      }]
    },
    options: {                  
    
    },
   plugins: [ChartDataLabels],
        options:{
          plugins:{
            /*     tooltip:{
                  enabled:false
                },   */
                legend:{
                  
            display:false , 
                  labels:{
                    boxWidth:0
                  }
                }
              },
          scales: {
            y2:{
              title:{
                display:true,
                text:'Nombre de relevé',
                font: {
                  size: 20,
                  weight: 'bold',        
                }, 
              },
              beginAtZero:true,
              position:'right',
              suggestedMax:Math.max(...datay2)+5,
              grid:{
                display:false,
              }
            },
            y:{
              title:{
                display:true,
                text:'Nombre de Threads',
                font: {
                  size: 20,
                  weight: 'bold',        
                }, 
              },
                        
            }
        }
          
        } 
}); 

