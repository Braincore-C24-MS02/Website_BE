// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyAFYEUUziI12WWTrFgR3omCKDFuy-jBnPU",
  authDomain: "bangkit-capstone-dms.firebaseapp.com",
  projectId: "bangkit-capstone-dms",
  storageBucket: "bangkit-capstone-dms.appspot.com",
  messagingSenderId: "987502499591",
  appId: "1:987502499591:web:7cd1c908910dd73b4a17a2",
  measurementId: "G-8Y7NLPFNC9"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);