import firebase from 'firebase'
import  store  from "./store/store.js";

// firebase init goes here
const config = {
	apiKey: process.env.VUE_APP_API_KEY,
	authDomain: process.env.VUE_APP_AUTH_DOMAIN,
	databaseURL: process.env.VUE_APP_DATABASE_URL,
	projectId: process.env.VUE_APP_PROJECT_ID,
	storageBucket: process.env.VUE_APP_STORAGE_BUCKET,
    messagingSenderId: process.env.VUE_APP_MESSAGING_SENDER_ID,
    appId: process.env.VUE_APP_ADD_ID,
    measurementId: process.env.VUE_APP_MEASUREMENT_ID, 
}
firebase.initializeApp(config)

// firebase utils
const auth = firebase.auth()
const currentUser = auth.currentUser

//keep users signed in
auth.onAuthStateChanged(user => {
    if(user){
        store.dispatch('autoSignIn',{ user })
    }
})

export {
    auth,
    currentUser,
}
