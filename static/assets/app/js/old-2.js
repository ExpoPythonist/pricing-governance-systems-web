// Scatter plot chart js
let product_scatter_plot_canvas = document.getElementById(
  "product-scatter-plot-canvas"
);

let t = () => {
  let scatterChartDataJson = [];
  $.get("/visualization/scatter-plot-chart-data")
    .then(response => {
      if (response.data.length > 0) {
        response.data.map(data => {
          //   console.log("y", data.pocket_margin);
          scatterChartDataJson.push([
            parseFloat(data.sales_volume_mt),
            parseFloat(data.pocket_margin)
          ]);
          return { x: data.pocket_margin, y: data.pocket_margin };
        });
      }
      /* START: scatter plot chart */
      console.log("scatterChartDataJson", scatterChartDataJson);
      Highcharts.chart("container", {
        title: {
          text: "Highcharts Histogram"
        },
        credits: {
          enabled: false
        },
        xAxis: [
          {
            title: { text: "Data" },
            alignTicks: false
          },
          {
            title: { text: "Histogram" },
            alignTicks: false,
            opposite: false
          }
        ],

        yAxis: [
          {
            title: { text: "Data" }
          },
          {
            title: { text: "Histogram" },
            opposite: false
          }
        ],

        series: [
          {
            name: "Line",
            type: "line",
            data: [71.5],
            baseSeries: "s1",
            zIndex: -1
          },
          {
            name: "Data",
            type: "scatter",
            data: scatterChartDataJson,
            id: "s1",
            marker: {
              radius: 1.5
            }
          }
        ]
      });
    })
    .fail(response => {
      console.log("error response", response);
    });
};

if (product_scatter_plot_canvas) {
  t();
}
