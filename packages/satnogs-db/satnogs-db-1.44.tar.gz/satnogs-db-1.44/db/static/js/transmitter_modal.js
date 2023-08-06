// This script handles adjustments in the user interface of the transmitter
// modals (like changing between Transmitter, Transceiver, and Transponder)
//
// NOTE: Since this script is loaded dynamically after page load, we have
// to be cautious of CSP requirements. Any changes to this script will need
// to have the hash recalculated and changed in settings.py under
// CSP_SCRIPT_SRC. For hash recalculation use the command:
//
// cat transmitter_modal.js | openssl sha256 -binary | openssl base64

function ppb_to_freq(freq, drift) {
    var freq_obs = freq + ((freq * drift) / Math.pow(10,9));
    return Math.round(freq_obs);
}

function freq_to_ppb(freq_obs, freq) {
    if(freq == 0){
        return 0;
    } else {
        return Math.round(((freq_obs / freq) - 1) * Math.pow(10,9));
    }
}

function transmitter_suggestion_type(selection) {
    switch(selection){
    case 'Transmitter':
        $('.input-group').has('input[name=\'uplink_low\']').addClass('d-none');
        $('.input-group').has('input[name=\'uplink_high\']').addClass('d-none');
        $('.input-group').has('input[name=\'uplink_drift_hz\']').addClass('d-none');
        $('.input-group').has('input[name=\'uplink_drift\']').addClass('d-none');
        $('.input-group').has('input[name=\'downlink_high\']').addClass('d-none');
        $('.input-group').has('input[name=\'invert\']').addClass('d-none');
        $('.input-group').has('select[name=\'uplink_mode\']').addClass('d-none');
        $('input[name=\'uplink_high\']').val('');
        $('input[name=\'downlink_high\']').val('');
        $('select[name=\'invert\']').removeAttr('checked');
        $('input[name=\'uplink_low\']').val('');
        $('input[name=\'uplink_drift\']').val('');
        $('input[name=\'uplink_drift_hz\']').val('');
        $('select[name=\'uplink_mode\']').val('');
        $('.input-group-prepend:contains(\'Downlink Low\')').html('Downlink Freq.');
        break;
    case 'Transceiver':
        $('.input-group').has('input[name=\'uplink_high\']').addClass('d-none');
        $('.input-group').has('input[name=\'downlink_high\']').addClass('d-none');
        $('.input-group').has('input[name=\'invert\']').addClass('d-none');
        $('.input-group').has('input[name=\'uplink_low\']').removeClass('d-none');
        $('.input-group').has('input[name=\'uplink_drift_hz\']').removeClass('d-none');
        $('.input-group').has('input[name=\'uplink_drift\']').removeClass('d-none');
        $('.input-group').has('select[name=\'uplink_mode\']').removeClass('d-none');
        $('input[name=\'uplink_high\']').val('');
        $('input[name=\'downlink_high\']').val('');
        $('select[name=\'invert\']').removeAttr('checked');
        $('input[name=\'downlink_low\']').prev().html('Downlink Freq.');
        $('input[name=\'uplink_low\']').prev().html('Uplink Freq.');
        break;
    case 'Transponder':
        $('.input-group').has('input[name=\'uplink_high\']').removeClass('d-none');
        $('.input-group').has('input[name=\'downlink_high\']').removeClass('d-none');
        $('.input-group').has('input[name=\'invert\']').removeClass('d-none');
        $('.input-group').has('input[name=\'uplink_low\']').removeClass('d-none');
        $('.input-group').has('input[name=\'uplink_drift\']').removeClass('d-none');
        $('.input-group').has('input[name=\'uplink_drift_hz\']').removeClass('d-none');
        $('.input-group').has('select[name=\'uplink_mode\']').removeClass('d-none');
        $('input[name=\'downlink_low\']').prev().html('Downlink low');
        $('input[name=\'uplink_low\']').prev().html('Uplink low');
        break;
    }
}

$(function () {
    // Initialize ITU Notifications URLs textarea and hide the JSON one
    $('textarea[name=\'itu_notification\']').prop('readonly', true);
    $('#itu-coordination-input-group').hide();
    var itu_urls = $.parseJSON($('textarea[name=\'itu_notification\']').val())['urls'];
    $('textarea[name=\'itu_notification_per_line\']').val(itu_urls.join('\n'));
    // Add event for changing JSON textarea when ITU Notifications URLs changes
    $('textarea[name=\'itu_notification_per_line\']').on('change click', function(){
        var itu_notification_json = $.parseJSON($('textarea[name=\'itu_notification\']').val());
        var new_itu_urls = $('textarea[name=\'itu_notification_per_line\']').val().split('\n');
        // Trim all entries and remove the empty ones
        new_itu_urls = new_itu_urls.map(function(url){
            return url.trim();
        }).filter(function (url){
            if (url.length !=0){
                return true;
            }
        });
        itu_notification_json['urls'] = new_itu_urls;
        $('textarea[name=\'itu_notification\']').val(JSON.stringify(itu_notification_json));
    });
    // Initialize frequency drift fields and their events
    $('input[name=\'uplink_drift\']').prop('readonly', true);
    var uplink_ppb = $('input[name=\'uplink_drift\']').val();
    if (uplink_ppb != 0) {
        var uplink_freq = parseInt($('input[name=\'uplink_low\']').val());
        $('input[name=\'uplink_drift_hz\']').val(ppb_to_freq(uplink_freq, uplink_ppb));
    }
    $('input[name=\'uplink_drift_hz\']').on('change click', function(){
        var freq_obs = parseInt($(this).val());
        var freq = parseInt($('input[name=\'uplink_low\']:visible').val());
        $('input[name=\'uplink_drift\']').val(freq_to_ppb(freq_obs,freq));
    });
    $('input[name=\'downlink_drift\']').prop('readonly', true);
    var downlink_ppb = $('input[name=\'downlink_drift\']').val();
    if (downlink_ppb != 0) {
        var downlink_freq = parseInt($('input[name=\'downlink_low\']').val());
        $('input[name=\'downlink_drift_hz\']').val(ppb_to_freq(downlink_freq, downlink_ppb));
    }
    $('input[name=\'downlink_drift_hz\']').on('change click', function(){
        var freq_obs = parseInt($(this).val());
        var freq = parseInt($('input[name=\'downlink_low\']:visible').val());
        $('input[name=\'downlink_drift\']').val(freq_to_ppb(freq_obs,freq));
    });
    // Initialize fields for transmitter type.
    transmitter_suggestion_type($('#id_type option:selected').text());

    $('#id_type').on('change click', function () {
        var selection = $(this).val();
        transmitter_suggestion_type(selection);
    });
});

// Enable tooltips
$('[data-toggle="tooltip"]').tooltip();
