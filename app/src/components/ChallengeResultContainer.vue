<template>
    <div class="challenge-result">
        <h2>{{ result_summary}}</h2>
        <ChallengeResultHeatMap v-bind:id="challenge.challenge_id" v-bind:spendingJson.sync= "this.heatmap_data" />
        <grid class="table--margin" striped hover :rows="table_rows" :cols="fields"></grid>
    </div>
</template>
<script>
import Grid from 'gridjs-vue';
import ChallengeResultHeatMap from './ChallengeResultHeatMap.vue';
export default {
    props: ['challenge'],
    components: {
        ChallengeResultHeatMap,
        Grid
    },
    data() {
        return {
            result_summary: "Calculating Results...",
            fields: [],
            challengee_name: "",
            table_rows: [],
            heatmap_data: {}
        };
    },
    computed: {
    },
    watch: {
    },
    methods: {
    },
    created(){
        console.log(this.challenge);
        if(this.challenge.challengee_name != undefined){
            this.challengee_name = this.challenge.challengee_name
        }
        this.fields = ['region_name', '# votes region is worth','You spent', this.challengee_name + " spent", 'Winner']
        
        var user_seats = 0;
        var challengee_seats = 0;
        var tie_seats = 0;

        for(var i = 0; i < this.challenge.results.length; i++){
            var result = this.challenge.results[i];
            var winner = '';
            var numerical_winner;
            if (result.challengee_spending > result.challenger_spending){
                winner = this.challengee_name + ' won.'
                numerical_winner = -1;
                challengee_seats += result.vote_num;
            } else if(result.challengee_spending == result.challenger_spending){
                winner = 'Tie';
                numerical_winner = 0;
                tie_seats += result.vote_num;
            } else {
                winner = 'You won!';
                numerical_winner = 1;
                user_seats += result.vote_num;
            }
            var row = [result.region, result.vote_num, result.challenger_spending, result.challengee_spending, winner]
            this.table_rows.push(row);
            this.heatmap_data[result.region] = numerical_winner
        }
        var result_string = "";
        if (user_seats > challengee_seats) {
            result_string += "You won!";
        } else if (user_seats === challengee_seats) {
            result_string += "It's a tie!";
        } else {
            result_string += this.challengee_name + " won!";
        }
        result_string += " You have " + user_seats + " electoral votes, " + this.challengee_name + " has " + challengee_seats + " electoral votes, and " + tie_seats + " electoral votes were not distributed due to ties."
        this.result_summary = result_string;
    }
}
</script>
<style scoped>
</style>
