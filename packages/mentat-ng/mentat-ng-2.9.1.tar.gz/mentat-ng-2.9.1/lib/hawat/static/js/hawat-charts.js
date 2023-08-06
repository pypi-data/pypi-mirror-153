/*******************************************************************************

    FUNCTIONS FOR CHARTS AND DATASET TABLES.

*******************************************************************************/

// The visualisation registry was implemented due to the necessity to update
// specific visualisations on tab change. It is currently still proof of concept.
var VISUALISATION_REGISTRY = {};
var KW_REST = '__REST__';
var KW_DATE = '_date';
var TOPLIST_THRESHOLD = 20;

function register_visualisation(visualisation_id, visualisation) {
    VISUALISATION_REGISTRY[visualisation_id] = visualisation;
    console.log("Registered visualisation: " + visualisation_id);
}
function update_visualisation(visualisation_id) {
    try {
        VISUALISATION_REGISTRY[visualisation_id].update();
        console.log("Updated visualisation: " + visualisation_id);
    }
    catch(err) {
        console.error("Unable to update visualisation " + visualisation_id + ":" + err.message);
    }
}
function chart_statusbar_set(message) {
    $('#statusbar-chart-rendering').text(message);
    $('#statusbar-chart-rendering').show();
}
function chart_statusbar_clear() {
    $('#statusbar-chart-rendering').hide();
    $('#statusbar-chart-rendering').text('');
}

// Calculate delta of minimal and maximal value of time scale of given chart.
function calculate_chart_timescale_delta(chartobj) {
    scaledomain = chartobj.xAxis.scale().domain();
    datemin = new Date(scaledomain[0]);
    datemax = new Date(scaledomain[scaledomain.length-1]);
    return (datemax - datemin) / 1000;
}

// Convert given list of objects (LoOs) into list of lists (LoLs).
function loos_to_lols(header_row, data_rows, key_attr = 'key', val_attr = 'value') {
    return header_row.concat(
        data_rows.map(function(data) {
            return [
                data[key_attr],
                data[val_attr]
            ];
        })
    );
}

// Convert given list of objects (LoOs) into list of lists (LoLs) with given header keywords.
function loos_to_lols_kw(header_row, data_rows) {
    return [header_row.map(function(column) {
        return column.key;
    })].concat(
        data_rows.map(function(data) {
            result = [];
            header_row.forEach(function(column) {
                result.push(data[column.ident]);
            });
            return result;
        })
    );
}

// Convert given list of lists (LoLs) into CSV string.
function lols_to_csv(data, args = {}) {
	var result, ctr, columnDelimiter, lineDelimiter;

    if (data == null || !data.length) {
        return null;
    }

    columnDelimiter = args.columnDelimiter || ';';
    lineDelimiter = args.lineDelimiter || '\n';

    result = '';

    data.forEach(function(row) {
        ctr = 0;
        row.forEach(function(item) {
            if (ctr > 0) result += columnDelimiter;

            result += item;
            ctr++;
        });
        result += lineDelimiter;
    });

    return result;
}

// Alternative method for downloading JavaScript variable as CSV, resource:
// 		https://halistechnology.com/2015/05/28/use-javascript-to-export-your-data-as-csv/
// Currently rejected in favor of using this recipe:
// 		https://codepen.io/vidhill/pen/bNPEmX?editors=1010
// I am keeping it here for future consideration.
function download_as_CSV(args) {
    var data, filename, link;
    var csv = lols_to_csv(args.data);
    if (csv == null) return;

    filename = args.filename || 'export.csv';
    console.log('Downloading CSV: ' + filename);

    if (!csv.match(/^data:text\/csv/i)) {
        csv = 'data:text/csv;charset=utf-8,' + csv;
    }
    data = encodeURI(csv);

    link = document.createElement('a');
    link.setAttribute('href', data);
    link.setAttribute('download', filename);
    link.click();
}

// Render multi-timeline chart.
function render_chart_timeline_multi(chid, chart_data, params) {
	console.log('Rendering chart: ' + chid);

	nv.addGraph(function() {
        var chart = nv.models.multiBarChart()
            .reduceXTicks(true)   // If 'false', every single x-axis tick label will be rendered.
            .rotateLabels(0)      // Angle to rotate x-axis labels.
            .margin({bottom: 40}) // Make bottom margin big enough to fit the datetime labels.
            .showControls(false)  // Do not allow user to switch between 'Grouped' and 'Stacked' mode.
            .stacked(true)        // Use 'Stacked' mode by default.
            .showLegend(true)     // Show legend for datasets.
            .groupSpacing(0.1)    // Distance between each group of bars.
          ;

        // Custom tick formatter for datetime labels of X axis.
        // Must be defined here, because we are using closure
        // to ge to the chart object itself.
        var customTickFormat = d3.time.format.multi([
            ["%Y-%m-%d", function(d) { return calculate_chart_timescale_delta(chart) > (60*60*24); }],
            ["%H:%M:%S", function(d) { return d.getSeconds()!= 0; }],
            ["%H:%M",    function(d) { return true }]
        ]);

        // Customize the Y axis.
        chart
            .yAxis.tickFormat(d3.format(',d')) // Event counts are just integers.
            .axisLabel(params.ylabel || 'Count [#]')
        ;

        // Customize the X axis.
        chart
            .xAxis.tickFormat(function(d) {
                return customTickFormat(new Date(d))
            })
            .axisLabel(params.xlabel || 'Date')
        ;

        // Customize the tooltip.
        chart.tooltip.headerFormatter(function(d) {
            return d3.time.format.iso(new Date(d)); // Keep the date in tooltip header in full ISO format.
        });

        // Select the appropriate SVG element and bind datum to the chart.
        d3.select("#" + chid + " svg")
            .datum(chart_data)
            .transition().duration(350)
            .call(chart);

        nv.utils.windowResize(chart.update);

        register_visualisation(chid, chart);

        return chart;
    });
}

// Convert timeline chart raw data to representation appropriate for D3 bar chart.
function dstl_to_chart(dataset, data_series) {
    return data_series.map(function(serie) {
        return {
            ident: serie.ident,
            key: 'key' in serie ? serie.key : serie.ident,
            values: dataset.map(function(tl_data) {
                return {
                    x: tl_data._date,
                    y: tl_data[serie.ident] || 0
                };
            })
        };
    });
}

// Convert timeline chart raw data to representation appropriate for D3 scatter chart.
function dsts_to_chart(dataset, data_series) {
    return data_series.map(function(serie) {
        value_list = [];
        dataset.forEach(function(data_days, idx_day) {
            data_days.forEach(function(data_hours, idx_hour) {
                if (data_hours[serie.ident]) {
                    value_list.push({
                        x:    idx_hour,
                        y:    idx_day,
                        size: data_hours[serie.ident]
                    });
                }
            });
        });
        return {
            ident: serie.ident,
            key: 'key' in serie ? serie.key : serie.ident,
            values: value_list
        };
    });
}

// Convert timeline chart raw data to representation appropriate for D3 pie chart.
function dstl_to_pie(dataset, data_series) {
    return data_series.map(function(serie) {
        return {
            ident: serie.ident,
            key: 'key' in serie ? serie.key : serie.ident,
            value: d3.nest().rollup(function(rv) {
                return d3.sum(rv, function(g) { return g[serie.ident] });
            }).entries(dataset)
        };
    }).sort(function(a, b) {
        return b.value < a.value ? -1 : b.value > a.value ? 1 : b.value >= a.value ? 0 : NaN;
    });
}

// Prepare dataset for timeline visualisations from given data series list.
function get_dataset_timeline_list(raw_data, data_serie_list) {
    return raw_data.timeline.map(function(data) {
        result = {_date: data[0]};
        data_serie_list.forEach(function(data_serie) {
            result[data_serie.ident] = data_serie.ident in data[1] ? data[1][data_serie.ident] || 0 : 0;
        });
        return result;
    });
}

// Prepare dataset for timeline visualisations from given raw_data dictionary.
function get_dataset_timeline_dict(raw_data, data_serie_list, dict_key) {
    return raw_data.timeline.map(function(data) {
        result = {_date: data[0]};
        data_serie_list.forEach(function(data_serie) {
            if (dict_key in data[1] && data_serie.ident in data[1][dict_key]) {
                result[data_serie.ident] = data[1][dict_key][data_serie.ident];
            }
            else {
                result[data_serie.ident] = 0;
            }
        });
        return result;
    });
}

// Prepare dataset from given data series list.
function get_dataset_list(raw_data, data_serie_list, key_attr = 'key', val_attr = 'value') {
    return data_serie_list.map(function(data_serie) {
        result = {}
        result['ident'] = data_serie.ident;
        result[key_attr] = data_serie.key;
        result[val_attr] = raw_data[data_serie.ident];
        return result;
    });
}

// Prepare dataset for visualisations from given raw_data dictionary.
function get_dataset_dict(raw_data, key_attr = 'key', val_attr = 'value') {
    return d3.keys(raw_data).map(function(item) {
        result = {};
        result[key_attr] = item;
        result[val_attr] = raw_data[item];
        return result;
    }).sort(function(a,b) {
        return b[val_attr] < a[val_attr] ? -1 : b[val_attr] > a[val_attr] ? 1 : b[val_attr] >= a[val_attr] ? 0 : NaN;
    });
}

// Prepare dataset for visualisations from given raw_data dictionary.
function get_dataset_mdict(raw_data, key_attr = 'label', val_attr = 'value') {
    result = {'key': 'Data'};
    result['values'] = d3.keys(raw_data).map(function(item) {
        res = {};
        res[key_attr] = item;
        res[val_attr] = raw_data[item];
        return res;
    }).sort(function(a,b) {
        return b[val_attr] < a[val_attr] ? -1 : b[val_attr] > a[val_attr] ? 1 : b[val_attr] >= a[val_attr] ? 0 : NaN;
    });
    return [result];
}

// Prepare data series for visualisations from given raw_data dictionary.
function get_series_dict(raw_data, dict_key) {
    return d3.keys(raw_data[dict_key]).map(function(item) {
        result = {};
        result['ident'] = item;
        result['key']   = item;
        result['value'] = raw_data[dict_key][item];
        return result;
    }).sort(function(a,b) {
        return b.value < a.value ? -1 : b.value > a.value ? 1 : b.value >= a.value ? 0 : NaN;
    });
}

// Filter out the '__REST__' keyword from given dataset [{},{},{}].
function _filter_rest(full_data, key_attr = 'key') {
    result = [];
    rest   = 0;
    full_data.map(function(item) {
        if (item[key_attr] == KW_REST) {
            rest = item['value'];
        }
        else {
            result.push(item);
        }
    });
    return [result, rest];
}

// Make mask for creating toplist.
function _make_mask(mask_data) {
    mask = d3.map();
    mask_data.forEach(function(datum) {
        mask.set(datum['ident'], 1);
    });
    return mask;
}

// Mask given dataset [{},{},{}]. Works for get_dataset_timeline_dict().
function mask_toplist(data, mask_data) {
    mask = _make_mask(mask_data);
    result = []
    data.forEach(function(date_datum) {
        date_result = {};
        date_result[KW_REST] = date_datum[KW_REST] || 0;
        date_result[KW_DATE] = date_datum[KW_DATE];
        for (key in date_datum) {
            if ([KW_REST, KW_DATE].includes(key)) {
                continue;
            }
            if (!date_datum.hasOwnProperty(key)) {
                continue;
            }
            value = date_datum[key];
            if (!mask.has(key)) {
                date_result[KW_REST] += value;
            }
            else {
                date_result[key] = value;
            }
        }
        result.push(date_result);
    });
    return result;
}

// Make toplist from given dataset [{},{},{}]. Works for both get_dataset_dict()
// and get_series_dict().
function make_toplist(data, limit = 20, key_attr = 'key') {
    // Apply limitting only in case there is need to do so.
    if (limit && data.length > limit) {
        // Data may already contain the '__REST__' item, which contains sum of
        // the values not displayed directly. In case of limitting we must
        // pull this item out, add values of all stripped items to it and then
        // place it back.
        filter_result = _filter_rest(data, key_attr);
        result = filter_result[0];
        rest   = filter_result[1];
        // Now reduce the dataset to given limit of items - 1.
        result = result.reduce(function(total, currentItem, currentIndex, arr) {
            if (currentIndex < (limit - 1)) {
                total[0].push(currentItem);
            }
            else {
                total[1] += currentItem['value'];
            }
            return total;
        }, [[], rest]);
        // Put the '__REST__' item back to the dataset.
        if (result[1]) {
            res = {
                ident: KW_REST,
                value: result[1]
            };
            res[key_attr] = KW_REST;
            result[0].push(res);
        }
        data = result[0];
    }
    return data;
}

// Make toplist from given dataset [{},{},{}]. Works for both get_dataset_dict()
// and get_series_dict().
function make_mtoplist(data, limit = 20) {
    topl = make_toplist(data[0]['values'], limit, 'label');
    result = {'key': data[0].key, 'values': topl};
    return [result];
}

// Render pie chart.
function render_chart_pie(chid, chart_data, params = {}) {
    console.log('Rendering PIE chart: ' + chid);

    nv.addGraph(function() {
        var chart = nv.models.pieChart()
            .x(function(d) { return d.key })
            .y(function(d) { return d.value })
            .showLabels(true)
            .showLegend(true)
            .labelThreshold(.05)  //Configure the minimum slice size for labels to show up
            .labelType("key")     //Configure what type of data to show in the label. Can be "key", "value" or "percent"
            .donut(true)          //Turn on Donut mode. Makes pie chart look tasty!
            .donutRatio(0.2)      //Configure how big you want the donut hole size to be.
        ;

        // Parameters may override default value formatter.
        if (params.value_formatter) {
            chart.tooltip.valueFormatter(
                params.value_formatter
            );
        }

        // Select the appropriate SVG element and bind datum to the chart.
        d3.select("#" + chid + " svg")
            .datum(chart_data)
            .transition().duration(350)
            .call(chart);

        nv.utils.windowResize(chart.update);

        register_visualisation(chid, chart);

        return chart;
    });
}

// Render horizontal bar chart.
function render_chart_hbar(chid, chart_data, params = {}) {
    console.log('Rendering HORIZONTAL BAR chart: ' + chid);

    nv.addGraph(function() {
        var chart = nv.models.multiBarHorizontalChart()
            .x(function(d) { return d.label })
            .y(function(d) { return d.value })
            .showValues(true)
            .showControls(false)
            .showLegend(true)
            .legendPosition("bottom")
            .controlsPosition("bottom")
            .margin({left: 150})
            .stacked(false)
        ;

        // Parameters may override default value formatter.
        if (params.value_formatter) {
            chart.tooltip.valueFormatter(
                params.value_formatter
            );
        }

        // Select the appropriate SVG element and bind datum to the chart.
        d3.select("#" + chid + " svg")
            .datum(chart_data)
            .transition().duration(350)
            .call(chart);

        nv.utils.windowResize(chart.update);

        register_visualisation(chid, chart);

        return chart;
    });
}

// Custom color scale function for table rows. First column must inherit
// the color from parent, because datasets start on second column.
function table_row_color_scale() {
	var counter = 0;
	var palette = d3.scale.category20();
	return function() {
		counter += 1;
		if (counter == 1) {
			return 'inherit';
		}
		return palette(counter-1);
	};
}

// Custom color scale function for table columns.
function table_column_color_scale(column) {
    var column_number = column;
    var counter = 0;
    var palette = d3.scale.category20();
    return function(d, i) {
        if (column_number == i) {
            counter += 1;
            return palette(counter-1);
        }
        return 'inherit';
    };
}

// Custom color scale function.
function table_color_scale() {
    var palette = d3.scale.category20();
    return function(d, i) {
        return palette(i);
    };
}

function table_value_formatter(formatter) {
    var value_formatter = formatter;
    return function(value) {
        try {
            return value_formatter(value);
        }
        catch(err) {
            return value;
        }
    }
}

function byteFormatter() {
    var value_formatter = GLOBALIZER.numberFormatter({
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });
    var units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB'];
    var step_size = 1024;
    return function(size) {
        var unit = 'B';
        for (var i = 0; i < units.length-1; i++) {
            if (size > step_size) {
                if (unit.toUpperCase() == units[i]) {
                    size = size / step_size;
                    unit = units[i+1];
                }
            }
            else {
                break;
            }
        }
        return '' + value_formatter(size) + ' ' + unit;
    }
}

// Render multi-timeline table.
function render_table_timeline_multi(tid, table_columns, table_data, data_stats) {
	console.log('Rendering table: ' + tid);

    var value_formatter = table_value_formatter(GLOBALIZER.numberFormatter());
    var date_formatter = table_value_formatter(GLOBALIZER.dateFormatter());

	var table = d3.select('#' + tid).append('table')
	var thead = table.append('thead')
	var	tbody = table.append('tbody');
    var tfoot = table.append('tfoot');

	table.attr('class', 'table table-bordered table-striped table-condensed table-dataset table-dataset-timeline')

    // Precalculate the sums of all values in each table row. These will be displayed
    // in last table column.
    table_data.map(function(d) {
        d['_sum'] = d3.sum(
            table_columns.slice(1, -1).map(function (column) {
                return d[column.ident];
            })
        );
    });

	// Append the table header row.
	thead.append('tr')
		.selectAll('th')
		.data(table_columns).enter()
		.append('th')
		.style('background-color', table_row_color_scale())
		.text(function (column) { return column.key; });

	// Create a table body row for each object in the data.
	var brows = tbody.selectAll('tr')
		.data(table_data)
		.enter()
		.append('tr');

	// Create a cell in each table body row for each requested column.
	var bcells = brows.selectAll('td')
		.data(function (row) {
		    return table_columns.map(function (column) {
		        return {
                    column: column.ident,
                    value: row[column.ident]
                };
		    });
		})
		.enter()
		.append('td')
		.text(function (d, i) {
            // First column contains the datetime.
            if (i == 0) {
                return date_formatter(new Date(d.value));
            }
            // Other columns contain the numerical values.
            else {
                return value_formatter(d.value);
            }
        });

    // Map of aggregation functions for table footer statistical summaries.
    funcmap = {
        'cnt': function(a,b) { return a.length },
        'min': d3.min,
        'max': d3.max,
        'sum': d3.sum,
        'avg': d3.mean,
        'med': d3.median
    }

    // Create a table footer row for each requested statistical datum.
    var frows = tfoot.selectAll('tr')
        .data(data_stats)
        .enter()
        .append('tr');

    // Create a cell in each table footer row for each requested column except
    // the first one (contains date).
    var fcells = frows.selectAll('td')
        .data(function (row) {
            return [{value: row.key}].concat(
                table_columns.slice(1).map(function (column) {
                    return {
                        column: column.ident,
                        value: d3.nest().rollup(function(rv) {
                            return funcmap[row.ident](rv, function(g) { return g[column.ident] });
                        }).entries(table_data)
                    };
                })
            );
        })
        .enter()
        .append('td')
        .html(function (d, i) {
            // First column contains the HTML label for the statistical operation.
            if (i == 0) {
                return d.value;
            }
            // Other columns contain the values.
            else {
                return '<span>' + value_formatter(d.value) + '</span>';
            }
        });

	return table;
}

// Render context search action dropdown menu.
function render_action_dropdown(actions, args, kwargs) {
    root_elem = document.createElement('div');

    div_slct = d3.select(root_elem)
        .style('display', 'inline-block');

    div_dropdown = div_slct.append('div')
        .attr('class', 'btn-group');

    div_dropdown.append('button')
        .attr('class', 'btn btn-default btn-xs dropdown-toggle')
        .attr('type', 'button')
        .attr('data-toggle', 'dropdown')
        .attr('aria-haspopup', 'true')
        .attr('aria-expanded', 'false')
        .append('span')
            .attr('class', 'caret');

    ul_elem = div_dropdown.append('ul')
        .attr('class', 'dropdown-menu dropdown-menu-right')

    actions.forEach(function(action) {
        try {
            url = Flask.url_for(action.endpoint, action.params(args, kwargs));
            ul_elem.append('li').append('a')
                .attr('href', url)
                .attr('target', '_blank')
                .html(action.icon + action.title.replace('{name}', args));
        }
        catch(err) {
            console.error(err);
        }
    });

    return root_elem;
}

// Render table for dict-based dataset.
function render_table_dict(tid, table_columns, table_data, data_stats, action_list = null, params = {}) {
    console.log('Rendering table: ' + tid);

    var number_formatter = table_value_formatter(
        GLOBALIZER.numberFormatter()
    );
    var value_formatter = number_formatter;

    // Parameters may override default numeric value formatter.
    if (params.value_formatter) {
        value_formatter = table_value_formatter(params.value_formatter);
    }
    var percent_formatter = table_value_formatter(
        GLOBALIZER.numberFormatter({
            style: "percent",
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        })
    );

    var table = d3.select('#' + tid).append('table')
    var thead = table.append('thead')
    var tbody = table.append('tbody');
    var tfoot = table.append('tfoot');

    table.attr('class', 'table table-bordered table-striped table-condensed table-dataset table-dataset-pie')

    // Calculate the grand total.
    total = d3.nest().rollup(function(x) {
        return d3.sum(x, function(y) { return y.value; });
    }).entries(table_data)

    // Precalculate the percentages of all values in each table row. These will be displayed
    // in last table column.
    table_data.forEach(function(d) {
        d.share = d.value/total;
    });

    // Append the table header row.
    thead.append('tr')
        .selectAll('th')
        .data(table_columns).enter()
        .append('th')
        .text(function (column) { return column.label; });

    // Create a table body row for each object in the data.
    var brows = tbody.selectAll('tr')
        .data(table_data)
        .enter()
        .append('tr');

    // Create a cell in each table body row for each requested column.
    var bcells = brows.selectAll('td')
        .data(function (row) {
            return table_columns.map(function (column) {
                return {
                    column: column.ident,
                    value: row[column.ident]
                };
            });
        })
        .enter()
        .append('td');
        //.style('background-color', table_column_color_scale(0));

    bcells.append(function (d, i) {
            element = document.createElement('span');

            // First column contains the name.
            if (i == 0) {
                element.appendChild(
                    document.createTextNode(
                        d.value
                    )
                );
                return element;
            }
            // Second column contains the value.
            if (i == 1) {
                element.appendChild(
                    document.createTextNode(
                        value_formatter(d.value)
                    )
                );
                return element;
            }
            // Last column contains the percentage.
            element.appendChild(
                document.createTextNode(
                    percent_formatter(d.value)
                )
            );
            return element;
        });

    // Insert small circle icon with correct color for given dataset instead of
    // using background color of the whole table cell.
    if (!params.hide_table_colors) {
        brows.select('td')
            .insert('i')
            .style('color', table_color_scale())
            .attr('class', 'fas fa-fw fa-circle pull-left');
    }

    if (action_list) {
        brows.select('td')
            .filter(function(d, i) {
                return !(String(d.key).toLowerCase() in {'__unknown__': true, '__rest__': true});
            })
            .append(function (d, i) {
                return render_action_dropdown(action_list, d.key, params.kwargs);
            });
    }

    // Map of aggregation functions for table footer statistical summaries.
    funcmap = {
        'cnt': function(a,b) { return a.length },
        'min': d3.min,
        'max': d3.max,
        'sum': d3.sum,
        'avg': d3.mean,
        'med': d3.median
    }

    if (params.with_table_stats) {
        // Create a table footer row for each requested statistical datum.
        var frows = tfoot.selectAll('tr')
            .data(data_stats)
            .enter()
            .append('tr');

        // Create a cell in each table footer row for each requested column except
        // the first one (contains name).
        var fcells = frows.selectAll('td')
            .data(function (row) {
                return [{value: row.key}].concat(
                    table_columns.slice(1).map(function (column) {
                        return {
                            column: column.ident,
                            func: row.ident,
                            value: d3.nest().rollup(function(rv) {
                                return funcmap[row.ident](rv, function(g) { return g[column.ident] });
                            }).entries(table_data)
                        };
                    })
                );
            })
            .enter()
            .append('td')
            .html(function (d, i) {
                // First column contains the HTML label for the statistical operation.
                if (i == 0) {
                    return d.value;
                }
                // Second column contains the value, but always use numeric formatter
                // for 'cnt' aggregation.
                if (i == 1 && d.func == 'cnt') {
                    return '<span>' + number_formatter(d.value) + '</span>';
                }
                // Second column contains the value.
                if (i == 1) {
                    return '<span>' + value_formatter(d.value) + '</span>';
                }
                // Last column contains the percentage, but does not make sense for 'cnt' aggregation.
                if (d.func == 'cnt') {
                    return '<i class="fas fa-fw fa-times"></i>';
                }
                // Last column contains the percentage.
                return '<span>' + percent_formatter(d.value) + '</span>';
            });
    }

    return table;
}


// Render table for dict-based dataset.
function render_table_mdict(tid, table_columns, table_data, data_stats, total = null, action_list = null, params = {}) {
    console.log('Rendering table: ' + tid);

    var number_formatter = table_value_formatter(
        GLOBALIZER.numberFormatter()
    );
    var value_formatter = number_formatter;

    // Parameters may override default numeric value formatter.
    if (params.value_formatter) {
        value_formatter = table_value_formatter(params.value_formatter);
    }
    var percent_formatter = table_value_formatter(
        GLOBALIZER.numberFormatter({
            style: "percent",
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        })
    );

    var table = d3.select('#' + tid).append('table')
    var thead = table.append('thead')
    var tbody = table.append('tbody');
    var tfoot = table.append('tfoot');

    table.attr('class', 'table table-bordered table-striped table-condensed table-dataset table-dataset-pie')

    // Calculate the grand total.
    if (total === null) {
        total = d3.nest().rollup(function(x) {
            return d3.sum(x, function(y) { return y.value; });
        }).entries(table_data);
    }

    // Precalculate the percentages of all values in each table row. These will be displayed
    // in last table column.
    table_data.forEach(function(d) {
        d.share = d.value/total;
    });

    // Append the table header row.
    thead.append('tr')
        .selectAll('th')
        .data(table_columns).enter()
        .append('th')
        .text(function (column) { return column.label; });

    // Create a table body row for each object in the data.
    var brows = tbody.selectAll('tr')
        .data(table_data)
        .enter()
        .append('tr');

    // Create a cell in each table body row for each requested column.
    var bcells = brows.selectAll('td')
        .data(function (row) {
            return table_columns.map(function (column) {
                return {
                    column: column.ident,
                    value: row[column.ident]
                };
            });
        })
        .enter()
        .append('td');
        //.style('background-color', table_column_color_scale(0));

    bcells.append(function (d, i) {
            element = document.createElement('span');

            // First column contains the name.
            if (i == 0) {
                element.appendChild(
                    document.createTextNode(
                        d.value
                    )
                );
                return element;
            }
            // Second column contains the value.
            if (i == 1) {
                element.appendChild(
                    document.createTextNode(
                        value_formatter(d.value)
                    )
                );
                return element;
            }
            // Last column contains the percentage.
            element.appendChild(
                document.createTextNode(
                    percent_formatter(d.value)
                )
            );
            return element;
        });

    if (action_list) {
        brows.select('td')
            .filter(function(d, i) {
                return !(String(d.label).toLowerCase() in {'__unknown__': true, '__rest__': true});
            })
            .append(function (d, i) {
                return render_action_dropdown(action_list, d.label, params.kwargs);
            });
    }

    return table;
}
