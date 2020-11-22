<template>
    <v-app>
        <v-container>
        <v-row>
            <v-col cols="4" class="d-flex justify-center align-center">
            </v-col>
            <v-col id="arc" />
        </v-row>
        </v-container>
    </v-app>
</template>
<script>
import * as d3 from 'd3';
export default {
    name: "RegionChart",
    data() {
        return {
            spendings: [
                {region: "r1", value: 1000},
                {region: "r2", value: 2300},
                {region: "r3", value: 1400},
                {region: "r4", value: 3000},
                {region: "r5", value: 2000}
            ]
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
    methods: {
        generateArc() {
            const w = 500;
            const h = 500;

            const svg = d3
                .select("#arc")
                .append("svg")
                .attr("width", w)
                .attr("height", h);

            const sortedspendings = this.spendings.sort((a, b) => (a.value > b.value ? 1 : -1));
            const color = d3.scaleOrdinal(d3.schemeDark2);

            const max_spendings = d3.max(sortedspendings, o => o.value);

            const angleScale = d3
                .scaleLinear()
                .domain([0, max_spendings])
                .range([0, 1.5 * Math.PI]);

            const arc = d3
                .arc()
                .innerRadius((d, i) => (i + 1) * 25)
                .outerRadius((d, i) => (i + 2) * 25)
                .startAngle(angleScale(0))
                .endAngle(d => angleScale(d.value));

            const g = svg.append("g");

            g.selectAll("path")
                .data(sortedspendings)
                .enter()
                .append("path")
                .attr("d", arc)
                .attr("fill", (d, i) => color(i))
                .attr("stroke", "#FFF")
                .attr("stroke-width", "1px")
                .on("mouseenter", function() {
                d3.select(this)
                    .transition()
                    .duration(200)
                    .attr("opacity", 0.5);
                })
                .on("mouseout", function() {
                d3.select(this)
                    .transition()
                    .duration(200)
                    .attr("opacity", 1);
                });

            g.selectAll("text")
                .data(this.spendings)
                .enter()
                .append("text")
                .text(d => `${d.region} -  ${d.value}`)
                .attr("x", -150)
                .attr("dy", -8)
                .attr("y", (d, i) => -(i + 1) * 25);

            g.attr("transform", "translate(200,300)");
        },
        getSpendings () {
            this.$http.get('http://localhost:5000/user-spending?user_id=' +
            this.user["user_id"]).then( (response) => {
                if (response.status == 200) {
                    this.spendings = response.data.spendings;
                    this.generateArc();
                }
            });
        }
    }
}
</script>
