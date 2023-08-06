/* global Chart */
/* eslint new-cap: "off" */
$(document).ready(function () {
    $('#sats').DataTable({
        // the dom field controls the layout and visibility of datatable items
        // and is not intuitive at all. Without layout we have dom: 'ftrilp' 
        // https://datatables.net/reference/option/dom
        dom: '<"row"<"d-none d-md-block col-md-6"><"col-sm-12 col-md-6"f>>' +
            '<"row"<"col-sm-12"tr>>' +
            '<"row"<"col-sm-12 col-xl-3 align-self-center"i><"col-sm-12 col-md-6 col-xl-3 align-self-center"l><"col-sm-12 col-md-6 col-xl-6"p>>',
        responsive: {
            details: {
                display: $.fn.dataTable.Responsive.display.childRow,
                type: 'column'
            }
        },
        columnDefs: [
            {
                className: 'control',
                orderable: false,
                targets: 0
            },
        ],
        order: [3, 'desc'],
        pageLength: 25
    });

    $('#stations').DataTable({
        // the dom field controls the layout and visibility of datatable items
        // and is not intuitive at all. Without layout we have dom: 'ftrilp' 
        // https://datatables.net/reference/option/dom
        dom: '<"row"<"d-none d-md-block col-md-6"><"col-sm-12 col-md-6"f>>' +
            '<"row"<"col-sm-12"tr>>' +
            '<"row"<"col-sm-12 col-xl-3 align-self-center"i><"col-sm-12 col-md-6 col-xl-3 align-self-center"l><"col-sm-12 col-md-6 col-xl-6"p>>',
        responsive: {
            details: {
                display: $.fn.dataTable.Responsive.display.childRow,
                type: 'column'
            }
        },
        columnDefs: [
            {
                className: 'control',
                orderable: false,
                targets: 0
            },
        ],
        order: [2, 'desc'],
        pageLength: 25
    });

    Chart.pluginService.register({
        afterUpdate: function (chart) {
            if (chart.config.options.elements.center) {
                var helpers = Chart.helpers;
                var centerConfig = chart.config.options.elements.center;
                var globalConfig = Chart.defaults.global;
                var ctx = chart.chart.ctx;

                var fontStyle = helpers.getValueOrDefault(centerConfig.fontStyle, globalConfig.defaultFontStyle);
                var fontFamily = helpers.getValueOrDefault(centerConfig.fontFamily, globalConfig.defaultFontFamily);

                var fontSize;

                if (centerConfig.fontSize) {
                    fontSize = centerConfig.fontSize;
                }
                // figure out the best font size, if one is not specified
                else {
                    ctx.save();
                    fontSize = helpers.getValueOrDefault(centerConfig.minFontSize, 1);
                    var maxFontSize = helpers.getValueOrDefault(centerConfig.maxFontSize, 256);
                    var maxText = helpers.getValueOrDefault(centerConfig.maxText, centerConfig.text);

                    var breakage = true;
                    do {
                        ctx.font = helpers.fontString(fontSize, fontStyle, fontFamily);
                        var textWidth = ctx.measureText(maxText).width;

                        // check if it fits, is within configured limits and that we are not simply toggling back and forth
                        if (textWidth < chart.innerRadius * 2 && fontSize < maxFontSize) {
                            fontSize += 1;
                        }
                        else {
                            // reverse last step
                            fontSize -= 1;
                            breakage = false;
                        }
                    } while (breakage);
                    ctx.restore();
                }

                // save properties
                chart.center = {
                    font: helpers.fontString(fontSize, fontStyle, fontFamily),
                    fillStyle: helpers.getValueOrDefault(centerConfig.fontColor, globalConfig.defaultFontColor)
                };
            }
        },
        afterDraw: function (chart) {
            if (chart.center) {
                var centerConfig = chart.config.options.elements.center;
                var ctx = chart.chart.ctx;

                ctx.save();
                ctx.font = chart.center.font;
                ctx.fillStyle = chart.center.fillStyle;
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                var centerX = (chart.chartArea.left + chart.chartArea.right) / 2;
                var centerY = (chart.chartArea.top + chart.chartArea.bottom) / 2;
                ctx.fillText(centerConfig.text, centerX, centerY);
                ctx.restore();
            }
        },
    });

    $.getJSON('/statistics/', function (data) {
        if (data.length == 0) {
            $('#transmitters-charts h2').text('still calculating...');
            $('#transmitters-charts div').append('<p>please come back later</p>');
            $('#transmitters-numbers').hide();
        } else {
            var i;
            var h;
            var s;
            var l;
            var color;
            var mode_total = 0;
            var band_total = 0;
            // Create colors for Mode Chart
            var mode_colors = [];
            for (i = 0; i < data.mode_label.length; i++) {
                mode_total += data.mode_data[i];
            }
            for (i = 0; i < data.band_label.length; i++) {
                band_total += data.band_data[i];
            }
            for (i = 0; i < data.mode_label.length; i++) {
                // Switching to HSL to stick with hue of LSF logo
                h = 235;
                l = data.mode_data[i] / mode_total * 100;
                l *= 3; // adjust for better visibility
                s = data.mode_data[i] / mode_total * 100;
                s *= 3; // adjust for better visibility
                color = 'hsl(' + h + ',' + Math.floor(s) + '%,' + Math.floor(l) + '%)';
                mode_colors.push(color);
            }

            // Create colors for Band Chart
            var band_colors = [];
            for (i = 0; i < data.band_label.length; i++) {
                h = 235;
                l = data.band_data[i] / band_total * 100;
                l *= 1.25; // adjust for better visibility
                s = data.band_data[i] / band_total * 100;
                s *= 1.25; // adjust for better visibility
                color = 'hsl(' + h + ',' + s + '%,' + l + '%)';
                band_colors.push(color);
            }

            // Global chart configuration
            Chart.defaults.global.legend.display = false;
            Chart.defaults.global.title.display = false;

            //Mode Chart
            var mode_c = document.getElementById('modes');
            var mode_chart = new Chart(mode_c, {
                type: 'doughnut',
                data: {
                    labels: data.mode_label,
                    datasets: [{
                        backgroundColor: mode_colors,
                        data: data.mode_data,
                        borderWidth: 1
                    }]
                },
                options: {
                    elements: {
                        center: {
                            // the longest text that could appear in the center
                            maxText: '100%',
                            text: data.mode_data.length + ' Modes',
                            fontColor: '#000',
                            fontFamily: 'Helvetica Neue',
                            fontStyle: 'normal',
                            minFontSize: 1,
                            maxFontSize: 20,
                        }
                    },
                    legend: false,
                    legendCallback: function(chart) {
                        var legendHtml = [];
                        legendHtml.push('<dl class="row my-0">');
                        var item = chart.data.datasets[0];
                        for (var i=0; i < item.data.length; i++) {
                            if (item.data[i] > 9) {
                                legendHtml.push('<dt class="col-sm-8">' + chart.data.labels[i] + '</dt>');
                                legendHtml.push('<dd class="col-sm-4 my-0">' + item.data[i] + '</dd>');
                            }
                        }
            
                        legendHtml.push('</dl>');
                        return legendHtml.join('');
                    }
                }
            });
            $('#modes-footer').html(mode_chart.generateLegend());

            //Band Chart
            var band_c = document.getElementById('bands');
            var band_chart = new Chart(band_c, {
                type: 'doughnut',
                data: {
                    labels: data.band_label,
                    datasets: [{
                        backgroundColor: band_colors,
                        data: data.band_data,
                        borderWidth: 1
                    }]
                },
                options: {
                    elements: {
                        center: {
                            // the longest text that could appear in the center
                            maxText: '100%',
                            text: data.band_data.length + ' Bands',
                            fontColor: '#000',
                            fontFamily: 'Helvetica Neue',
                            fontStyle: 'normal',
                            minFontSize: 1,
                            maxFontSize: 20,
                        }
                    },
                    legend: false,
                    legendCallback: function(chart) {
                        var legendHtml = [];
                        legendHtml.push('<dl class="row my-0">');
                        var item = chart.data.datasets[0];
                        for (var i=0; i < item.data.length; i++) {
                            if (item.data[i] > 9) {
                                legendHtml.push('<dt class="col-sm-8">' + chart.data.labels[i] + '</dt>');
                                legendHtml.push('<dd class="col-sm-4 my-0">' + item.data[i] + '</dd>');
                            }
                        }
            
                        legendHtml.push('</dl>');
                        return legendHtml.join('');
                    }
                }
            });
            $('#bands-footer').html(band_chart.generateLegend());

            //HUD Stats
            $('#stats-alive').html(data.transmitters_alive);
            $('#stats-transmitters').html(data.transmitters);
            $('#stats-satellites').html(data.total_satellites);
            $('#stats-data').html(data.total_data);
        }
    }).fail(function () {
        $('.transmitters-charts').hide();
    });

    // Handle deep linking of tabbed panes
    let url = location.href.replace(/\/$/, '');
    history.replaceState(null, null, url);

    if (location.hash) {
        const hash = url.split('#');
        $('#tabs a[href="#' + hash[1] + '"]').tab('show');
        url = location.href.replace(/\/#/, '#');
        history.replaceState(null, null, url);
        setTimeout(() => {
            $(window).scrollTop(0);
        }, 400);
    }

    $('a[data-toggle="tab"]').on('click', function () {
        let newUrl;
        const hash = $(this).attr('href');
        if (hash == '#dashboard') {
            newUrl = url.split('#')[0];
        } else {
            newUrl = url.split('#')[0] + hash;
        }
        history.replaceState(null, null, newUrl);
    });
});
