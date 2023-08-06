window.NV_CHART_COLORS = window.NV_CHART_COLORS || [
  // Violet to orange
  '#003f5c', '#ffa600', '#2f4b7c', '#ff7c43', '#665191', '#f95d6a', '#a05195', '#d45087',
  // Violet to light green
  '#29005c', '#003292', '#0058bc', '#007dd4', '#00a0d6', '#00c2c4', '#00e2a3', '#00ff79',
];
window.NV_CHART_TYPE_FORMATTERS = window.NV_CHART_TYPE_FORMATTERS || {};
window.NV_CHART_TYPE_HANDLERS = window.NV_CHART_TYPE_HANDLERS || {};
window.NV_CHART_DEFAULT_TYPE = window.NV_CHART_DEFAULT_TYPE || 'bar';

window.createChart = (function () {
  // AXIS FORMATTERS:
  var setAxisFormatters = (function () {
    // Date formatter
    var createDateFormatter = (function () {
      var nullDay = new Date(0);
      var dateFormatComparatorsMap = [
        ['milliseconds', 'getUTCMilliseconds'],
        ['seconds', 'getUTCSeconds'],
        ['minutes', 'getUTCMinutes'],
        ['hours', 'getUTCHours'],
        ['days', 'getUTCDate'],
        ['months', 'getUTCMonth'],
        ['years', 'getUTCFullYear'],
      ]
      var N = 'numeric'
      var S = 'short'
      var locale = window.document.documentElement.lang
      var dateFormattersMap = {
        milliseconds: new Intl.DateTimeFormat(locale, { month: N, day:N, hour: N, minute: N, second: N, milliseconds: N, hour12: false }),
        seconds: new Intl.DateTimeFormat(locale, { month: N, day: N, hour: N, minute: N, second: N, hour12: false }),
        minutes: new Intl.DateTimeFormat(locale, { month: N, day: N, hour: N, minute: N, hour12: false }),
        hours: new Intl.DateTimeFormat(locale, { month: N, day: N, hour: N, hour12: false }),
        days: new Intl.DateTimeFormat(locale, { year: N, month: S, day: N }),
        months: new Intl.DateTimeFormat(locale, { year: N, month: S }),
        years: new Intl.DateTimeFormat(locale, { year: N }),
      }
      function getLowestDateFormat(dates) {
        var len = dateFormatComparatorsMap.length - 1

        if (dates.length === 0) {
          return dateFormatComparatorsMap[len - 1][0]
        }

        var start = dates.length == 1 ? nullDay : dates[0];
        const last = dateFormatComparatorsMap.findIndex(f => dates.some(
          date => date[f[1]]() !== start[f[1]]()
        )) || len;

        return dateFormatComparatorsMap[last === -1 ? len : last][0];
      }
      function createDateFormatter(field, data, config) {
        var dates = data.map(x => x[field])
        var lowestFormat = getLowestDateFormat(dates)

        return d => dateFormattersMap[lowestFormat].format(d);
      }

      return createDateFormatter;
    })()

    window.NV_CHART_TYPE_FORMATTERS.date = window.NV_CHART_TYPE_FORMATTERS.date || createDateFormatter;

    function setAxisFormatters(chart, data, config) {
      var formatterMaps = {};
      var toMap = (fields, name) => fields.forEach(field => {
        formatterMaps[field] = name
      })

      toMap(config.dates || [], 'date')

      var axis = [[config.x, chart.xAxis], [config.y, chart.yAxis]]

      for (let i = 0; i < axis.length; i++) {
        var [field, a] = axis[i];
        if (a && formatterMaps[field] && window.NV_CHART_TYPE_FORMATTERS[formatterMaps[field]]) {
          a.tickFormat(window.NV_CHART_TYPE_FORMATTERS[formatterMaps[field]](field, data, config))
        }
      }

      return chart
    }

    return setAxisFormatters;
  })();

  var findLegend = (field, config) => config.legend.find(x => x.key === field)
  var createXGetter = config => d => d[config.x]
  var createYGetter = config => d => d[config.y]

  function setAxisLabels(chart, data, config) {
    chart.xAxis && chart.xAxis.axisLabel(findLegend(config.x, config).title)
    chart.yAxis && chart.yAxis.axisLabel(findLegend(config.y, config).title)

    return chart;
  }

  function prepareChart(chart, data, config) {
    setAxisFormatters(chart, data, config)
    setAxisLabels(chart, data, config)
    return chart
  }

  function mapDates(data, config) {
    var dateFields = config.dates || [];

    if (dateFields.length) {
      data.forEach(item => dateFields.forEach(field => {
        item[field] = new Date(item[field]);
      }))
    }

    return data;
  }

  function mapColors(data, colors) {
    var colors_length = colors.length;

    if (colors_length > 0) {
      data.forEach((item, i) => {
        item.color = colors[i % colors_length];
      });
    }

    return data
  }

  function collectMultiBarData(data, config) {
    var config = config || {};
    var x = config.x;
    var y = config.y;
    var legend = config.legend;
    var chartData = [];

    if (legend.length == 3) {
      var grouper = config.legend.find(v => v.key != x && v.key != y);
      chartData = Object.values(data.reduce((acc, item) => {
        acc[item[grouper.key]] = acc[item[grouper.key]] || {
          key: item[grouper.key], values: [],
        };
        acc[item[grouper.key]].values.push(item);

        return acc;
      }, {}));
    } else {
      chartData.push({
        values: data
      });
    }

    return mapColors(chartData, window.NV_CHART_COLORS)
  }

  function collectBarData(data, config) {
    return mapColors(data, window.NV_CHART_COLORS)
  }

  function bar(data, config) {
    return {
      data: collectMultiBarData(data, config),
      chart: prepareChart(nv.models.multiBarChart(), data, config)
        .x(createXGetter(config)).y(createYGetter(config))
        .reduceXTicks(true)
        .showControls(true)
        .showLegend(true)
        .showYAxis(true)
        .showXAxis(true)
    }
  }
  window.NV_CHART_TYPE_HANDLERS.bar = window.NV_CHART_TYPE_HANDLERS.bar || bar

  function pie(data, config) {
    return {
      data: collectBarData(data, config),
      chart: prepareChart(nv.models.pieChart(), data, config)
        .x(createXGetter(config)).y(createYGetter(config))
        .showLabels(true)
        .labelType(config.labelType || 'key')
        .donut(true)
        .donutRatio(0.35)
    }
  }
  window.NV_CHART_TYPE_HANDLERS.pie = window.NV_CHART_TYPE_HANDLERS.pie || pie

  function line(data, config) {
    return {
      data: collectMultiBarData(data, config),
      chart: prepareChart(nv.models.lineChart(), data, config)
        .x(createXGetter(config)).y(createYGetter(config))
        .useInteractiveGuideline(true)
        .showLegend(true)
        .showYAxis(true)
        .showXAxis(true)
    }
  }
  window.NV_CHART_TYPE_HANDLERS.line = window.NV_CHART_TYPE_HANDLERS.line || line

  return function createChart(chart_id, data, config) {
    var type = config.type || window.NV_CHART_DEFAULT_TYPE;
    var chart = window.NV_CHART_TYPE_HANDLERS[type](mapDates(data, config), config)

    nv.addGraph(function() {
      d3.select('#chart-' + chart_id + ' svg')
        .datum(chart.data)
        .call(chart.chart)
      nv.utils.windowResize(chart.update)

      return chart
    });
  }
})();

