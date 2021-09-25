const sparkDatesStr=$('#sparkDates').data('sparkdates');
const sparkPricesStr=$('#sparkPrices').data('sparkprices');
const sparkDatesSplit = sparkDatesStr.match(/\d+(?:\:\d+)?/g).map(String);
const sparkPrices = sparkPricesStr.match(/\d+(?:\.\d+)?/g).map(Number);
let sparkDates = [];

for (let i = 2; i < sparkDatesSplit.length ; i+=5){
    let x='';
    x+=sparkDatesSplit[i];
    x+='. ';
    x+=sparkDatesSplit[i+1];
    sparkDates.push(x);
};
Chart.Tooltip.positioners.custom = function(elements, eventPosition) {
    const tooltip = this;
    return {
        x: eventPosition.x,
        y: eventPosition.y
    };
}

const ctx = document.getElementById('sparkline-chart').getContext('2d');

const myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: sparkDates,
        datasets: [{
            data: sparkPrices,
            backgroundColor: 'transparent',
            borderColor: '#274758',
            borderWidth: 2
        }]
    },
    options: {
        hover: {
            mode: 'index',
            intersect: false
        },
        plugins:{
            tooltip:{
                position: 'custom',
                mode:'index',
                intersect:false,
                displayColors:false,
                callbacks:{
                    label: function(item, everything){
                        let value = item.formattedValue;

                        let label = '$'+value;
                        return label;
                    }
                }
            },
            legend:{
                display: false
            },
        },
        elements:{
            point:{
                pointStyle:'star',
                hoverBorderWidth:'15'
            },
            line:{
                tension:0
            }
        },
        scales: {
            y: {
                beginAtZero: false
            }
        }
    }
});