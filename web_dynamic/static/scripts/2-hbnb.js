$(function () {
  const amenityIds = {};

  $('.amenities input[type=checkbox]').change(function () {
    if (this.checked) {
      amenityIds[$(this).data('name')] = $(this).data('id');
    } else {
      delete amenityIds[$(this).data('name')];
    }

    $('.amenities h4').text(Object.keys(amenityIds).join(', '));
  });

  const API_URL = 'http://127.0.0.1:5001/api/v1/status';
  $.get(API_URL, function (data, response) {
    if (response === 'success' && data.status === 'OK') {
      $('DIV#api_status').addClass('available');
    } else {
      $('DIV#api_status').removeClass('available');
    }
  });
});
