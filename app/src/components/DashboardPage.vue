<template>
    <div id="dashboardPage" class="dashboard">
        <base-navbar :links="navLinks" />
        <div class="dashboard__content">
             <div id="user-info-div">
                <h1> Summary of spending for {{user.user_name}}</h1>
                <h3> Candidate that you are mimicking: {{candidate_name}} </h3>
            </div>
            <!-- <div class="heatmap-div">
               <RegionChart/>     
            </div> -->
            <div class="heatmap-div">
                <h1> Heatmap of your spending </h1>
                <HeatMap v-bind:id="1" v-bind:spendingJson.sync= "this.userSpending"/>
            </div>
            <div class="heatmap-div">
                <h1> Heatmap of {{candidate_name}}'s spending </h1>
                <HeatMap v-bind:id="2" v-bind:spendingJson.sync= "this.candidateSpending"/>
            </div>
            <div class="heatmap-div">
                <h1> Heatmap of the average user's spending who mimics {{candidate_name}} </h1>
                <HeatMap v-bind:id="3" v-bind:spendingJson.sync= "this.avgUserSpending"/>
            </div>
        </div>
    </div>
</template>
<script>
//import RegionChart from "./Chart.vue";
import HeatMap from "./HeatMap.vue";
import BaseNavbar from "./BaseNavbar.vue";

export default {
    components: {
        BaseNavbar,
        //RegionChart,
        HeatMap
    },
    data() {
        return {
            navLinks: [
                {
                    title: "Dashboard",
                    isActive: true,
                    url: "/dashboard"
                },
                {
                    title: "Spend Money",
                    isActive: false,
                    url: "/spend"
                },
                {
                    title: "Challenge",
                    isActive: false,
                    url: "/challenge"
                }
            ],
            userSpending: {},
            candidateSpending: {},
            avgUserSpending: {},
            candidate_name: ""
        };
    },
    computed: {
        user() {
            return this.$store.getters.user
        }
    },
    watch: {
        user(value) {
            if(value === null || value === undefined){
                //sign up complete, redirect
                this.$router.push('/');
            }
        }
    },
    mounted() {
        this.getUserSpending(this.user.user_id);
        this.getCandidateSpending();
    },
    methods: {
        getUserSpending(user_id) {
            this.$http.get('http://localhost:5000/user-spending-heatmap?user_id=' + user_id).then((response) => {
                if (response.status === 200 ) {
                    this.userSpending = response.data.data;
                }
            });
        },
        getCandidateSpending() {
            this.$http.get('http://localhost:5000/mimics?user_id=' + this.user.user_id ).then( (candidate_resp) => {
                if (candidate_resp.status === 200) {
                    let candidate_id = candidate_resp.data.data.mimics;
                    this.$http.get('http://localhost:5000/user-spending-heatmap?user_id=' + candidate_id).then((response) => {
                        if (response.status === 200 ) {
                            this.candidateSpending = response.data.data;
                        }
                    });
                    this.$http.get("http://localhost:5000/official-candidates").then((response) => {
                        var candidates = response.data.candidates;
                        for(var i = 0; i < candidates.length; i++){
                            if(candidates[i].user_id == candidate_id){
                                this.candidate_name = candidates[i].user_name.replace("'", "").replace("'", "");
                            }
                        }
                    });

                    this.$http.get('http://localhost:5000/average-mimic-spending-heatmap?candidate_id=' + candidate_id).then((response) => {
                        if (response.status === 200 ) {
                            this.avgUserSpending = response.data.data;
                        }
                    });
                }
            });
        }
    }
}
</script>
<style scoped>
.dashboard__content {
    display: flex;
    flex-direction: column;
}

.baseButton--margin {
    margin: 10px auto;
    justify-self:flex-end;
}

.heatmap-div {
    padding-bottom: 3%;
    border-bottom: 1px solid
}

</style>
