import { initializeApp, getApps, getApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";

const firebaseConfig = {
  projectId: "gen-lang-client-0388415499",
  appId: "1:86856480452:web:ba318a7f60c16bd5a47b91",
  apiKey: "AIzaSyDzPOShwcwpv4VC-3dS3F2uEUA9ib33z6s",
  authDomain: "gen-lang-client-0388415499.firebaseapp.com",
  storageBucket: "gen-lang-client-0388415499.firebasestorage.app",
  messagingSenderId: "86856480452",
  measurementId: ""
};

const app = !getApps().length ? initializeApp(firebaseConfig) : getApp();
const auth = getAuth(app);
const db = getFirestore(app);

export { app, auth, db };
