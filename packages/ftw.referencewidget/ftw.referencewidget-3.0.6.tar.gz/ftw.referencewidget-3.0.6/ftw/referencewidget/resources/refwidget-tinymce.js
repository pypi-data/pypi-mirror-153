define([
  'jquery',
  'underscore',
  'pat-registry',
  'tinymce',
  'mockup-patterns-tinymce-url/js/links',
  'refwidget',
  'text!link.xml',
  'mockup-patterns-tinymce'
], function($, _, registry, tinymce, links, refwidget, LinkTemplate, TinyMCE) {
  'use strict';

  // LinkType is an implicit dependency of links (Old LinkModal)
  var LinkType = registry.patterns.linktype;

  // Unregister original internal link pattern
  delete registry.patterns.internallinktype;
  delete $.fn.internallinktype;

  var InternalLink = LinkType.extend({
    name: 'internallinktype',
    trigger: '.pat-internallinktype-dummy',
    init: function() {
      LinkType.prototype.init.call(this);
      this.refwidget = new initRefBrowser(this.getEl().next()[0])
    },

    getEl: function(){
      var selected = this.$el.find('input[name="internal"]:checked');
      if (selected.length) {
        return selected;
      }
      return this.$el.find('input[name="internal"]:first');
    },

    value: function() {
      return this.getEl().data('uid');
    },

    toUrl: function() {
      var value = this.value();
      if (value) {
        return this.tinypattern.generateUrl({ UID: value });
      }
      return null;
    },
    load: function(element) {
      var val = this.tiny.dom.getAttrib(element, 'data-val');
      if (val) {
        this.set(val);
      }
    },

    set: function(val) {
      // Prepare dom for refwidget
      var widget = this.refwidget;
      var container = widget.field.find('.selected_items');
      var inputfield = $('<input type="hidden" name="internal" />');

      var url = widget.field.data('url') + "/search_for_refs";
      $.post(url, {'uid': val}, function(data){

        if (data.items.length === '') {
            // No access or delete internalt link
            return;
        }

        inputfield.data('title', data.items[0].title);
        inputfield.data('uid', data.items[0].uid);
        inputfield.val(data.items[0].path);
        inputfield.appendTo(container);
        // Yeah weird api...
        widget.loadSelectedItems(widget);
      });
    },

    attributes: function() {
      var val = this.value();
      if (val) {
        return {
          'data-val': val
        };
      }
      return {};
    }
  });

  // Unregister original internal link pattern
  delete registry.patterns.linkmodal;
  delete $.fn.linkmodal;

  var LinkModal = links.extend({
    defaults: {
      anchorSelector: 'h1,h2,h3',
      linkTypes: [
        /* available, none activate by default because these options
         * only get merged, not set.
        'internal',
        'upload',
        'external',
        'email',
        'anchor',
        'image'
        'externalImage'*/
      ],
      initialLinkType: 'internal',
      text: {
        insertHeading: 'Insert Link'
      },
      linkTypeClassMapping: {
        'internal': InternalLink,
        'upload': registry.patterns.uploadlinktype,
        'external': registry.patterns.externallinktype,
        'email': registry.patterns.emaillinktype,
        'anchor': registry.patterns.anchorlinktype,
        'image': registry.patterns.imagelinktype,
        'uploadImage': registry.patterns.uploadlinktype,
        'externalImage': LinkType
      }
    },
    // XXX: this is a temporary work around for having separated templates.
    // Image modal is going to have its own modal class, funcs and template.
    linkTypeTemplateMapping: {
      'internal': LinkTemplate,
      'upload': LinkTemplate,
      'external': LinkTemplate,
      'email': LinkTemplate,
      'anchor': LinkTemplate,
      'image': links.prototype.linkTypeTemplateMapping.image,
      'uploadImage': links.prototype.linkTypeTemplateMapping.image,
      'externalImage': links.prototype.linkTypeTemplateMapping.image
    },
  });


  // Override pat-tinymce "addLinkClicked" in order to use our new link modeal template
  TinyMCE.prototype.addLinkClicked = function() {
    var self = this;
    if (self.linkModal === null) {
      var $el = $('<div/>').insertAfter(self.$el);
      var linkTypes = ['internal', 'upload', 'external', 'email', 'anchor'];
      if(!self.options.upload){
        linkTypes.splice(1, 1);
      }
      self.linkModal = new LinkModal($el,
        $.extend(true, {}, self.options, {
          tinypattern: self,
          linkTypes: linkTypes
        })
      );
      self.linkModal.show();
    } else {
      self.linkModal.reinitialize();
      self.linkModal.show();
    }
  }
  return LinkModal;

});

