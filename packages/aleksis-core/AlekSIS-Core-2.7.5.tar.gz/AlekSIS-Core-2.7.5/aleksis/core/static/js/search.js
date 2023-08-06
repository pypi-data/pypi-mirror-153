/*
 * Based on: https://django-haystack.readthedocs.io/en/master/autocomplete.html
 *
 * © Copyright 2009-2016, Daniel Lindsley
 * Licensed under the 3-clause BSD license
 */

var Autocomplete = function (options) {
    this.form_selector = options.form_selector || '.autocomplete';
    this.url = options.url || Urls.searchbarSnippets();
    this.delay = parseInt(options.delay || 300);
    this.minimum_length = parseInt(options.minimum_length || 3);
    this.form_elem = null;
    this.query_box = null;
    this.selected_element = null;
};

Autocomplete.prototype.setup = function () {
    var self = this;

    this.form_elem = $(this.form_selector);
    this.query_box = this.form_elem.find('input[name=q]');


    $("#search-form").focusout(function (e) {
        if (!$(e.relatedTarget).hasClass("search-item")) {
            e.preventDefault();
            $("#search-results").remove();
        }
    });

    // Trigger the "keyup" event if input gets focused

    this.query_box.focus(function () {
        self.query_box.trigger("input");
    });

    this.query_box.on("input", () => {
        console.log("Input changed, fetching again...")
        var query = self.query_box.val();

        if (query.length < self.minimum_length) {
            $("#search-results").remove();
            return true;
        }

        self.fetch(query);
        return true;
    });

    // Watch the input box.
    this.query_box.keydown(function (e) {

        if (e.which === 38) { // Keypress Up
            if (!self.selected_element) {
                self.setSelectedResult($("#search-collection").children().last());
                return false;
            }

            let prev = self.selected_element.prev();
            if (prev.length > 0) {
                self.setSelectedResult(prev);
            }
            return false;
        }

        if (e.which === 40) { // Keypress Down
            if (!self.selected_element) {
                self.setSelectedResult($("#search-collection").children().first());
                return false;
            }

            let next = self.selected_element.next();
            if (next.length > 0) {
                self.setSelectedResult(next);
            }
            return false;
        }

        if (self.selected_element && e.which === 13) {
            e.preventDefault();
            window.location.href = self.selected_element.attr("href");
        }
    });

    // // On selecting a result, remove result box
    // this.form_elem.on('click', '#search-results', function (ev) {
    //     $('#search-results').remove();
    //     return true;
    // });

    // Disable browser's own autocomplete
    // We do this here so users without JavaScript can keep it enabled
    this.query_box.attr('autocomplete', 'off');
};

Autocomplete.prototype.fetch = function (query) {
    var self = this;

    $.ajax({
        url: this.url,
        data: {
            'q': query
        },
        beforeSend: (request, settings) => {
            $('#search-results').remove();
            self.setLoader(true);
        },
        success: function (data) {
            self.setLoader(false);
            self.show_results(data);
        }
    })
};

Autocomplete.prototype.show_results = function (data) {
    $('#search-results').remove();
    var results_wrapper = $('<div id="search-results">' + data + '</div>');
    this.query_box.after(results_wrapper);
    this.selected_element = null;
};

Autocomplete.prototype.setSelectedResult = function (element) {
    if (this.selected_element) {
        this.selected_element.removeClass("active");
    }
    element.addClass("active");
    this.selected_element = element;
    console.log("New element: ", element);
};

Autocomplete.prototype.setLoader = function (value) {
        $("#search-loader").css("display", (value === true ? "block" : "none"))
}
