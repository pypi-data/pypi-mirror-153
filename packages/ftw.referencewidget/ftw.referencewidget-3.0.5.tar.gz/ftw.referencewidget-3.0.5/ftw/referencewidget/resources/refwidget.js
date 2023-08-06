(function(global, $, Handlebars) {


  $(function() {


    function initRefBrowser(button){
      var widget = this;
      widget.button = $(button);
      var buttonSelector = '#' + widget.button.attr('id');
      widget.isInTinyMce = Boolean(widget.button.attr('name') === 'browse-internal');

      if (widget.isInTinyMce) {
        // Plone 5 tinymce
        $(document).off("mouseup", buttonSelector);
        $(document).on("mouseup", buttonSelector, widget.openOverlay.bind(null, widget));
      } else {
        $(document).off("click", buttonSelector);
        $(document).on("click", buttonSelector, widget.openOverlay.bind(null, widget));
      }

      $(window).one("resize", widget.resize);

      $(document).one("keydown", function(event){
        if(event.which == 27){
          event.stopPropagation();
          overlayClose(event);
        }
      });

      widget.field = widget.button.closest(".referencewidgetField");
      widget.name = widget.field.data("fieldname");

      // XXX Implement i18n handlebars helper
      widget.translations = widget.button.closest(".referencewidget").data('trans');
      widget.request_data = {};
      widget.widget_url = "";
      widget.field_id = "";
      widget.list_template = "";
      widget.checkbox_template = "";
      widget.request_path = widget.field.data("path");
      widget.sel_type = "";
      widget.page = 1;
      widget.term = "";
      widget.search_current_path = 0;

      widget.list_template = Handlebars.compile($("#listing-template", widget.field).html());
      widget.checkbox_template = Handlebars.compile($("#checkbox-template", widget.field).html());
      widget.sel_type = widget.button.closest(".referencewidget").data("type");

      widget.loadSelectedItems(widget);

      $(document).on('OverlayContentReloaded', ".overlay", function(widget, event){
        widget.button = $('#' + widget.button.attr("id"));
        widget.loadSelectedItems(widget);
      }.bind(null, widget));
}

    initRefBrowser.prototype.loadSelectedItems = function(widget){
        var container = widget.field.find('.selected_items');
        if (!container.find('ul').is(':empty')){
          return;
        }

        $(container).find('[type="hidden"]').each(function(index, item){
          var context = {};
          var inputElement = $(item);

          if (inputElement.val() === ""){
            return;
          }

          const portal_url = $('body').data('portal-url');
          context["path"] = inputElement.val();
          context["title"] = inputElement.data("title") + " (" + context["path"].substring(portal_url.replace(window.location.origin, '').length) + ")";
          context["selectable"] = true;
          context["traversable"] = false;
          context['addclass'] = "";
          context['tag'] = "span";
          context["selected"] = "checked=\"checked\"";
          context["type"] = widget.sel_type;
          context["name"] = widget.name;
          context["uid"] = inputElement.data("uid");
          context["checkbox"] = widget.checkbox_template(context);

          inputElement.remove();

          var node = $(widget.list_template(context));
          widget.AddremoveLink(node);

          $(container).find("ul").append(node);
        });
    };

    initRefBrowser.prototype.openOverlay = function(widget, event){
      event.stopPropagation();
      event.preventDefault();
      $("body").addClass("RefBrowserOverlayOpened");
      widget.list_template = Handlebars.compile($("#listing-template", widget.field).html());
      widget.checkbox_template = Handlebars.compile($("#checkbox-template", widget.field).html());
      $(".sortable").sortable();

      var target = $(event.currentTarget);
      var container = target.closest(".referencewidget");
      widget.container = container;
      widget.sel_type = container.data("type");
      widget.field_id = widget.field.attr("id");

      if (widget.isInTinyMce) {
        widget.widget_url = container.data("url");
      } else {
        widget.widget_url = container.data("url") + "/++widget++" + widget.name;
      }
      
      var refbrowser_template = Handlebars.compile($("#refbrowser-template", widget.field).html());
      $("body").append(refbrowser_template(widget.translations));
      widget.build_pathbar(widget, "");
      widget.get_data(widget, "");

      var overlay = $(".refbrowser");
      overlay.on("click", ".path a", widget.jump_to.bind(null, widget));
      overlay.on("click", ".search button", widget.search.bind(null, widget));
      overlay.on("keypress", ".search input", function(event){
        if(event.which == 13) {
          widget.search(widget, event);
      }});

      overlay.on("change", ".listing input.ref-checkbox", widget.checkbox_flipped.bind(null, widget));
      overlay.on("change", "select", widget.reload.bind(null, widget));
      overlay.on("click", "button.cancel", function(){$(".refbrowser").remove();});
      overlay.on("click", ".ref_list_entry a", widget.switch_level.bind(null, widget));
      overlay.on("click", ".listing input.ref-checkbox", function(e) {e.stopPropagation();});
      overlay.on("click", ".refbrowser_batching a", widget.change_page.bind(null, widget));

    };

    function overlayClose(event){
      $("body").removeClass("RefBrowserOverlayOpened");
      $(".refbrowser").remove();
    }

    initRefBrowser.prototype.search = function(widget, event){
      event.stopPropagation();
      event.preventDefault();

      var term = $(".refbrowser .searchField").val();
      var search_current_path = $(".refbrowser #searchCurrentPath:checked").length;

      if (term.length === 0) {
        return;
      }


      widget.term = term;
      widget.search_current_path = search_current_path;
      widget.page = 1;
      widget.search_results(widget);
    };

    initRefBrowser.prototype.search_results = function(widget){
      var payload = {"term": widget.term,
                     "search_current_path": widget.search_current_path,
                     "request_path": widget.request_path,
                     "page": widget.page,
                     "sort_on": $('.refbrowser select[name="sort_on"]').val(),
                     "sort_order": $('.refbrowser select[name="sort_order"]').val()
                   };

      $.post(widget.widget_url + "/search_for_refs", payload, function(widget, data){
        $(".refbrowser .refbrowser_batching").remove();
        widget.build_list(widget, data);
        widget.request_data = data;
        $(".refbrowser .listing").addClass("search_result");
      }.bind(null, widget));

    };

    initRefBrowser.prototype.build_pathbar = function(widget, path){
      $.post(widget.widget_url +"/generate_pathbar", {"origin": path}, function(data){
        var hb_template = Handlebars.compile($("#node-template", widget.field).html());
        var pathbar = "";
        data.forEach(function(item){
          pathbar += hb_template(item);
        });
        $(".path").html(pathbar);
      });

    };

    initRefBrowser.prototype.switch_level = function(widget, event){
      event.preventDefault();
      event.stopPropagation();

      var target = $(event.currentTarget).parent();
      var traversable = target.data("traversable");
      if (traversable === false){
        return;
      }

      var path = target.data("path");
      widget.request_path = path;
      widget.build_pathbar(widget, path);
      widget.get_data(widget, path);
      $(".refbrowser .searchField").val("");
    };

    initRefBrowser.prototype.reload = function(widget, event){
      event.preventDefault();
      event.stopPropagation();

      if ($(".refbrowser .searchField").val().length === 0) {
        widget.get_data(widget, widget.request_path, widget.page);
      } else {
        widget.search(widget, event);
      }
    };

    initRefBrowser.prototype.change_page = function(widget, event){
      var target = $(event.currentTarget);
      if (target.hasClass("next")){
        widget.page++;
      }
      else if (target.hasClass("previous")){
        widget.page--;
      }
      else{
        widget.page = parseInt(target.text());
      }
      var listing = target.closest('.formcontrols').siblings('.listing');
      if (listing.hasClass("search_result") === true){
        widget.search_results(widget, widget.page);
      }
      else{
        widget.get_data(widget, widget.request_path, widget.page);
      }
    };

    initRefBrowser.prototype.rebuild_listing = function (widget, data){
      $(".refbrowser .listing ul").empty();
      var list_html = "";
      for (var key in data) {
        if (data.hasOwnProperty(key)) {
          var item = data[key];
          item["selected"] = "";
          item["extras"] = "";
          item["tag"] = "span";
          item["name"] = widget.name;
          var is_selected = $(".referencewidget .selected_items li[data-path=\"" + item["path"] + "\"]", widget.field);
          if (is_selected.find("input:checked").length > 0) {
            item["selected"] = "checked=\"checked\"";
          }
          item["addclass"] = "";
          if (item["traversable"]){
            item["addclass"] = "traversable";
            item["tag"] = "a";
            item["extras"] = "href='#'";
          }
          if (item["selectable"]){
            item["type"] = widget.sel_type;
            item["checkbox"] = widget.checkbox_template(item);
          }
          list_html += widget.list_template(item);
        }
      }
      $(".listing ul").append(list_html);
    };

    initRefBrowser.prototype.build_list = function(widget, data){
      $(".refbrowser .refbrowser_batching").remove();
      var batch_template = Handlebars.compile($("#batch_template", widget.field).html());
      $(".refbrowser .batchingcontainer").append(batch_template(data));
      $(".refbrowser .batchingcontainer .previous").html("&laquo;");
      $(".refbrowser .batchingcontainer .next").html("&raquo;");

      var hb_sorter = Handlebars.compile($("#sort-template", widget.field).html());
      $(".refbrowser .sorter").html(
        hb_sorter({sortOnOptions: data.sortOnOptions,
                   sortOrderOptions: data.sortOrderOptions,
                   label_sort_by: widget.translations.label_sort_by}));

      widget.rebuild_listing(widget, data["items"]);
      var height = $(".refbrowser .pathbar").outerHeight(true);
      $(".refbrowser .listing").css({ top: height + "px" });

    };

    initRefBrowser.prototype.get_data = function(widget, path, page){
      if (page === undefined){
        page = 1;
      }

      var payload = {"start": path,
                     "page": page,
                     "sort_on": $('.refbrowser select[name="sort_on"]').val(),
                     "sort_order": $('.refbrowser select[name="sort_order"]').val()
                   };

      $.post(widget.widget_url + "/get_reference_data", payload, function(widget, data){

        widget.request_data = data;
        widget.build_list(widget, widget.request_data);

      }.bind(null, widget));
    };

    initRefBrowser.prototype.jump_to = function(widget, event){
      event.stopPropagation();
      event.preventDefault();
      var item = $(event.currentTarget);
      var path = $(item).data("path");
      if ($(item).data("clickable")){
        widget.request_path = path;
        widget.build_pathbar(widget, path);
        widget.get_data(widget, path);
        $(".refbrowser .searchField").val("");
      }
    };

    initRefBrowser.prototype.resize = function(){
      $(".refbrowser .pathbar").each(function(item){
          var height = $(this).outerHeight(true);
          var listing = $(this).siblings(".listing");
          listing.css({"top": height + "px"});
        });
    };

    initRefBrowser.prototype.AddremoveLink = function(node) {
      if ($('[type="radio"]', node).length === 1) {
        var removeLink = $('<a href="#" class="removeItem">X</a>');
        removeLink.on('click', function(event){
          event.preventDefault();
          event.stopPropagation();
          $(this).parent().remove();
        });
        $(node).prepend(removeLink);
      }
      return node;
    };

    initRefBrowser.prototype.checkbox_flipped = function(widget, event){
      event.stopPropagation();
      event.preventDefault();

      var checkbox = event.currentTarget;
      if (checkbox.checked === true){
        var node = $(event.currentTarget.parentNode).clone();
        $(node).find("input").attr("name", widget.name);
        $(node).find("a").on("click", function(event){
          event.preventDefault();
          return;
        });
        var text = $.trim(node.find("span").text());
        text = text + " (" + node.data("path") + ")";
        node.find("span").text(text);

        widget.AddremoveLink(node);

        $('.selected_items ul', widget.container).append(node);

        if ($(checkbox).attr('type') === 'radio') {
            overlayClose();
        }
      }
      else {
        var query = "#" + widget.field_id + " .referencewidget .selected_items li[data-path=\"" + $(event.currentTarget.parentNode).data("path") + "\"]";
        $(query).remove();
      }
    };


    // Regular usecase
    $(window).on('load', function(event){
      var refButtons = $(".referencewidget button");
      if (refButtons.length !== 0){
        refButtons.each(function(index, button){
          new initRefBrowser(button);
        });
      }
    });    // Overlays

    $(document).on("onLoad", ".overlay", function(event){
      var refButtons = $(".referencewidget button", $(this));
      if (refButtons.length !== 0){
        refButtons.each(function(index, button){
          new initRefBrowser(button);
        });
      }
    });

    // Public api
    window.initRefBrowser = initRefBrowser;

  });


})(window, window.jQuery, window.Handlebars);
