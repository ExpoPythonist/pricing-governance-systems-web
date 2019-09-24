let is_active_get_file_status;
let is_file_upload = false;
let file_upload_progress_default_interval = 1000;

function el_id(el) {
    return document.getElementById(el);
}

function uploadFile($this, all_years) {
    let upload_year = $("#year").val();
    let is_already_upload = false;
    for(let i=0;i<all_years.length;i++){
        if (upload_year == all_years[i].year){
            is_already_upload = true;
        }
    }

    $(el_id("m_form_2_upload")).validate();
    $(el_id("upload_file")).rules("add", {
        messages: {
            required: "This FILE upload field is required",
            accept: "Only excel file is allowed."
        }
    });

    if (!$(el_id("upload_file")).valid()) {
        return false;
    }

    if (is_already_upload == true){
        swal({
            title: "File Upload Confirmation",
            text: "You already have pricing data for " + upload_year + ". Uploading a new file will delete existing data and any analysis done on that data. Are you sure you want to proceed?",
            type: "warning",
            showCancelButton: !0,
            confirmButtonText: "Yes, proceed.",
        }).then((e) => {
            if (e.value) {
                let formdata = new FormData(el_id("m_form_2_upload"));
                let ajax = new XMLHttpRequest();
                ajax.upload.addEventListener("progress", progressHandler, false);
                ajax.addEventListener("load", completeHandler, false);
                ajax.addEventListener("error", errorHandler, false);
                ajax.addEventListener("abort", abortHandler, false);
                ajax.open("POST", "/upload-file");
                ajax.send(formdata);
            } else {
                return false;
            }
        });
    }else{
        let formdata = new FormData(el_id("m_form_2_upload"));
        let ajax = new XMLHttpRequest();
        ajax.upload.addEventListener("progress", progressHandler, false);
        ajax.addEventListener("load", completeHandler, false);
        ajax.addEventListener("error", errorHandler, false);
        ajax.addEventListener("abort", abortHandler, false);
        ajax.open("POST", "/upload-file");
        ajax.send(formdata);
    }

    // $(el_id("m_form_2_upload")).validate();
    // $(el_id("upload_file")).rules("add", {
    //     messages: {
    //         required: "This FILE upload field is required",
    //         accept: "Only excel file is allowed."
    //     }
    // });

    // if (!$(el_id("upload_file")).valid()) {
    //     return false;
    // }
    // let formdata = new FormData(el_id("m_form_2_upload"));
    // let ajax = new XMLHttpRequest();
    // ajax.upload.addEventListener("progress", progressHandler, false);
    // ajax.addEventListener("load", completeHandler, false);
    // ajax.addEventListener("error", errorHandler, false);
    // ajax.addEventListener("abort", abortHandler, false);
    // ajax.open("POST", "/upload-file");
    // ajax.send(formdata);
}

function progressHandler(event) {
    el_id("upload-excel-file-btn").disabled = true;
    el_id("upload-excel-file-btn").classList.add("m-loader");
    el_id("upload-excel-file-btn").innerText = "Uploading . . .";
}

function completeHandler(event) {

    el_id("status").innerHTML = event.target.responseText;
    el_id("upload-excel-file-btn").disabled = false;
    el_id("upload-excel-file-btn").classList.remove("m-loader");
    el_id("upload-excel-file-btn").innerText = "Upload";
    el_id("reset-upload-from").click();
    if (event.currentTarget.status === 201) {
        is_file_upload = true;
        // setTimeout(() => {
        is_active_get_file_status = setInterval(get_file_upload_progress, file_upload_progress_default_interval);
        // }, 7000);
        alert_fadeout();
    }
}

function errorHandler(event) {
    el_id("status").innerHTML = "Upload Failed";
    el_id("upload-excel-file-btn").disabled = false;
    el_id("upload-excel-file-btn").classList.remove("m-loader");
    el_id("upload-excel-file-btn").innerText = "Upload";
    is_file_upload = false;
    console.log("error")
}

function abortHandler(event) {
    el_id("upload-excel-file-btn").disable = false;
    el_id("upload-excel-file-btn").classList.remove("m-loader");
    el_id("upload-excel-file-btn").innerText = "Upload";
    is_file_upload = false
}

// Get file progress
let uploaded_percentage = 0;
$(document).ready(() => {
    is_active_get_file_status = setInterval(get_file_upload_progress, file_upload_progress_default_interval);
});

function get_file_upload_progress() {
    $.get("/get-progress")
        .then(response => {
            uploaded_percentage = parseFloat(response.data);
            if (uploaded_percentage !== 0 || is_file_upload == true) {
                $("#draft-data-upload-status")
                    .css("display", "block")
                    .fadeIn();
                $("#draft-data-upload-status").addClass("active-file-upload-progess");
                $("#upload-complete-percentage")
                    .find(".value")
                    .text(uploaded_percentage.toFixed(2) + "%");
                $("#data-process-progress-bar-container").fadeIn(0);
                $("#data-process-progress-bar")
                    .css("width", uploaded_percentage.toFixed(2) + "%")
                    .attr("aria-valuenow", uploaded_percentage.toFixed(2))
                    .fadeIn();
                $("#draft-data-upload-status")
                    .find("#up-loader")
                    .removeClass("fa-check fa-times")
                    .addClass("fa-spinner fa-spin")
                    .fadeIn();
            } else {
                $("#draft-data-upload-status").fadeOut();
                $("#draft-data-upload-status").removeClass(
                    "active-file-upload-progess"
                );
                clearInterval(is_active_get_file_status);
                $("#data-process-progress-bar")
                    .css("width", 0)
                    .fadeOut();
                $("#data-process-progress-bar-container").fadeOut(0);
                is_file_upload = false;

                $("#draft-data-upload-status")
                    .find("#up-loader")
                    .removeClass("fa-spinner fa-spin fa-check")
                    .addClass("fa-times")
                    .fadeIn();
            }

            if (uploaded_percentage == 100) {
                clearInterval(is_active_get_file_status);
                $("#draft-data-upload-status").addClass(
                    "active-file-upload-progess-done"
                );
                $("#upload-complete-percentage")
                    .find(".value")
                    .text("100%");
                $("#draft-data-upload-status")
                    .find("#up-loader")
                    .removeClass("fa-spinner fa-spin fa-times")
                    .addClass("fa-check")
                    .fadeIn();
                is_file_upload = false;
            }
        })
        .fail(data => {
            clearInterval(is_active_get_file_status);
            $("#draft-data-upload-status").fadeOut();
            is_file_upload = false;
            $("#draft-data-upload-status")
                .find("#up-loader")
                .removeClass("fa-spinner fa-spin fa-check")
                .addClass("fa-times")
                .fadeIn();
        });
}

// Response table without edit option
let DatatablesExtensionsResponsive = {
    init: function (table) {
        $(table).DataTable({
            responsive: true,
            sort: false,
            paginate: false,
            filter: false,
            info: false
        });
    }
};
jQuery(document).ready(function () {
    let table = document.getElementById("data-table-response");
    if (table) DatatablesExtensionsResponsive.init(table);

    let histogram_data_table = el_id('histogram-data-table');
    if (histogram_data_table) DatatablesExtensionsResponsive.init(histogram_data_table);
});

/* BEGIN: scatter plot chart */
// Scatter plot chart js
// let product_scatter_plot_canvas = document.getElementById(
//     "product-scatter-plot-canvas"
// );


// let barGraph;
// let generate_scatter_chart = (dataParams) => {
//     $(el_id('product-scatter-plot-canvas-display')).fadeIn(0);
//     $(el_id('chartjs-loader')).fadeIn(0);
//     let scatterChartDataJson = [];

//     $.ajax({
//         type: "get",
//         url: '/visualization/scatter-plot-chart-ajax',
//         data: dataParams,
//         beforeSend: () => {
//             $(product_scatter_plot_canvas).fadeOut(0);
//             $(el_id('chartjs-loader')).fadeIn(0);
//             $(el_id('scatter-load-chart-data')).fadeOut(0);
//             $(el_id('table-data-loader')).fadeIn(0);
//             $(el_id('chart-data-error')).fadeOut(0);
//         },
//         success: (response) => {
//             $(el_id('scatter-load-chart-data')).html(response);
//             if (product_scatter_data.length > 0) {
//                 product_scatter_data.map(data => {
//                     // console.log(data);
//                     scatterChartDataJson.push({
//                         x: parseFloat(data.sales_volume_mt).toFixed(2),
//                         y: parseFloat(data.pocket_margin_percentage).toFixed(2),
//                         customer_group_name: data.customer_group_name,
//                         sold_to_region: data.sold_to_region
//                     });
//                 });
//                 $(product_scatter_plot_canvas).fadeIn(0);
//                 $(el_id('chartjs-loader')).fadeOut(0);
//                 $(el_id('scatter-load-chart-data')).fadeIn(0);
//                 $(el_id('scatter-load-chart-data')).fadeIn(0);
//                 $(el_id('table-data-loader')).fadeOut(0);
//                 $(el_id('chart-data-error')).fadeOut(0);
//                 let scatter_plot_data_table = document.getElementById(
//                     "scatter-plot-data-table"
//                 );

//                 if (scatter_plot_data_table)
//                     DatatablesExtensionsResponsive.init(scatter_plot_data_table);
//                 /* START: scatter plot chart */
//                 let color = Chart.helpers.color;
//                 let scatterChartData = {
//                     datasets: [
//                         {
//                             borderColor: window.chartColors.blue,
//                             backgroundColor: color(window.chartColors.blue)
//                                 .alpha(1)
//                                 .rgbString(),
//                             pointRadius: 2.5,
//                             pointHoverRadius: 3,
//                             label: [],
//                             data: scatterChartDataJson
//                         }
//                     ]
//                 };
//                 let ctx = document.getElementById("product-scatter-plot-canvas");
//                 barGraph = new Chart.Scatter(ctx, {
//                     data: scatterChartData,
//                     options: {
//                         response: true,
//                         maintainAspectRatio: true,
//                         responsiveAnimationDuration: 1500,
//                         legend: {
//                             display: false
//                         },
//                         tooltips: {
//                             enabled: false,
//                             custom: function (tooltipModel) {
//                                 // Tooltip Element
//                                 let tooltipEl = document.getElementById("chartjs-tooltip");

//                                 // Create element on first render
//                                 if (!tooltipEl) {
//                                     tooltipEl = document.createElement("div");
//                                     tooltipEl.id = "chartjs-tooltip";
//                                     tooltipEl.innerHTML =
//                                         "<div class='card'></div>";
//                                     document.body.appendChild(tooltipEl);
//                                 }

//                                 // Hide if no tooltip
//                                 if (tooltipModel.opacity === 0) {
//                                     tooltipEl.style.opacity = 0;
//                                     return;
//                                 }

//                                 // Set caret Position
//                                 tooltipEl.classList.remove("above", "below", "no-transform");
//                                 if (tooltipModel.yAlign) {
//                                     tooltipEl.classList.add(tooltipModel.yAlign);
//                                 } else {
//                                     tooltipEl.classList.add("no-transform");
//                                 }

//                                 // Set Text

//                                 if (tooltipModel.dataPoints.length > 0) {
//                                     tooltipModel.dataPoints.forEach(function (dataPoint) {
//                                         // console.log(dataPoint);
//                                         let contents = "<ul class='list-unstyled'>" +
//                                             "<li>Customer Name: <strong>" + scatterChartDataJson[dataPoint.index].customer_group_name + "</strong></li> " +
//                                             "<li>Volume (MT): <strong>" + dataPoint.xLabel + "MT</strong></li> " +
//                                             "<li>Pocket Margin (%): <strong>" + dataPoint.yLabel + "%" + "</strong></li> " +
//                                             "<li>Sold-To Region: <strong>" + scatterChartDataJson[dataPoint.index].sold_to_region + "</strong></li> " +
//                                             "</ul>";
//                                         let tableRoot = tooltipEl.querySelector("div");
//                                         tableRoot.innerHTML = contents;
//                                     });
//                                 }

//                                 // `this` will be the overall tooltip
//                                 let position = this._chart.canvas.getBoundingClientRect();

//                                 // Display, position, and set styles for font
//                                 tooltipEl.style.opacity = 1;
//                                 tooltipEl.style.position = "absolute";
//                                 tooltipEl.style.left =
//                                     position.left + window.pageXOffset + tooltipModel.caretX + "px";
//                                 tooltipEl.style.top =
//                                     position.top +
//                                     window.pageYOffset +
//                                     tooltipModel.caretY + 3 + "px";
//                                 tooltipEl.style.fontFamily = tooltipModel._bodyFontFamily;
//                                 tooltipEl.style.fontSize = tooltipModel.bodyFontSize + "px";
//                                 tooltipEl.style.fontStyle = tooltipModel._bodyFontStyle;
//                                 tooltipEl.style.padding =
//                                     tooltipModel.yPadding + "px " + tooltipModel.xPadding + "px";
//                                 tooltipEl.style.pointerEvents = "none";
//                             }
//                         },
//                         onClick: (evt, item) => {
//                             console.log(item);
//                         },
//                         scales: {
//                             xAxes: [
//                                 {
//                                     type: "linear",
//                                     position: "bottom",
//                                     scaleLabel: {
//                                         labelString: "Volume",
//                                         display: true
//                                     }
//                                 }
//                             ],
//                             yAxes: [
//                                 {
//                                     type: "linear",
//                                     position: "left",
//                                     ticks: {
//                                         userCallback: function (tick) {
//                                             return tick.toString() + "%";
//                                         }
//                                     },
//                                     scaleLabel: {
//                                         labelString: "Pocket Margin",
//                                         display: true
//                                     }
//                                 }
//                             ]
//                         }
//                     }
//                 });
//             } else {
//                 $(product_scatter_plot_canvas).fadeOut(0);
//                 $(el_id('chartjs-loader')).fadeOut(0);
//                 $(el_id('table-data-loader')).fadeOut(0);
//                 $(el_id('scatter-load-chart-data')).fadeIn(0);
//                 $(el_id('chart-data-error')).fadeIn(0);
//                 return false;
//             }
//         },
//         error: () => {
//             $(product_scatter_plot_canvas).fadeOut(0);
//             $(el_id('chartjs-loader')).fadeOut(0);
//         }
//     });
// };


// if (product_scatter_plot_canvas) {
//     let product = product_scatter_plot_canvas.dataset.product;
//     let customer = product_scatter_plot_canvas.dataset.customer;
//     let year = product_scatter_plot_canvas.dataset.year;
//     let dataPrams = {};
//     if (product != "None") {
//         dataPrams = {"product": product, "year": year};
//     } else if (customer != "None") {
//         dataPrams = {"customer": customer, "year": year};
//     }
//     product_scatter_plot(dataPrams);
// }

// //product-scatter-plot
// function product_scatter_plot(product) {
//     if (barGraph) barGraph.destroy();
//     $(el_id('product-scatter-plot-canvas-display')).fadeOut(0);
//     generate_scatter_chart(product);
// }

/* END: scatter plot chart */


// /* BEGIN: Waterfall chart */
// let pocket_margin_waterfall_canvas = el_id("pocket-margin-waterfall-canvas");


// let generate_waterfall_chart = (data, title_text = "Pocket Price Waterfall in $ per MT") => {
//     let dataPoints = [
//         {
//             label: "Invoice Price",
//             y: parseFloat(data.invoice_price.toFixed(2))
//         },
//         {
//             label: 'Freight Costs',
//             y: parseFloat(data.freight_costs.toFixed(2))
//         },
//         {
//             label: 'Freight Revenue',
//             y: parseFloat(data.freight_revenue.toFixed(2))
//         },
//         {
//             label: 'Other Adjustments',
//             y: parseFloat(data.other_discounts_and_rebates.toFixed(2))
//         },
//         {
//             label: 'Pocket Price',
//             y: parseFloat(data.pocket_price.toFixed(2)),
//             color: "#C7C7C7"
//         },
//         {
//             label: 'COGS',
//             y: parseFloat(data.cogs.toFixed(2))
//         },
//         {
//             label: 'Pocket Margin',
//             y: parseFloat(data.pocket_margin.toFixed(2)),
//             color: "#C7C7C7"
//         },
//         // {
//         //     label: 'Pocket Margin %',
//         //     y: parseFloat(data.pocket_margin_percentage.toFixed(2))
//         // },
//         {
//             label: "Sub Total",
//             y: parseFloat(data.pocket_margin.toFixed(2)),
//             color: "#C7C7C7"
//         }
//     ];
//     var chart = new CanvasJS.Chart(pocket_margin_waterfall_canvas, {
//         theme: "light1", // "light1", "ligh2", "dark1", "dark2"
//         animationEnabled: true,
//         title: {
//             text: title_text,
//             fontSize:22
//         },
//         axisY: {
//             title: "",
//             tickLength: 0,
//             lineThickness: 0,
//             margin: 0,
//             valueFormatString: " ",//comment this to show numeric,
//         },
//         data: [{
//             type: "waterfall",
//             indexLabel: "",
//             indexLabelFontColor: "#EEEEEE",
//             indexLabelPlacement: "inside",
//             yValueFormatString: "",
//             risingColor: "#5B9BD5",
//             fallingColor: "#ED7D31",
//             lineColor: "#222222",
//             dataPoints: dataPoints
//         }]
//     });
//     chart.render();
// };
// if (pocket_margin_waterfall_canvas) {
//     let data = single_waterfall_data;
//     generate_waterfall_chart(data);
// }


// function regenerate_waterfall($this, type) {
//     $(".waterfall-btn").removeClass('btn-info');
//     $(".waterfall-btn").addClass('btn-default');
//     if ($this.hasClass('btn-default')) {
//         $this.removeClass('btn-default');
//         $this.addClass('btn-info');
//     }
//     if (type == "single") {
//         let data3 = single_waterfall_data;
//         generate_waterfall_chart(data3);
//     } else if (type == "total") {
//         let data2 = total_waterfall_data;
//         generate_waterfall_chart(data2, "Pocket Price Waterfall in $ total MT");
//     }
// }

// /* END: Waterfall chart */

/* BEGIN: Histogram */
let histogram;


function generate_histogram() {
    let histogramBand = el_id('histogram-band');
    let histogramBand_val = parseInt(histogramBand.value);
    let year = histogramCanvas.dataset.year;
    let labels = [];
    let datas = [];
    $.ajax({
        type: "GET",
        url: "/visualization/histogram-chart",
        data: {year: year, threshold: histogramBand_val},
        dataType: "json",
        beforeSend: function (response) {
            $(histogramCanvas).fadeOut(0);
            $(el_id('chartjs-loader')).fadeIn(0);
            $(el_id('chart-data-error')).fadeOut(0);
            $(el_id('histogram-band-width-input')).fadeOut(0);
        },
        success: function (response) {
            if (response.data.length > 0) {
                response.data.map((d) => {
                    labels.push(d.last_range);
                    datas.push(d.calculated_total_percentage);
                });

                let color = Chart.helpers.color;
                let barChartData = {
                    labels: labels,
                    datasets: [{
                        label: '',
                        backgroundColor: color(window.chartColors.red).alpha(0.5).rgbString(),
                        borderColor: window.chartColors.red,
                        borderWidth: 100,
                        data: datas
                    }]
                };
                histogram = new Chart(histogramCanvas, {
                    type: 'bar',
                    data: barChartData,
                    options: {
                        responsive: true,
                        legend: {
                            display: false,
                            position: 'top',
                        },
                        title: {
                            display: true,
                            text: 'Histogram'
                        },
                        scales: {
                            xAxes: [
                                {
                                    ticks: {
                                        userCallback: function (tick) {
                                            return tick.toString() + "%";
                                        }
                                    }
                                }
                            ]
                        }
                    }
                });
                $(histogramCanvas).fadeIn(0);
                $(el_id('chartjs-loader')).fadeOut(0);
                $(el_id('chart-data-error')).fadeOut(0);
                $(el_id('histogram-band-width-input')).fadeIn(0);
            } else {
                $(histogramCanvas).fadeOut(0);
                $(el_id('chartjs-loader')).fadeOut(0);
                $(el_id('chart-data-error')).fadeIn(0);
                $(el_id('histogram-band-width-input')).fadeOut(0);
            }
        },
        error: function (xhr) {
            $(histogramCanvas).fadeOut(0);
            $(el_id('chartjs-loader')).fadeOut(0);
            $(el_id('chart-data-error')).fadeIn(0);
            $(el_id('histogram-band-width-input')).fadeIn(0);
        }
    });
}

let histogramCanvas = el_id('histogram-canvas');
if (histogramCanvas) {
    if (histogram) histogram.destroy();
    generate_histogram();
}

function update_histogram_by_bandwidth() {
    if (histogram) histogram.destroy();
    generate_histogram();

}

/*END: Histogram*/
function abbrNum(number, decPlaces) {
    // 2 decimal places => 100, 3 => 1000, etc
    decPlaces = Math.pow(10, decPlaces);

    // Enumerate number abbreviations
    var abbrev = ["K", "M", "B", "T"];

    // Go through the array backwards, so we do the largest first
    for (var i = abbrev.length - 1; i >= 0; i--) {

        // Convert array index to "1000", "1000000", etc
        var size = Math.pow(10, (i + 1) * 3);

        // If the number is bigger or equal do the abbreviation
        if (size <= number) {
            // Here, we multiply by decPlaces, round, and then divide by decPlaces.
            // This gives us nice rounding to a particular decimal place.
            number = Math.round(number * decPlaces / size) / decPlaces;

            // Handle special case where we round up to the next abbreviation
            if ((number == 1000) && (i < abbrev.length - 1)) {
                number = 1;
                i++;
            }

            // Add the letter for the abbreviation
            number += abbrev[i];

            // We are done... stop
            break;
        }
    }

    return number;
}

let dynamicColors = () => {
    let r = Math.floor(Math.random() * 255);
    let g = Math.floor(Math.random() * 255);
    let b = Math.floor(Math.random() * 255);
    return "rgb(" + r + "," + g + "," + b + ")";
};
/* BEGIN:  Profit Pie chart */
if (el_id('chart-area-profit-center')) {
    let p1_data = [];
    let p1_data2 = [];
    let coloR = [];
    let total_percentage = 0;
    $(el_id('chartjs-loader-one')).fadeIn(0);
    $(el_id('chart-data-error-one')).fadeOut(0);
    $(el_id('chart-area-profit-center')).fadeOut(0);
    $.getJSON('/visualization/get-pie-chart-data/' + year, {}, (response) => {
        if (!$.isEmptyObject(response)) {
            total_percentage = convert_volume(response.sum_of_all_sales_volume);
            response.sales_by_profit_center.map(data => {
                p1_data.push(convert_volume(data.total_sales_volume));
                p1_data2.push(data.profit_center_name + abbrNum(convert_volume(data.total_sales_volume).toFixed(2), 2) + " " + default_volume + " / " + data.ratio.toFixed(2) + '%');
                // total_percentage +=  data.ratio;
                coloR.push(dynamicColors());
            });
            $(el_id('chartjs-loader-one')).fadeOut(0);
            $(el_id('chart-data-error-one')).fadeOut(0);
            $(el_id('chart-area-profit-center')).fadeIn(0);
        } else {
            $(el_id('chartjs-loader-one')).fadeOut(0);
            $(el_id('chart-data-error-one')).fadeIn(0);
            $(el_id('chart-area-profit-center')).fadeOut(0);
        }

        let config = {
            type: 'doughnut',
            plugins: [{
                beforeDraw: function (chart, options) {
                    if (chart.config.centerText.display !== null &&
                        typeof chart.config.centerText.display !== 'undefined' &&
                        chart.config.centerText.display) {
                        profitCenterPieChartCenterText(chart);
                    }
                }
            }],
            data: {
                datasets: [{
                    data: p1_data,
                    backgroundColor: coloR,
                    label: 'Dataset 1'
                }],
                labels: p1_data2,
            },
            options: {
                responsive: true,
                legend: false,
                // legend: {
                //     display: true,
                //     position: 'right',
                //     labels: {
                //         usePointStyle: true
                //     }
                // },
                legendCallback: function (chart) {
                    let text = [];
                    text.push('<ul class="list-unstyled ' + chart.id + '-legend">');
                    for (let i = 0; i < chart.data.datasets[0].data.length; i++) {
                        // console.log(chart);
                        text.push('<li><span class="pie-legend" style="background-color:' + chart.data.datasets[0].backgroundColor[i] + '"></span><span class="pie-tegend-text">');
                        if (chart.data.labels[i]) {
                            text.push(chart.data.labels[i]);
                        }
                        text.push('</span></li>');
                    }
                    text.push('</ul>');
                    return text.join("");
                },
                title: {
                    display: false,
                    text: 'Sales By Profit Center'
                },
                cutoutPercentage: 80,
                animation: {
                    animateScale: true,
                    animateRotate: true
                }
            },

            centerText: {
                display: true,
                text: abbrNum(total_percentage, 1),
                subText: ""
            }
        };
        let ctx = el_id('chart-area-profit-center').getContext('2d');
        if (total_percentage > 0) {
            let centerTextHTML = "<div id='profit-center-piechart-center-text' class=\"donut-inner\">\n" +
                "<span>Total</span>\n" +
                "<h5>" + abbrNum(total_percentage, 2) + "</h5>\n" +
                "</div>";
            $(el_id('chart-area-profit-center')).parent().append(centerTextHTML);
        }
        let myChartD2 = new Chart(ctx, config);
        $("#chartjs-legend-two").html(myChartD2.generateLegend());
    });
}

/* END: Profit Pie chart */

function profitCenterPieChartCenterText(chart) {

    let width = chart.chart.width;
    let height = chart.chart.height;
    let ctx = chart.chart.ctx;
    if (el_id('profit-center-piechart-center-text')) {
        el_id('profit-center-piechart-center-text').style.left = width / 2 + "px"
    }
}


/* BEGIN:  creight  Pie chart */


if (el_id('chart-area-creight-cost-type')) {
    let p2_data = [];
    let p2_data_2 = [];
    let coloR = [];
    let total_percentage = 0;
    $(el_id('chartjs-loader-two')).fadeIn(0);
    $(el_id('chart-data-error-two')).fadeOut(0);
    $(el_id('chart-area-creight-cost-type')).fadeOut(0);
    $.getJSON('/visualization/get-pie-chart-data/' + year, {}, (response) => {
        if (!$.isEmptyObject(response)) {
            total_percentage = response.sum_of_all_freight_costs;
            response.freight_costs_by_freight_types.map(data => {
                p2_data.push(Math.abs(data.total_freight_costs));
                p2_data_2.push(data.freight_types + " " + "$" + abbrNum(Math.abs(data.total_freight_costs).toFixed(2), 2) + " / " + data.ratio.toFixed(2) + '%');
                coloR.push(dynamicColors());
            });
            $(el_id('chartjs-loader-two')).fadeOut(0);
            $(el_id('chart-data-error-two')).fadeOut(0);
            $(el_id('chart-area-creight-cost-type')).fadeIn(0);
        } else {
            $(el_id('chartjs-loader-two')).fadeOut(0);
            $(el_id('chart-data-error-two')).fadeIn(0);
            $(el_id('chart-area-creight-cost-type')).fadeOut(0);
        }
        let config2 = {
            type: 'doughnut',
            plugins: [{
                beforeDraw: function (chart, options) {
                    if (chart.config.centerText.display !== null &&
                        typeof chart.config.centerText.display !== 'undefined' &&
                        chart.config.centerText.display) {
                        frightCostPieChartCenterText(chart);
                    }
                }
            }],
            data: {
                datasets: [{
                    data: p2_data,
                    backgroundColor: coloR,
                    label: 'Dataset 1'
                }],
                labels: p2_data_2
            },
            options: {
                responsive: true,
                legend: false,
                // legend: {
                //     display: true,
                //     position: 'right',
                //     labels: {
                //         usePointStyle: true
                //     }
                // },
                legendCallback: function (chart) {
                    let text = [];
                    text.push('<ul class="list-unstyled ' + chart.id + '-legend">');
                    for (let i = 0; i < chart.data.datasets[0].data.length; i++) {
                        // console.log(chart);
                        text.push('<li><span class="pie-legend" style="background-color:' + chart.data.datasets[0].backgroundColor[i] + '"></span><span class="pie-tegend-text">');
                        if (chart.data.labels[i]) {
                            text.push(chart.data.labels[i]);
                        }
                        text.push('</span></li>');
                    }
                    text.push('</ul>');
                    return text.join("");
                },
                title: {
                    display: false,
                    text: 'Freight Costs By Freight Type'
                },
                cutoutPercentage: 80,
                animation: {
                    animateScale: true,
                    animateRotate: true
                }
            },
            centerText: {
                display: true,
                text: abbrNum(total_percentage, 1),
                subText: ""
            }
        };
        let ctx2 = el_id('chart-area-creight-cost-type').getContext('2d');
        if (abbrNum(Math.abs(total_percentage) > 0)) {
            let centerTextHTML = "<div id='fright-cost-pie-chart-center-text' class=\"donut-inner\">\n" +
                "<span>Total</span>\n" +
                "<h5>" + abbrNum(Math.abs(total_percentage), 2) + "</h5>\n" +
                "</div>";
            $(el_id('chart-area-creight-cost-type')).parent().append(centerTextHTML);
        }
        let myChartD = new Chart(ctx2, config2);
        $("#chartjs-legend").html(myChartD.generateLegend());
    });

}

function frightCostPieChartCenterText(chart) {

    let width = chart.chart.width;
    let height = chart.chart.height;
    let ctx = chart.chart.ctx;
    if (el_id('fright-cost-pie-chart-center-text')) {
        el_id('fright-cost-pie-chart-center-text').style.left = width / 2 + "px"
    }
}

/* END: creight Pie chart */

//change_data_status
function change_data_status($this) {
    let status = parseInt($this.find('input[name="status"]').val());
    let btn_txt, title, txt;
    if (status === 1) {
        btn_txt = "Yes, finalize it!";
        title = "";
        txt = "Any data you have already uploaded for this year will be deleted. You will not be able to undo this. Are you sure you want to proceed? ";
    } else {
        title = "Are you sure?";
        btn_txt = "Yes, delete it!";
        txt = "This data will be deleted. You won't be able to revert this!"
    }

    swal({
        title: title,
        text: txt,
        type: "warning",
        showCancelButton: !0,
        confirmButtonText: btn_txt,
    }).then((e) => {
        if (e.value) {
            $.ajax({
                type: 'POST',
                url: $this.attr('action'),
                data: $this.serialize(),
                dataType: 'json',
                beforeSend: () => {
                    swal("Please wait a bit. Your request is in progress!", "info");
                },
                success: (response) => {
                    if (response.status === 200) {
                        swal("Data information successfully changed!", "success");
                    } else {
                        swal("Error! Data information remains unchanged!", 'error');
                    }
                    setTimeout(() => {
                        window.location.reload();
                    }, 2000);
                },
                error: (response) => {
                    swal("Error! Data information remains unchanged!", 'error');
                }
            })

        } else {
            swal("Data information remains unchanged!");
        }
    });
    return false;
}

// let chartjs_loader_generating_data = el_id('chartjs-loader-generating-data');
// let generate_list_prices = el_id('generate-list-prices');
// if (generate_list_prices) {
//     $.ajax({
//         url: '/visualization/scatter-plot-analysis-data',
//         data: {year: generate_list_prices.dataset.year, product: generate_list_prices.dataset.product},
//         beforeSend: (xhr) => {
//             $(chartjs_loader_generating_data).css('display', 'flex');
//         },
//         success: (response) => {
//             // console.log(response);
//             $(generate_list_prices).html(response).fadeIn(0);
//             $(chartjs_loader_generating_data).fadeOut(0);
//         }
//     });
// }

//alert-fadeout-time
function alert_fadeout() {
    setTimeout(function () {
        $('.alert-fadeout-time-t').fadeOut(1000);
    }, 2000);
}

let query = $(document).ready(function () {
    alert_fadeout();
});

let product_list_select2 = el_id('all_product_list_select2');
if (product_list_select2) {
    $(product_list_select2).select2({
        placeholder: 'Select product family...',
        width: '100%',
        allowClear: true,
        ajax: {
            url: '/visualization/product-family',
            delay: 250, // wait 250 milliseconds before triggering the request
            dataType: 'json',
            data: function (params) {
                return {
                    keyword: params.term || "",
                    page: params.page || 1,
                    year: year
                }
            },
            processResults: function (data, page) {
                let alldata = [];
                if (data.data.length > 0) {
                    data.data.map(d => {
                        alldata.push({"id": d.product_family, "text": d.product_family})
                    });
                }
                return {
                    results: alldata,
                    pagination: {
                        // more: true
                        more: (data.page * 50) < data.total_count
                    }
                };
            },
            cache: true
        }
    })
}

let customer_list_select2 = el_id('all_customer_list_select2');
if (customer_list_select2) {
    $(customer_list_select2).select2({
        placeholder: 'Select customer...',
        width: '100%',
        allowClear: true,
        ajax: {
            url: '/visualization/customers',
            delay: 250, // wait 250 milliseconds before triggering the request
            dataType: 'json',
            data: function (params) {
                return {
                    keyword: params.term || "",
                    page: params.page || 1,
                    year: year
                }
            },
            processResults: function (data, page) {
                let alldata = [];
                if (data.data.length > 0) {
                    data.data.map(d => {
                        alldata.push({"id": d, "text": d})
                    });
                }
                return {
                    results: alldata,
                    pagination: {
                        // more: true
                        more: (data.page * 50) < data.total_count
                    }
                };
            },
            cache: true
        }
    })
}


let get_product_scatterplot_data = (year,product) =>{
    $.ajax({
        url: '/visualization/ajax/product-scatterplot',
        data: {year: year, product: product},
        beforeSend: (xhr) => {
            $("#ajax-product-scatterplot-container").html("").fadeOut(0);
            $("#ajax-product-waterfall-container").html("").fadeOut(0);
        },
        success: (response) => {
            $("#ajax-product-scatterplot-container").html(response).fadeIn(0);
        }
    });
}

let  get_product_waterfall_data = (year,product, customer) =>{
    // console.log(year,product,customer);
    $.ajax({
        url: '/visualization/ajax/product-waterfall',
        data: {year: year, product: product, customer: customer},
        beforeSend: (xhr) => {
            $("#ajax-product-waterfall-container").html("").fadeOut(0);
        },
        success: (response) => {
            $("#ajax-product-waterfall-container").html(response).fadeIn(0);
        }
    });
}
