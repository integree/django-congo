// How to Create a Basic Plugin
// https://learn.jquery.com/plugins/basic-plugin-creation/

// Advanced Plugin Concepts
// https://learn.jquery.com/plugins/advanced-plugin-concepts/

// jQuery Plugin Boilerplate
// http://stefangabos.ro/jquery/jquery-plugin-boilerplate-revisited/


// exists

(function($) {
  $.fn.exists = function() {
    return this.length > 0 ? this : false;
  };
})(jQuery);


// noCopyPaste

(function ($) {
  $.fn.noCopyPaste = function() {
    return this.bind("cut copy paste contextmenu", function(e) {
      e.preventDefault();
    });
  };
}(jQuery));