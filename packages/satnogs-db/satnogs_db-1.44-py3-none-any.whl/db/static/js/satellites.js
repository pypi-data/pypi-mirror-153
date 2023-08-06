/* eslint new-cap: "off" */
$(document).ready(function() {
    var table = $('#sats').DataTable( {
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
        ],
        language: {
            search: 'Filter:',
            buttons: {
                colvis: 'Columns',
            }
        },
        order: [ 1, 'asc' ],
        pageLength: 50
    });

    // Create Satellite Initilization
    function createSatelliteModalForm(){
        $('.create-satellite-link').each(function () {
            $(this).modalForm({
                formURL: $(this).data('form-url'),
                modalID: '#create-satellite-modal'
            });
        });
    }

    // Update Satellite
    function updateSatelliteModalForm(){
        $('.update-satellite-link').each(function () {
            // Remove event handlers from previous draws of the table
            $(this).off('click');

            $(this).modalForm({
                formURL: $(this).data('form-url'),
                modalID: '#update-satellite-modal'
            });
        });
    }

    // Merge Satellites Initilization
    function mergeSatellitesModalForm(){
        $('.merge-satellites-link').each(function () {
            $(this).modalForm({
                formURL: $(this).data('form-url'),
                modalID: '#merge-satellites-modal',
                errorClass: '.invalid-feedback'
            });
        });
    }

    createSatelliteModalForm();
    updateSatelliteModalForm();
    mergeSatellitesModalForm();

    table.on('draw', function(){
        updateSatelliteModalForm();
    });
});
