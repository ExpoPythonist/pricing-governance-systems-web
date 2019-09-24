// Scatter plot chart js
let product_scatter_plot_canvas = document.getElementById(
  "product-scatter-plot-canvas"
);

let t = () => {
  let scatterChartDataJson = [];
  $.getJSON("/visualization/scatter-plot-chart-data", response => {
    if (response.data.length > 0) {
      response.data.map(data => {
        // console.log('x', data.pocket_margin);
        scatterChartDataJson.push({
          x: data.sales_volume_mt,
          y: data.pocket_margin
        });
        // return {x: data.pocket_margin, y: data.pocket_margin}
      });
    }

    /* START: scatter plot chart */
    console.log("scatterChartDataJson", scatterChartDataJson);
    let color = Chart.helpers.color;
    let scatterChartData = {
      datasets: [
        {
          borderColor: window.chartColors.red,
          backgroundColor: color(window.chartColors.red)
            .alpha(0.5)
            .rgbString(),
          label: [],
          data: scatterChartDataJson
        }
      ]
    };

    // window.onload = function () {
    let ctx = document.getElementById("product-scatter-plot-canvas");
    let barGraph = new Chart.Scatter(ctx, {
      data: scatterChartData,
      options: {
        responsiveAnimationDuration: 1500,
        legend: {
          display: false
        },
        tooltips: {
          enabled: false,
          // position: 'average',
          // mode: 'average',
          // intersect: false,
          // caretSize: 8,
          custom: function(tooltipModel) {
            // Tooltip Element
            let tooltipEl = document.getElementById("chartjs-tooltip");

            // Create element on first render
            if (!tooltipEl) {
              tooltipEl = document.createElement("div");
              tooltipEl.id = "chartjs-tooltip";
              tooltipEl.innerHTML =
                "<table class='table table-bordered'></table>";
              document.body.appendChild(tooltipEl);
            }

            // Hide if no tooltip
            if (tooltipModel.opacity === 0) {
              tooltipEl.style.opacity = 0;
              return;
            }

            // Set caret Position
            tooltipEl.classList.remove("above", "below", "no-transform");
            if (tooltipModel.yAlign) {
              tooltipEl.classList.add(tooltipModel.yAlign);
            } else {
              tooltipEl.classList.add("no-transform");
            }

            // Set Text

            if (tooltipModel.dataPoints.length > 0) {
              tooltipModel.dataPoints.forEach(function(dataPoint) {
                let contents = //"<table class='table table-bordered'>" +
                  "<thead class=\"thead-dark\"><th class='text-center'>Volume X</th><th class='text-center'>Pocket Margin Y</th></thead>" +
                  "<tbody>" +
                  "<td class='text-center'>" +
                  dataPoint.xLabel +
                  "</td>" +
                  "<td class='text-center'>" +
                  dataPoint.yLabel +
                  "%" +
                  "</td>" +
                  "           </tbody>";
                // "</table>";
                let tableRoot = tooltipEl.querySelector("table");
                tableRoot.innerHTML = contents;
              });
            }

            // `this` will be the overall tooltip
            let position = this._chart.canvas.getBoundingClientRect();

            // Display, position, and set styles for font
            tooltipEl.style.opacity = 1;
            tooltipEl.style.position = "absolute";
            tooltipEl.style.left =
              position.left + window.pageXOffset + tooltipModel.caretX + "px";
            tooltipEl.style.top =
              position.top +
              window.pageYOffset +
              tooltipModel.caretY +
              3 +
              "px";
            tooltipEl.style.fontFamily = tooltipModel._bodyFontFamily;
            tooltipEl.style.fontSize = tooltipModel.bodyFontSize + "px";
            tooltipEl.style.fontStyle = tooltipModel._bodyFontStyle;
            tooltipEl.style.padding =
              tooltipModel.yPadding + "px " + tooltipModel.xPadding + "px";
            tooltipEl.style.pointerEvents = "none";
          }
        },
        onClick: (evt, item) => {
          console.log(evt, item);
        },
        scales: {
          xAxes: [
            {
              type: "linear",
              position: "bottom",
              ticks: {
                callback: function(value, index, values) {
                  if (Math.floor(value) === value) {
                    return value;
                  }
                }
              },
              scaleLabel: {
                labelString: "Volume",
                display: true
              }
            }
          ],
          yAxes: [
            {
              type: "linear",
              position: "left",
              ticks: {
                // min:0,
                callback: function(value, index, values) {
                  console.log(value);
                  if (Math.floor(value) === value) {
                    return value;
                  }
                },
                userCallback: function(tick) {
                  return tick.toString() + "%";
                }
              },
              scaleLabel: {
                labelString: "Pocket Margin",
                display: true
              }
            }
          ]
        }
      }
    });
  });
  // }
};

if (product_scatter_plot_canvas) {
  t();
}
/* END: scatter plot chart */
