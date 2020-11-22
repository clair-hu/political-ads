<template>
    <div id="spendingPage">
        <base-navbar :links="navLinks" />
        <div>
            <EditableTable/>
        </div>
    </div>
</template>
<script>
import BaseNavbar from "./BaseNavbar.vue";
import EditableTable from "./EditableTable.vue";
export default {
    components: {
        BaseNavbar,
        EditableTable
    },
    data(){
        return {
            navLinks: [
                {
                    title: "Dashboard",
                    isActive: false,
                    url: "/dashboard"
                },
                {
                    title: "Spend Money",
                    isActive: true,
                    url: "/spend"
                },
                {
                    title: "Challenge",
                    isActive: false,
                    url: "/challenge"
                }
            ]
        };
    }
}
</script>
<style scoped>
</style>
