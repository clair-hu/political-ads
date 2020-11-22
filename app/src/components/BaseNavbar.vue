<template>
    <div class="navbar">
        <div v-for="link in links" :key="link.title" class="navbar__item" :class="{'navbar__item--active': link.isActive}" @click="goToLink(link.url)">
            {{ link.title }}
        </div>
        <div class="logoutButton">
            <base-button class="baseButton--margin" type="default" @click.native="handleLogout()">
                <template slot="text">
                    logout
                </template>
            </base-button>
        </div>
    </div>
</template>
<script>
import BaseButton from "./BaseButton.vue";
export default {
    components: {
        BaseButton
    },
    props: {
        links: {
            type: Array
        }
    },
    methods: {
        /**
         * uses router to go to specified url
         * @param {String} url
         */
        goToLink(url) {
            console.log(url);
            this.$router.push(url);
        },
        async handleLogout() {
            try {
                await this.$store.dispatch("postLogout");
            } catch (error) {
                alert(error);
            }
        }
    }
}
</script>
<style scoped>
.navbar {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 80px;
    background-color: #72808C;
}
.navbar__item {
    width: 100px;
    height: 100%;
    padding: 0 10px;
    font-size: 16px;
    font-weight: 800;
    color: peachpuff;
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
}
.navbar__item:hover {
    background-color: #485259;
}
.navbar__item--active {
    background-color: #485259;
    font-style: italic;
    font-weight: 800;
}

.logoutButton {
    float: right;
    margin-left: auto;
    margin-right: 5%;
}
</style>
