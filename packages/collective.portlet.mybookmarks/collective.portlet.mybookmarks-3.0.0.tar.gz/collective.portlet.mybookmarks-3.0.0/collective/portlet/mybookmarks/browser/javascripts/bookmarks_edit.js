require(['jquery', 'mockup-patterns-sortable'], function($, Sortable) {
  'use strict';
  $(document).ready(function() {
    var absolute_url = $('body').data().portalUrl;

    var initializeSortable = function() {
      var sortable = new Sortable($('.bookmarks-wrapper .bookmark-fields'), {
        selector: $('.bookmark-field'),
        drop: function($el, delta) {
          if (delta !== 0) {
            var token = $('input[name="_authenticator"]').attr('value');
            var actualPosition = $($el).data().index;
            if (absolute_url !== undefined) {
              $.ajax({
                url: absolute_url + '/reorder-bookmarks',
                data: { delta: delta, original: actualPosition },
                method: 'POST',
                beforeSend: function(xhr, options) {
                  xhr.setRequestHeader('X-CSRF-TOKEN', token);
                }
              })
                .done(function(data) {
                  var url = $('body').data().baseUrl;
                  $('#content-core').load(
                    url + '/my-bookmarks-edit #content-core >',
                    function() {
                      initializeSortable();
                    }
                  );
                })
                .fail(function(error) {
                  console.error(error);
                });
            }
          }
        }
      });
    };

    var removeBookmark = function(field) {
      var token = $('input[name="_authenticator"]').attr('value');
      var index = field.parents('.bookmark-field').data().index;
      if (absolute_url !== undefined) {
        $.ajax({
          url: absolute_url + '/remove-bookmark',
          data: {
            index: index
          },
          method: 'POST',
          beforeSend: function(xhr, options) {
            xhr.setRequestHeader('X-CSRF-TOKEN', token);
          }
        })
          .done(function(data) {
            var result = JSON.parse(data);
            var url = $('body').data().baseUrl;
            $('#content-core').load(
              url + '/my-bookmarks-edit #content-core >',
              function() {
                initializeSortable();
              }
            );
          })
          .fail(function(error) {
            console.error(error);
          });
      }
    };

    var addBookmark = function(values) {
      var token = $('input[name="_authenticator"]').attr('value');
      if (absolute_url !== undefined) {
        $.ajax({
          url: absolute_url + '/add-external-bookmark',
          data: values,
          method: 'POST',
          beforeSend: function(xhr, options) {
            xhr.setRequestHeader('X-CSRF-TOKEN', token);
          }
        })
          .done(function(data) {
            var result = JSON.parse(data);
            var url = $('body').data().baseUrl;
            $('#content-core').load(
              url + '/my-bookmarks-edit #content-core >',
              function() {
                initializeSortable();
              }
            );
          })
          .fail(function(error) {
            console.error(error);
          });
      }
    };

    var saveData = function(field) {
      var token = $('input[name="_authenticator"]').attr('value');
      if (absolute_url !== undefined) {
        $.ajax({
          url: absolute_url + '/edit-bookmark',
          data: {
            value: field.prop('value'),
            fieldName: field.attr('name')
          },
          method: 'POST',
          beforeSend: function(xhr, options) {
            xhr.setRequestHeader('X-CSRF-TOKEN', token);
          }
        })
          .done(function(data) {
            var result = JSON.parse(data);
            var field = $('input[name="' + result.field + '"');
            var wrapper = field.parent();
            var feedbackButton = wrapper
              .siblings('.sort-column')
              .find('button .glyphicon');
            var statusClass =
              result.success === true ? 'has-success' : 'has-error';
            var statusIcon =
              result.success === true ? 'glyphicon-ok' : 'glyphicon-remove';
            wrapper.addClass(statusClass);
            feedbackButton
              .removeClass('glyphicon-option-vertical')
              .addClass(statusIcon);
            setTimeout(function() {
              wrapper.removeClass(statusClass);
              feedbackButton
                .removeClass(statusIcon)
                .addClass('glyphicon-option-vertical');
            }, 2000);
          })
          .fail(function(error) {
            console.error(error);
          });
      }
    };

    //add external bookmark
    $(document).on('submit', '.add-bookmark-form', function(e) {
      e.preventDefault();
      var $form = $(this);
      var unindexedArray = $form.serializeArray();
      var indexedArray = {};
      $.map(unindexedArray, function(n, i) {
        indexedArray[n.name] = n.value;
      });
      addBookmark(indexedArray);
    });

    //delete bookmark
    $(
      document
    ).on(
      'click',
      '.bookmarks-wrapper .bookmark-fields button.remove-bookmark',
      function(e) {
        e.preventDefault();
        removeBookmark($(e.target));
      }
    );

    // change value in fields
    $(
      document
    ).on(
      'input',
      '.bookmarks-wrapper .bookmark-fields input[type="text"]',
      function(e) {
        window.clearTimeout($(this).data('timeout'));
        $(this).data(
          'timeout',
          setTimeout(function() {
            saveData($(e.target));
          }, 1000)
        );
      }
    );

    //sortable items
    initializeSortable();
  });
});
