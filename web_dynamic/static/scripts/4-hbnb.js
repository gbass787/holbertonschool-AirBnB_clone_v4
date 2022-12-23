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

  $.ajax({
    url: 'http://127.0.0.1:5001/api/v1/places_search/',
    method: 'POST',
    data: JSON.stringify({}),
    contentType: 'application/json',
    success: function (data) {
      data.forEach(d => $('.places').append(addPlace(d)));
    }
  });

  function addPlace (place) {
    return `
    <article>
      <div class="title_box">
      <h2>${place.name}</h2>
      <div class="price_by_night">${place.price_by_night}
      </div>
      </div>
      <div class="information">
      <div class="max_guest">
      ${place.max_guest} Guest
      </div>
      <div class="number_rooms">${place.number_rooms} Bedroom
      </div>
      <div class="number_bathrooms">${place.number_bathrooms} Bathroom
      </div>
      </div>
      <div class="description">${place.description}
      </div>
    </article>
    `;
  }

  $('button').click(() => {
    $('.places').empty();
    $.ajax({
      url: 'http://127.0.0.1:5001/api/v1/places_search/',
      method: 'POST',
      data: JSON.stringify({ amenities: Object.keys(amenityIds) }),
      contentType: 'application/json',
      success: function (data) {
        data.forEach(d => $('.places').append(addPlace(d)));
      }
    });
  });
});
