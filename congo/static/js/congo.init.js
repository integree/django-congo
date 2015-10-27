$(document).ready(function() {
  // localStorage.clear();
  // console.log(localStorage);
  
  // modal iframe

  $('body.modal-iframe').each(function() {
    parent.congo.setModalIframeHeight(this.offsetHeight);
  });
  
  $('.modal-iframe').on('show.bs.modal', function() {
    $('.modal-body', this).html($('.modal-loading', this).html());
  });

  $('.modal-iframe').on('shown.bs.modal', function() {
    congo.setActiveModal(this);
    var body = $('.modal-body', this);
    body.html('<iframe src="' + $(this).data('src') + '" style="height: ' + (body.height() - 5) + 'px" scrolling="no"></iframe>');
  });
});