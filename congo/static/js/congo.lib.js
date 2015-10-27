// Creating a JavaScript Library
// http://checkman.io/blog/creating-a-javascript-library/

// Learning Advanced JavaScript
// http://ejohn.org/apps/learn/

(function (window, $) {
  var Congo = function () {
    var defaults = {
        foo: true,
        bar: 0
    };
    
    return {
      now: now,
      
      setActiveModal: setActiveModal,
      setModalIframeHeight: setModalIframeHeight,
    };

    // utils
  
    function now() {
      return new Date().getTime();
    }
    
    // modal iframe
    
    var $activeModal;
    
    function setActiveModal(activeModal) {
      $activeModal = activeModal;
    }
    
    function setModalIframeHeight(height) {
      $('iframe', $activeModal).css('height', height + 'px');
    }
    
  };
  
  if (typeof(congo) === 'undefined') {
    window.congo = Congo()
  }
  
})(window, jQuery);