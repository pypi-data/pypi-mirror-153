/*******************************************************************************

    jQuery and Bootstrap related functions.

*******************************************************************************/

$(function() {

    // Initialize date and datetime picker components.
    //$('.datepicker').datetimepicker({
    //    //locale: 'en',
    //    format: 'YYYY-MM-DD'
    //});
    //$('.datetimepicker').datetimepicker({
    //    //locale: 'en',
    //    format: 'YYYY-MM-DD HH:mm:ss'
    //});

    // Initialize linked date and datetime picker components.
    $('#datetimepicker-from').datetimepicker({
        locale: GLOBAL_LOCALE,
        format: 'YYYY-MM-DD HH:mm:ss',
        icons: {
            time: "fas fa-fw fa-clock",
            date: "fas fa-fw fa-calendar-alt",
            up:   "fas fa-fw fa-arrow-up",
            down: "fas fa-fw fa-arrow-down"
        }
    });
    $('#datetimepicker-to').datetimepicker({
        useCurrent: false, //Important! See issue #1075
        locale: GLOBAL_LOCALE,
        format: 'YYYY-MM-DD HH:mm:ss',
        icons: {
            time: "fas fa-fw fa-clock",
            date: "fas fa-fw fa-calendar-alt",
            up:   "fas fa-fw fa-arrow-up",
            down: "fas fa-fw fa-arrow-down"
        }
    });
    $("#datetimepicker-from").on("dp.change", function (e) {
        $('#datetimepicker-to').data("DateTimePicker").minDate(e.date);
    });
    $("#datetimepicker-to").on("dp.change", function (e) {
        $('#datetimepicker-from').data("DateTimePicker").maxDate(e.date);
    });

    // Initialize linked date and datetime picker components.
    $('.datetimepicker-ymdhms-from').datetimepicker({
        locale: GLOBAL_LOCALE,
        format: 'YYYY-MM-DD HH:mm:ss',
        icons: {
            time: "fas fa-fw fa-clock",
            date: "fas fa-fw fa-calendar-alt",
            up:   "fas fa-fw fa-arrow-up",
            down: "fas fa-fw fa-arrow-down"
        }
    });
    $('.datetimepicker-ymdhms-to').datetimepicker({
        useCurrent: false, //Important! See issue #1075
        locale: GLOBAL_LOCALE,
        format: 'YYYY-MM-DD HH:mm:ss',
        icons: {
            time: "fas fa-fw fa-clock",
            date: "fas fa-fw fa-calendar-alt",
            up:   "fas fa-fw fa-arrow-up",
            down: "fas fa-fw fa-arrow-down"
        }
    });
    $("#datetimepicker-from-1").on("dp.change", function (e) {
        $('#datetimepicker-to-1').data("DateTimePicker").minDate(e.date);
    });
    $("#datetimepicker-to-1").on("dp.change", function (e) {
        $('#datetimepicker-from-1').data("DateTimePicker").maxDate(e.date);
    });
    $("#datetimepicker-from-2").on("dp.change", function (e) {
        $('#datetimepicker-to-2').data("DateTimePicker").minDate(e.date);
    });
    $("#datetimepicker-to-2").on("dp.change", function (e) {
        $('#datetimepicker-from-2').data("DateTimePicker").maxDate(e.date);
    });

    // Disable built-in JS form validation in case the form`s cancel button is clicked.`
    $('input[type="submit"][value="Cancel"]').click(function(){
        $(this).parents('form:first').attr('novalidate', 'novalidate');
    });

    // Initialize linked date and datetime picker components.
    $('#datetimepicker-hm-from').datetimepicker({
        locale: GLOBAL_LOCALE,
        format: 'YYYY-MM-DD HH:mm',
        icons: {
            time: "fas fa-fw fa-clock",
            date: "fas fa-fw fa-calendar-alt",
            up:   "fas fa-fw fa-arrow-up",
            down: "fas fa-fw fa-arrow-down"
        }
    });
    $('#datetimepicker-hm-to').datetimepicker({
        useCurrent: false, //Important! See issue #1075
        locale: GLOBAL_LOCALE,
        format: 'YYYY-MM-DD HH:mm',
        icons: {
            time: "fas fa-fw fa-clock",
            date: "fas fa-fw fa-calendar-alt",
            up:   "fas fa-fw fa-arrow-up",
            down: "fas fa-fw fa-arrow-down"
        }
    });
    $("#datetimepicker-hm-from").on("dp.change", function (e) {
        $('#datetimepicker-hm-to').data("DateTimePicker").minDate(e.date);
    });
    $("#datetimepicker-hm-to").on("dp.change", function (e) {
        $('#datetimepicker-hm-from').data("DateTimePicker").maxDate(e.date);
    });

    // Initialize select pickers.
    //$('.selectpicker').selectpicker();

    // Initialize tooltips.
    $('body').tooltip({
        selector: "[data-toggle=tooltip]",
        container: "body",
    });

    // Tooltips for navbar tabs require special handling.
    $('.nav-tabs-tooltipped').tooltip({
        selector: "[data-toggle=tab]",
        trigger: 'hover',
        placement: 'top',
        animate: true,
        container: 'body'
    });

    // Initialize popovers.
    $('body').popover({
        selector: "[data-toggle=popover]",
    });
    // Custom popovers implemented using Popper.js library. The Bootstrap variant
    // does not support some advanced features.
    $('.popover-hover-container').on("mouseenter", ".popover-hover", function() {
        var ref = $(this);
        var popup = $($(this).attr("data-popover-content"));
        popup.toggleClass("hidden static-popover");
        var popper = new Popper(ref, popup, {
                placement: 'top',
                onCreate: function(data) {
                    popup.find('.popover').removeClass('top');
                    popup.find('.popover').removeClass('bottom');
                    popup.find('.popover').addClass(data.placement);
                    popper.scheduleUpdate();
                },
                onUpdate: function(data) {
                    popup.find('.popover').removeClass('top');
                    popup.find('.popover').removeClass('bottom');
                    popup.find('.popover').addClass(data.placement);
                    popper.scheduleUpdate();
                },
                modifiers: {
                    flip: {
                        behavior: ['top','bottom']
                    }
                }
        });
        ref.data('popper-instance', popper);
    });
    $('.popover-hover-container').on("mouseleave", ".popover-hover", function() {
        var ref = $(this);
        var popup = $($(this).attr("data-popover-content"));
        popup.toggleClass("hidden static-popover");
        var popper = ref.data('popper-instance');
        popper.destroy();
        ref.data('popper-instance', null);
    });

    // Callback for triggering re-render of NVD3 charts within the bootstrap tabs.
    // Without this function the charts on invisible tabs are rendered incorrectly.
    // References:
    //      https://stackoverflow.com/questions/32211346/chart-update-when-bootstrap-tab-changed
    //      https://stackoverflow.com/a/47521742
    $(document).on('shown.bs.tab', 'a[data-toggle="tab"]', function (e) {
        // Each tab navigation link points to the tab panel. Use this link
        // to get IDs of all subsequent chart containers. These IDs match the
        // IDs of the charts, use this information to update correct chart.
        $(e.currentTarget.hash + ' div.chart-container').each(function(idx) {
            console.log("Updating visualisation: " + this.id);
            update_visualisation(this.id);
        });
        // Original and now deprecated solution was really slow, because it
        // triggered update on all charts on the page, regardless of their
        // visibility to the user.
        //window.dispatchEvent(new Event('resize'));
    });

    // Callback for triggering re-render of NVD3 charts after the collapse transition
    // (collapsible sidebar for timeline charts).
    // Resources:
    //      https://stackoverflow.com/questions/9255279/callback-when-css3-transition-finishes
    //      https://stackoverflow.com/a/47521742
    $(".column-chart-sidebar").bind("transitionend webkitTransitionEnd oTransitionEnd MSTransitionEnd", function(e) {
        // Sibling of each sidebar is the container for chart. Its ID matches the
        // ID of the chart, so it is possible to trigger the update.
        $('#' + e.currentTarget.previousElementSibling.id + ' div.chart-container').each(function(idx) {
            console.log("Updating visualisation: " + this.id);
            update_visualisation(this.id);
        });
        // Original and now deprecated solution was really slow, because it
        // triggered update on all charts on the page, regardless of their
        // visibility to the user.
        //window.dispatchEvent(new Event('resize'));
    });

    // Special handling of '__EMPTY__' and '__ANY__' options in event search form
    // selects. This method stil can be improved, so that 'any' is capable of disabling
    // 'empty'.
    //$(".esf-any-empty").on("changed.bs.select", function(e, clickedIndex, newValue, oldValue) {
    //    var selected = $(e.currentTarget).val();
    //    // The empty option is mutually exclusive with everything else and has
    //    // top priority.
    //    if (selected.indexOf('__EMPTY__') != -1) {
    //        console.log('Empty selected');
    //        $(e.currentTarget).selectpicker('deselectAll');
    //        $(e.currentTarget).selectpicker('refresh');
    //        $(e.currentTarget).val('__EMPTY__');
    //        $(e.currentTarget).selectpicker('refresh');
    //    }
    //    // The any option is mutually exclusive with everything else.
    //    else if (selected.indexOf('__ANY__') != -1) {
    //        console.log('Any selected');
    //        $(e.currentTarget).selectpicker('deselectAll');
    //        $(e.currentTarget).selectpicker('refresh');
    //        $(e.currentTarget).val('__ANY__');
    //        $(e.currentTarget).selectpicker('refresh');
    //    }
    //    console.log(e, this, 'VAL', this.value, 'SEL', selected, 'CI', clickedIndex, 'NV', newValue, 'OV', oldValue);
    //});
});
