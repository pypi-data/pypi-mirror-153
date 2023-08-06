/* eslint new-cap: "off" */
$(document).ready(function() {
    'use strict';

    // Add current copyright year
    var current_year = '-' + new Date().getFullYear();
    $('#copy').text(current_year);

    // Enable tooltips
    $('[data-toggle="tooltip"]').tooltip();

    // User Settings / API Modal Form Link
    $('.basemodal-link').each(function () {
        $(this).modalForm({
            formURL: $(this).data('form-url'),
            modalID: '#basemodal'
        });
        $(this).click(function() {
            $('#control-sidebar-toggle').ControlSidebar('toggle');
        });
    });

    // Transitional from inline alerts to Toasts
    $('.alert').each(function() {
        var alerticon = 'fas fa-question';
        var alerttitle = 'Unknown';
        var alertclass = 'alert-info';
        if ($(this).data('alertclass') == 'alert-success') {
            alerticon = 'far fa-thumbs-up';
            alerttitle = 'Success';
            alertclass = 'alert-success';
        }
        if ($(this).data('alertclass') == 'alert-error') {
            alerticon = 'fas fa-ban';
            alerttitle = 'Error';
            alertclass = 'alert-danger';
        }
        if ($(this).data('alertclass') == 'alert-warning') {
            alerticon = 'fas fa-exclamation';
            alerttitle = 'Alert';
            alertclass = 'alert-warning';
        }
        $(document).Toasts('create', {
            class: alertclass,
            title: alerttitle,
            autohide: true,
            delay: 6000,
            icon: alerticon,
            body: $(this).data('alertmessage')
        });
    });
});
