require(['jquery', 'mockup-patterns-modal'], function($, Modal) {
  'use strict';
  $(document).ready(function() {
    $('.portlet-my-bookmarks-zzzzz a.bookmarks-list-link').each(function() {
      var modal = new Modal($(this), {
        content: '#content-core',
        loadLinksWithinModal: true,
        templateOptions: {
          template:
            '' +
            '<div class="<%= options.className %>">' +
            '  <div class="<%= options.classDialog %>">' +
            '    <div class="<%= options.classModal %>">' +
            '      <div class="<%= options.classHeaderName %>">' +
            '        <a class="plone-modal-close">&times;</a>' +
            '        <% if (title) { %><h2 class="plone-modal-title"><%= title %></h2><% } %>' +
            '      </div>' +
            '      <div class="<%= options.classBodyName %>">' +
            '        <div class="<%= options.classPrependName %>"><%= prepend %></div> ' +
            '        <div class="<%= options.classContentName %>"><%= content %></div>' +
            '      </div>' +
            '    </div>' +
            '  </div>' +
            '</div>'
        }
      });
    });
  });
});
