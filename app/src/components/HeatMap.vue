<template>
    <v-app v-bind:id="'heatmap-'+ id">
    </v-app>
</template>
<script>
import * as d3 from 'd3';
import * as topojson from "topojson-client";
import us_json from '../assets/us.json';


// This function is FROM https://observablehq.com/@d3/color-legend
// We were unable to import it properly :'(
function legend({
  color,
  title,
  tickSize = 6,
  width = 320, 
  height = 44 + tickSize,
  marginTop = 18,
  marginRight = 0,
  marginBottom = 16 + tickSize,
  marginLeft = 0,
  ticks = width / 64,
  tickFormat,
  tickValues
} = {}) {

  const svg = d3.create("svg")
      .attr("width", width)
      .attr("height", height)
      .attr("viewBox", [0, 0, width, height])
      .attr("xmlns","http://www.w3.org/2000/svg")
      .style("overflow", "visible")
      .style("display", "block");

  let tickAdjust = g => g.selectAll(".tick line").attr("y1", marginTop + marginBottom - height);
  let x;

  // Continuous
  if (color.interpolate) {
    const n = Math.min(color.domain().length, color.range().length);

    x = color.copy().rangeRound(d3.quantize(d3.interpolate(marginLeft, width - marginRight), n));

    svg.append("image")
        .attr("x", marginLeft)
        .attr("y", marginTop)
        .attr("width", width - marginLeft - marginRight)
        .attr("height", height - marginTop - marginBottom)
        .attr("preserveAspectRatio", "none")
        .attr("xlink:href", "data:image/png;base64");
        //.attr("xlink:href", ramp(color.copy().domain(d3.quantize(d3.interpolate(0, 1), n))).toDataURL());
  }

  // Sequential
  else if (color.interpolator) {
    x = Object.assign(color.copy()
        .interpolator(d3.interpolateRound(marginLeft, width - marginRight)),
        {range() { return [marginLeft, width - marginRight]; }});

    svg.append("image")
        .attr("x", marginLeft)
        .attr("y", marginTop)
        .attr("width", width - marginLeft - marginRight)
        .attr("height", height - marginTop - marginBottom)
        .attr("preserveAspectRatio", "none")
        .attr("xlink:href", "data:image/png;base64");
        //.attr("xlink:href", ramp(color.interpolator()).toDataURL());

    // scaleSequentialQuantile doesn’t implement ticks or tickFormat.
    if (!x.ticks) {
      if (tickValues === undefined) {
        const n = Math.round(ticks + 1);
        tickValues = d3.range(n).map(i => d3.quantile(color.domain(), i / (n - 1)));
      }
      if (typeof tickFormat !== "function") {
        tickFormat = d3.format(tickFormat === undefined ? ",f" : tickFormat);
      }
    }
  }

  // Threshold
  else if (color.invertExtent) {
    const thresholds
        = color.thresholds ? color.thresholds() // scaleQuantize
        : color.quantiles ? color.quantiles() // scaleQuantile
        : color.domain(); // scaleThreshold

    const thresholdFormat
        = tickFormat === undefined ? d => d
        : typeof tickFormat === "string" ? d3.format(tickFormat)
        : tickFormat;

    x = d3.scaleLinear()
        .domain([-1, color.range().length - 1])
        .rangeRound([marginLeft, width - marginRight]);

    svg.append("g")
      .selectAll("rect")
      .data(color.range())
      .join("rect")
        .attr("x", (d, i) => x(i - 1))
        .attr("y", marginTop)
        .attr("width", (d, i) => x(i) - x(i - 1))
        .attr("height", height - marginTop - marginBottom)
        .attr("fill", d => d);

    tickValues = d3.range(thresholds.length);
    tickFormat = i => thresholdFormat(thresholds[i], i);
  }

  // Ordinal
  else {
    x = d3.scaleBand()
        .domain(color.domain())
        .rangeRound([marginLeft, width - marginRight]);

    svg.append("g")
      .selectAll("rect")
      .data(color.domain())
      .join("rect")
        .attr("x", x)
        .attr("y", marginTop)
        .attr("width", Math.max(0, x.bandwidth() - 1))
        .attr("height", height - marginTop - marginBottom)
        .attr("fill", color);

    tickAdjust = () => {};
  }

  svg.append("g")
      .attr("transform", `translate(0,${height - marginBottom})`)
      .call(d3.axisBottom(x)
        .ticks(ticks, typeof tickFormat === "string" ? tickFormat : undefined)
        .tickFormat(typeof tickFormat === "function" ? tickFormat : undefined)
        .tickSize(tickSize)
        .tickValues(tickValues))
      .call(tickAdjust)
      .call(g => g.select(".domain").remove())
      .call(g => g.append("text")
        .attr("x", marginLeft)
        .attr("y", marginTop + marginBottom - height - 6)
        .attr("fill", "currentColor")
        .attr("text-anchor", "start")
        .attr("font-weight", "bold")
        .text(title));

  return svg.node();
}


export default {
    name: "HeatMap",
    props: ['spendingJson', 'id'],
    data() {
        return {
            spendings: 
            {"Vermont":2.1,"North Dakota":2.4,"Iowa":2.5,"New Hampshire":2.5,"Hawaii":2.8,"Utah":2.8,"Colorado":2.9,"Idaho":2.9,"Massachusetts":2.9,"South Dakota":2.9,"Virginia":2.9,"Maine":3,"Wisconsin":3,"Nebraska":3.1,"Oklahoma":3.2,"Alabama":3.3,"Delaware":3.3,"Florida":3.3,"Kansas":3.3,"Missouri":3.3,"New Jersey":3.3,"Arkansas":3.4,"Indiana":3.4,"Minnesota":3.4,"Montana":3.4,"South Carolina":3.4,"Texas":3.4,"Rhode Island":3.5,"Tennessee":3.5,"Connecticut":3.6,"Georgia":3.6,"Wyoming":3.6,"Maryland":3.8,"Pennsylvania":3.9,"New York":4,"Ohio":4,"Oregon":4,"California":4.1,"Nevada":4.1,"Illinois":4.2,"North Carolina":4.2,"Kentucky":4.3,"Louisiana":4.3,"Michigan":4.3,"Washington":4.6,"West Virginia":4.7,"Arizona":4.9,"New Mexico":4.9,"Mississippi":5.1,"District of Columbia":5.6,"Alaska":6.3}
            ,
            us : us_json
        };
    },
    mounted() {
        this.getSpendings();
    },
    computed: {
        user() {
            return this.$store.getters.user;
        }
    },
    watch: {
        spendingJson() {
            this.updateGraph();
        }
    },
    methods: {
        generateArc() {
            let svg = d3
                .select("#heatmap-"+this.id)
                .append("svg")
                .attr("viewBox", [0, 0, 975, 610])
                .attr("width", 975)
                .attr("xmlns","http://www.w3.org/2000/svg");

            const color = d3.scaleSequential([0, 10], d3.interpolateReds);
            let g = svg.append("g");
            const path = d3.geoPath();
            const format = d => `${d}%`;
            g.attr("transform", "translate(10, 20)")
                .append(() => legend({color, title: "Budget Allocated", width: 0, marginLeft : 500}));

            g.selectAll("path")
                .data(topojson.feature(this.us, this.us.objects.states).features)
                .join("path")
                .attr("fill", d => color(this.spendings[d.properties.name]))
                .attr("d", path)
                .append("title")
                .text(d => `${d.properties.name}
                ${format(this.spendings[d.properties.name])}`);
            
            svg.append("path")
                .datum(topojson.mesh(this.us, this.us.objects.states, (a, b) => a !== b))
                .attr("fill", "none")
                .attr("stroke", "white")
                .attr("stroke-linejoin", "round");

        },
        getSpendings () {
            this.spendings = this.spendingJson;
            this.generateArc();
        },
        updateGraph() {
            d3.select('#heatmap-'+this.id).select("svg")
                .remove();
            this.getSpendings();
        }
    }
}
</script>
