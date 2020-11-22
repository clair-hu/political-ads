<template>
    <div id="table-div">
        <h2> Balance: ${{balance}} </h2>
        <vue-editable-grid
            class="grid"
            ref="grid"
            :column-defs="columnDefs"
            :row-data="rows"
            row-data-key='shipmentId'
            @cell-updated="cellUpdated"
            @row-selected="rowSelected"
            @link-clicked="linkClicked"
        >
        </vue-editable-grid>
    </div>
</template>
<script>

const columnDefinition = [
  { sortable: true, filter: true, field: 'region', headerName: 'Region', editable: false },
  { sortable: true, filter: true, field: 'spending', headerName: 'Spendings', editable: true }
]
export default {
    name: "EditableTable",
    data() {
        return {
            columnDefs: columnDefinition,
            rows: [],
            spendings: [],
            expandedSpendings: [],
            selectedRow: null,
            regions: null,
            balance: 0,
        };
    },
    async created () {
        var response = await this.$http.get('http://localhost:5000/balance?user_id='+this.user["user_id"]);
        this.balance = response.data.data.balance;
        response = await this.$http.get('http://localhost:5000/user-spending?user_id=' + this.user["user_id"]);
        if (response.status == 200 && response.data != null) {
            this.spendings = response.data.spendings;
        }
        response = await this.$http.get('http://localhost:5000/regions');
        this.regions = response.data.regions;
        this.formatData()
    },
    computed: {
        user() {
            return this.$store.getters.user;
        }
    },
    mounted() {

    },
    methods: {
        formatData() {
            // this.rows = this.spendings;
            this.expandedSpendings = [];
            for(const region of this.regions){
                var name = region.region_name;
                var found = false;
                for(var i = 0; i < this.spendings.length; i++){
                    if(this.spendings[i].region == name){
                        this.expandedSpendings.push({region: name, spending: this.spendings[i].value});
                        found = true;
                        break;
                    }
                }
                if(!found){
                    this.expandedSpendings.push({region: name, spending: 0});
                }
            }
            this.rows = JSON.parse(JSON.stringify(this.expandedSpendings));
        },
        cellUpdated ($event) {
            console.log($event);
            if(isNaN($event.value)){
                this.rows = JSON.parse(JSON.stringify(this.expandedSpendings));
                alert("Must enter a number in the row");
                return;
            }
            var spent = +$event.value
            if(spent < 0){
                this.rows = JSON.parse(JSON.stringify(this.expandedSpendings));
                alert("Must enter a positive number in the row");
                return;
            }

            var oldSpent = 0;
            var region = $event.row.region;
            for(var i = 0; i < this.expandedSpendings.length; i++){
                if(this.expandedSpendings[i].region == region){
                    oldSpent = this.expandedSpendings[i].spending;
                    break;
                }
            }
            //check if they entered too much
            if(this.balance - (spent-oldSpent) < 0){
                this.rows = JSON.parse(JSON.stringify(this.expandedSpendings));
                alert("You don't have enough money to spend that much");
                return;
            }

            // valid
            this.balance = this.balance - (spent-oldSpent);
            var region_id = -1;
            for(i = 0; i < this.regions.length; i++){
                if(this.regions[i].region_name == region){
                    region_id = this.regions[i].region_id; 
                }
            }
            const body = {
                "user_id":this.user["user_id"],
                "region_id":region_id,
                "value":spent
            }
            this.$http.put('http://localhost:5000/update-spending', body).then( response => {
                if(response.status == 200){
                    this.expandedSpendings = JSON.parse(JSON.stringify(this.rows));
                }
            },
            err => {
                console.log(err);
            })
        },
        rowSelected ($event) {
        this.selectedRow = $event.rowData
        },
        linkClicked ($event) {
        console.log($event)
        },
        removeCurrentRow () {
        this.rows = this.rows.filter(row => row.id !== this.selectedRow.id)
        },
        contextMenu ($event) {
        console.log($event)
        },
    }
}
</script>
<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #D3C1AF;
  font-size: 14px;
  height: 400px;
}

.grid {
  height: 100%;
}

.ml-1 {
  margin-left: 10px;
}
#table-div{
    display: flex;
    flex-direction: column;
    justify-content: space-evenly;
    align-items: center;
}
</style>