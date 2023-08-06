// Define maps between Python's strftime and Luxon's and Materialize's proprietary formats
const pythonToMomentJs = {
    "%a": "EEE",
    "%A": "EEEE",
    "%w": "E",
    "%d": "dd",
    "%b": "MMM",
    "%B": "MMMM",
    "%m": "MM",
    "%y": "yy",
    "%Y": "yyyy",
    "%H": "HH",
    "%I": "hh",
    "%p": "a",
    "%M": "mm",
    "%s": "ss",
    "%f": "SSSSSS",
    "%z": "ZZZ",
    "%Z": "z",
    "%U": "WW",
    "%j": "ooo",
    "%W": "WW",
    "%u": "E",
    "%G": "kkkk",
    "%V": "WW",
};

const pythonToMaterialize = {
    "%d": "dd",
    "%a": "ddd",
    "%A": "dddd",
    "%m": "mm",
    "%b": "mmm",
    "%B": "mmmm",
    "%y": "yy",
    "%Y": "yyyy",
}

function buildDateFormat(formatString, map) {
    // Convert a Python strftime format string to another format string
    for (const key in map) {
        formatString = formatString.replace(key, map[key]);
    }
    return formatString;
}

function initDatePicker(sel) {
    // Initialize datepicker [MAT]

    // Get the date format from Django
    const dateInputFormat = get_format('DATE_INPUT_FORMATS')[0]
    const inputFormat = buildDateFormat(dateInputFormat, pythonToMomentJs);
    const outputFormat = buildDateFormat(dateInputFormat, pythonToMaterialize);

    const el = $(sel).datepicker({
        format: outputFormat,
        // Pull translations from Django helpers
        i18n: {
            months: calendarweek_i18n.month_names,
            monthsShort: calendarweek_i18n.month_abbrs,
            weekdays: calendarweek_i18n.day_names,
            weekdaysShort: calendarweek_i18n.day_abbrs,
            weekdaysAbbrev: calendarweek_i18n.day_abbrs.map(([v]) => v),

            // Buttons
            today: gettext('Today'),
            cancel: gettext('Cancel'),
            done: gettext('OK'),
        },

        // Set monday as first day of week
        firstDay: get_format('FIRST_DAY_OF_WEEK'),
        autoClose: true,
        yearRange: [new Date().getFullYear() - 100, new Date().getFullYear() + 100],
    });

    // Set initial values of datepickers
    $(sel).each(function () {
        const currentValue = $(this).val();
        if (currentValue) {
            const currentDate = luxon.DateTime.fromFormat(currentValue, inputFormat).toJSDate();
            $(this).datepicker('setDate', currentDate);
        }
    });

    return el;
}

function initTimePicker(sel) {
    // Initialize timepicker [MAT]
    return $(sel).timepicker({
        twelveHour: false,
        autoClose: true,
        i18n: {
            cancel: 'Abbrechen',
            clear: 'Löschen',
            done: 'OK'
        },
    });
}

$(document).ready(function () {
    $("dmc-datetime input").addClass("datepicker");
    $("[data-form-control='date']").addClass("datepicker");
    $("[data-form-control='time']").addClass("timepicker");

    // Initialize sidenav [MAT]
    $(".sidenav").sidenav();

    // Initialize datepicker [MAT]
    initDatePicker(".datepicker");

    // Initialize timepicker [MAT]
    initTimePicker(".timepicker");

    // Initialize tooltip [MAT]
    $('.tooltipped').tooltip();

    // Initialize select [MAT]
    $('select').formSelect();

    // Initialize dropdown [MAT]
    $('.dropdown-trigger').dropdown();

    // If JS is activated, the language form will be auto-submitted
    $('.language-field select').change(function () {
        $(this).parents(".language-form").submit();
    });

    // If auto-submit is activated (see above), the language submit must not be visible
    $(".language-submit-p").hide();

    // Initalize print button
    $("#print").click(function () {
        window.print();
    });

    // Initialize Collapsible [MAT]
    $('.collapsible').collapsible();

    // Initialize FABs [MAT]
    $('.fixed-action-btn').floatingActionButton();

    // Initialize Modals [MAT]
    $('.modal').modal();

    // Initialize image boxes [Materialize]
    $('.materialboxed').materialbox();

    // Intialize Tabs [Materialize]
    $('.tabs').tabs();

    // Sync color picker
    $(".jscolor").change(function () {
        $("#" + $(this).data("preview")).css("color", $(this).val());
    });

    // Initialise auto-completion for search bar
    window.autocomplete = new Autocomplete({minimum_length: 2});
    window.autocomplete.setup();

    // Initialize text collapsibles [MAT, own work]
    $(".text-collapsible").addClass("closed").removeClass("opened");

    $(".text-collapsible .open-icon").click(function (e) {
        var el = $(e.target).parent();
        el.addClass("opened").removeClass("closed");
    });
    $(".text-collapsible .close-icon").click(function (e) {
        var el = $(e.target).parent();
        el.addClass("closed").removeClass("opened");
    });

    // Initialize the service worker
    if ('serviceWorker' in navigator) {
        console.debug("Start registration of service worker.");
        navigator.serviceWorker.register('/serviceworker.js', {
            scope: '/'
        }).then(function() {
            console.debug("Service worker has been registered.");
        }).catch(function() {
            console.debug("Service worker registration has failed.")
        });
    }
});

// Show notice if serviceworker broadcasts that the current page comes from its cache
const channel = new BroadcastChannel("cache-or-not");
channel.addEventListener("message", event => {
    if ((event.data) && !($("#cache-alert").length)) {
        $("main").prepend('<div id="cache-alert" class="alert warning"><p><i class="material-icons left">warning</i>' + gettext("This page may contain outdated information since there is no internet connection.") + '</p> </div>')
    }
});
