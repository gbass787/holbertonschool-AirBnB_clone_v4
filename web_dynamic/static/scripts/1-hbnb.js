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
});
