<template>
    <div id="homePage">
        <div class="title">
            <h1>
                CS348 Project
            </h1>
            <h3>
                Political Ads Application
            </h3>
        </div>
        <div>
        </div>
        <div class="options">
            <div class="homePage__bigButton homePage__bigButton--orange" @click="goToLoginPage()">
                Login
            </div>
            <div class="homePage__bigButton homePage__bigButton--purple" @click="goToSignUpPage()">
                Sign up
            </div>
        </div>
        <div class="description">
            <p>
                Our users are anyone who has interests in political data from US presidential selection. We have decided to use the web as our primary user interface since we suspect that the majority of users interested in Facebook’s political advertisement data would prefer a webpage over a command-line interface. 
            </p>
            <p>
                On our application, a user can create a mock campaign with a set budget. A user will be able to allocate money on advertisements in different regions and then compare their campaign statistics with other regions. We plan on providing graphs and other interesting data visualisation to depict how different politicians target specific demographics and regions. Users can also see how other users allocate funds for different candidates. These analyses are visualized in the form of heat maps and graphs. 
            </p>
            <p>
                We choose to work with a publicly available dataset provided by the Facebook Ad Library Report. These datasets describe spendings and audience targeting for political campaigns in Facebook Ads. In order to work with this dataset we plan on preprocessing the data in order to remove Facebook specific information as well as curate the dataset to more easily retrieve the data we are looking for.
            </p>

        </div>
    </div>
</template>
<script>
export default {
    methods: {
        goToLoginPage() {
            this.$router.push('login');
        },
        goToSignUpPage() {
            this.$router.push('signup');
        }
    }
};
</script>
<style scoped>
#homePage {
    display: flex;
    flex-direction: column;
    justify-content: space-evenly;
    align-items: center;
}
.options{
    display: flex;
}
.title{
    text-align: center;
    color: white;
}
.title h1{
    font-size: 100px;
}
.title h3{
    font-size: 80px;
    font-style: italic;
}

.description{
    color: white;
    padding: 5% 5% 5% 5%;
}

.homePage__bigButton {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 250px;
    width: 400px;
    margin: 20px;
    border-radius: 5px 30% 5px 30%;
    font-size: 80px;
    font-weight: 900;
    font-style: italic;
}
.homePage__bigButton--orange {
    border: solid 5px#ffb26d;
    background-color: #ffcda0;
    color: #66574a;
}
.homePage__bigButton--orange:hover {
    background-color: #e5b890;
    cursor: pointer;
}
.homePage__bigButton--purple {
    border: solid 5px#a594b7;
    background-color:#cfbae5;
    color: #524a5b;
}
.homePage__bigButton--purple:hover {
    background-color: #baa7ce;
    cursor: pointer;
}

</style>
