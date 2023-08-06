/* global d3 */

/* eslint-disable no-unused-vars */

function renderTransmittersChart({ el, transmitters, satellites_list }) {
    d3.formatDefaultLocale({
        decimal: '.',
        thousands: '',
        grouping: [3],
    });
    const data = processData(transmitters, satellites_list);
    const container = d3.select(el).classed('transmitters-chart', true);
    const tooltip = renderTooltip(container);
    renderLegend(container, data.types);
    const { zoom } = renderChart(container, data, tooltip);

    function processData(transmitters, satellites_list) {
        let satellites = {};

        satellites_list.forEach(function(item){
            satellites[item.norad_cat_id] = item;
        });

        let sorted = transmitters
            .map((d) => {
                d['satellite'] = satellites[d.norad_cat_id];
                const width = (d.baud || 9600) / 1e6;
                const x0 = d.downlink_low / 1e6 - width / 2;
                const x1 = d.downlink_low / 1e6 + width / 2;
                return {
                    x0,
                    x1,
                    width,
                    type: d.type.toLowerCase(),
                    data: d,
                };
            })
            .sort((a, b) => d3.ascending(a.x0, b.x0));
        const xMin = d3.min(sorted, (d) => d.x0);
        const xMax = d3.max(sorted, (d) => d.x1);
        const rows = [];
        const types = ['Transmitter', 'Transceiver', 'Transponder'];
        types.forEach((type) => {
            let typeSorted = sorted.filter((d) => d.data.type === type);
            while (typeSorted.length > 0) {
                const picked = [];
                const left = [];
                let x = xMin - 1;
                typeSorted.forEach((d, i) => {
                    if (d.x0 > x) {
                        picked.push(i);
                        x = d.x1;
                    } else {
                        left.push(i);
                    }
                });
                const row = picked.map((i) => typeSorted[i]);
                row.type = type.toLowerCase();
                rows.push(row);
                typeSorted = left.map((i) => typeSorted[i]);
            }
        });
        return {
            rows,
            types,
            xMin,
            xMax,
        };
    }

    function renderTooltip(container) {
        const tooltip = container.append('div').attr('class', 'chart-tooltip');
        let tooltipBox, 
            containerBox;

        function show(content, colorClass) {
            tooltip.attr('class', `chart-tooltip ${colorClass}`).html(content);
            tooltipBox = tooltip.node().getBoundingClientRect();
            containerBox = container.node().getBoundingClientRect();
            tooltip.classed('show', true);
        }

        function hide() {
            tooltip.classed('show', false);
        }

        function move(event) {
            let [x, y] = d3.pointer(event, container.node());
            x = x - tooltipBox.width / 2;
            if (x < 0) {x = 0;}
            if (x + tooltipBox.width > containerBox.width)
            {x = containerBox.width - tooltipBox.width;}
            y = y - tooltipBox.height - 8;
            if (y < 0) {
                y = y + tooltipBox.height + 8 * 2;
            }
            tooltip.style('transform', `translate(${x}px,${y}px)`);
        }

        return {
            show,
            hide,
            move,
        };
    }

    function renderLegend(container, items) {
        const legend = container.append('div').attr('class', 'chart-legend');
        const legendItem = legend
            .selectAll('.legend-item')
            .data(items)
            .join('div')
            .attr('class', 'legend-item');
        legendItem
            .append('div')
            .attr('class', (d) => `legend-swatch color-${d.toLowerCase()}`);
        legendItem
            .append('div')
            .attr('class', 'legend-value')
            .text((d) => d);
    }

    function renderChart(container, data, tooltip) {
        const dimension = {
            rowHeight: 20,
            rowPadding: 4,
            margin: {
                top: 40,
                right: 20,
                bottom: 20,
                left: 20,
            },
            totalWidth: null,
            get width() {
                return this.totalWidth - this.margin.left - this.margin.right;
            },
            get height() {
                return this.rowHeight * data.rows.length;
            },
            get totalHeight() {
                return this.height + this.margin.top + this.margin.bottom;
            },
            minBarWidth: 2,
        };

        const zoom = d3.zoom().on('zoom', zoomed);

        const x = d3.scaleLinear().domain([data.xMin, data.xMax]);
        let xz = x.copy();

        const y = d3
            .scaleBand()
            .domain(d3.range(data.rows.length))
            .range([0, dimension.height])
            .paddingInner(dimension.rowPadding / dimension.rowHeight)
            .paddingOuter(dimension.rowPadding / dimension.rowHeight / 2);

        const xAxisTop = (g, x) =>
            g.call(
                d3
                    .axisTop(x)
                    .ticks(dimension.width / 80)
                    .tickPadding(6)
                    .tickSizeInner(-dimension.height)
                    .tickSizeOuter(0)
            );
        const xAxisBottom = (g, x) =>
            g.call(
                d3
                    .axisBottom(x)
                    .ticks(dimension.width / 80)
                    .tickPadding(6)
                    .tickSize(0)
            );

        const svg = container
            .append('svg')
            .attr('class', 'chart-svg')
            .call(zoom)
            .on('click', () => {});
        const clipRect = svg
            .append('defs')
            .append('clipPath')
            .attr('id', 'transmitters-chart-bars-clip')
            .append('rect');
        const g = svg
            .append('g')
            .attr(
                'transform',
                `translate(${dimension.margin.left},${dimension.margin.top})`
            );
        const axisUnit = g
            .append('text')
            .attr('class', 'axis axis__unit')
            .attr('y', -20)
            .attr('text-anchor', 'end')
            .text('Frequency (MHz)');
        const gAxisTop = g.append('g').attr('class', 'axis axis--top');
        const gAxisBottom = g
            .append('g')
            .attr('class', 'axis axis--bottom')
            .attr('transform', `translate(0,${dimension.height})`);
        const gRows = g
            .append('g')
            .attr('class', 'bar-rows')
            .attr('clip-path', 'url(#transmitters-chart-bars-clip)');
        const gRow = gRows
            .selectAll('.bar-row')
            .data(data.rows)
            .join('g')
            .attr('class', 'bar-row')
            .attr('transform', (_, i) => `translate(0,${y(i)})`);
        const bar = gRow
            .selectAll('.bar')
            .data((d) => d)
            .join('rect')
            .attr('class', (d) => `bar color-${d.type}`)
            .attr('height', y.bandwidth())
            .on('mouseenter', entered)
            .on('mouseleave', left)
            .on('mousemove', moved)
            .on('click', clicked);

        resize();
        window.addEventListener('resize', resize);

        function entered(_, d) {
            d3.select(this).raise();
            tooltip.show(tooltipContent(d.data), `color-${d.type}`);
        }

        function left() {
            tooltip.hide();
        }

        function moved(event) {
            tooltip.move(event);
        }

        function clicked(_, d) {
            window.open('/satellite/' + d.data.norad_cat_id + '#transmitters', 'transmitter');
        }

        function zoomed({ transform }) {
            const range = x.range().map(transform.invertX, transform);
            const domain = range.map(x.invert, x);
            xz.domain(domain);
            render();
        }

        function resize() {
            dimension.totalWidth = container.node().clientWidth;
            svg.attr('viewBox', [0, 0, dimension.totalWidth, dimension.totalHeight]);
            clipRect.attr('width', dimension.width).attr('height', dimension.height);
            axisUnit.attr('x', dimension.width);
            x.range([0, dimension.width - dimension.minBarWidth]);
            xz.range([0, dimension.width - dimension.minBarWidth]);
            render();
        }

        function render() {
            gAxisTop.call(xAxisTop, xz);
            gAxisBottom.call(xAxisBottom, xz);
            bar
                .attr('x', (d) => xz(d.x0))
                .attr('width', (d) =>
                    Math.max(dimension.minBarWidth, xz(d.x1) - xz(d.x0))
                );
        }

        function tooltipContent(d) {
            return `
        <table>
          <tbody>
            <tr>
              <td>Satellite</td>
              <td>${d.satellite.name}</td>
            </tr>
            <tr>
              <td>NORAD ID</td>
              <td>${d.norad_cat_id}</td>
            </tr>
            <tr>
              <td>Type</td>
              <td>${d.type}</td>
            </tr>
            <tr>
              <td>Description</td>
              <td>${d.description}</td>
            </tr>
            <tr>
              <td>Downlink</td>
              <td>${d3.format(',')(d.downlink_low / 1e6) + 'MHz'}</td>
            </tr>
            <tr>
              <td>Mode</td>
              <td>${d.mode}</td>
            </tr>
            <tr>
              <td>Baud</td>
              <td>${d.baud ? d3.format(',')(d.baud) : ''}</td>
            </tr>
            <tr>
              <td>Service</td>
              <td>${d.service}</td>
            </tr>
            <tr>
              <td>Status</td>
              <td>${d.status}</td>
            </tr>
          </tbody>
        </table>
      `;
        }

        return {
            zoom: (minFreq, maxFreq) => {
                svg
                    .transition()
                    .call(
                        zoom.transform,
                        d3.zoomIdentity
                            .scale(dimension.width / (x(maxFreq) - x(minFreq)))
                            .translate(-x(minFreq), 0)
                    );
            },
        };
    }

    return {
        zoom,
    };
}
