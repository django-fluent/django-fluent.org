/**
 * A quick hack to get WYSIWYG editors working in django-fluent-contents.
 * The inlines are created dynamically, hence a standard HTMLField from django-tinymce doesn't do much.
 * Using the JavaScript API from django-wysiwyg to enable the text editors on demand.
 *
 * TODO: This manual registration thing needs to change FAST.
 */

(function($){

  var wysiwyg_handler = {
    'enable': function($root) {
      var textarea_id = $root.find('.form-row.body textarea').attr('id');
      django_wysiwyg.enable(textarea_id, textarea_id);
    },
    'disable': function($root) {
      var textarea_id = $root.find('.form-row.body textarea').attr('id');
      django_wysiwyg.disable(textarea_id);
    }
  };

  // Make sure the WYSIWYG editor is loaded for our models.
  fluent_contents.plugins.onInitialize(function() {
    fluent_contents.plugins.registerViewHandler('Col12Item', wysiwyg_handler);
    fluent_contents.plugins.registerViewHandler('ImageTextItem', wysiwyg_handler);
  });


})(window.jQuery || django.jQuery);
