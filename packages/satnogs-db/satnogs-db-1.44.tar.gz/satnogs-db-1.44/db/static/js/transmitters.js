/* global renderTransmittersChart */

function ppb_to_freq(freq, drift) {
    var freq_obs = freq + ((freq * drift) / Math.pow(10,9));
    return Math.round(freq_obs);
}

function format_freq(frequency) {
    if (isNaN(frequency) || frequency == ''){
        return 'None';
    } else if (frequency < 1000) {
    // Frequency is in Hz range
        return frequency.toFixed(3) + ' Hz';
    } else if (frequency < 1000000) {
        return (frequency/1000).toFixed(3) + ' kHz';
    } else {
        return (frequency/1000000).toFixed(3) + ' MHz';
    }
}
/* eslint-enable no-unused-vars */

/* eslint new-cap: "off" */
$(document).ready(function() {

    // Calculate the drifted frequencies
    $('.drifted').each(function() {
        var drifted = ppb_to_freq($(this).data('freq_or'),$(this).data('drift'));
        $(this).html(drifted);
    });

    // Format all frequencies
    $('.frequency').each(function() {
        var to_format = $(this).html();
        $(this).html(format_freq(to_format));
    });

    $('#transmitters').DataTable( {
        // the dom field controls the layout and visibility of datatable items
        // and is not intuitive at all. Without layout we have dom: 'Bftrilp' 
        // https://datatables.net/reference/option/dom
        dom: '<"row"<"d-none d-md-block col-md-6"B><"col-sm-12 col-md-6"f>>' +
        '<"row"<"col-sm-12"tr>>' +
        '<"row"<"col-sm-12 col-xl-3 align-self-center"i><"col-sm-12 col-md-6 col-xl-3 align-self-center"l><"col-sm-12 col-md-6 col-xl-6"p>>',
        buttons: [
            'colvis'
        ],
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
                targets:   0
            },
            {
                type: 'natural',
                targets: [5, 6, 7, 8, 11]
            }
        ],
        language: {
            search: 'Filter:',
            buttons: {
                colvis: 'Columns',
            }
        },
        order: [ 1, 'asc' ],
        pageLength: 25
    } );

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
        if (hash == '#list') {
            newUrl = url.split('#')[0];
        } else {
            newUrl = url.split('#')[0] + hash;
        }
        history.replaceState(null, null, newUrl);
    });

    Promise.all([
        fetch('/api/transmitters/?format=json')
            .then((response) => response.json()),
        fetch('/api/satellites/?format=json')
            .then((response) => response.json()),
    ]).then((responses) => {
        const transmittersChart = renderTransmittersChart({
            el: document.querySelector('#transmitters-chart-container'),
            transmitters: responses[0],
            satellites_list: responses[1],
        });

        transmittersChart.zoom(
            434.5,
            438.5
        );

        document.querySelector('#zoom-all').addEventListener('click', () => {
            transmittersChart.zoom(0,30000);
        });
        document.querySelector('#zoom-vhf').addEventListener('click', () => {
            transmittersChart.zoom(143,147);
        });
        document.querySelector('#zoom-uhf').addEventListener('click', () => {
            transmittersChart.zoom(434.5,438.5);
        });
    });
} );
