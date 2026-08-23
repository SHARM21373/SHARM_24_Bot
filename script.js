const API_URL = "https://sharm-backend.onrender.com";

const tg = window.Telegram.WebApp;

tg.ready();
tg.expand();

const initData = tg.initData;
const user = tg.initDataUnsafe?.user || {};

let referrerId = null;

const startParam = tg.initDataUnsafe?.start_param;

if (startParam) {
    const parsed = parseInt(startParam, 10);

    if (!isNaN(parsed) && parsed > 0) {
        referrerId = parsed;
    }
}

const balanceEl = document.getElementById("balance");
const batteryEl = document.getElementById("battery");
const processingEl = document.getElementById("processing");

const usernameEl = document.getElementById("username");
const accountIdEl = document.getElementById("accountId");

const referralsEl = document.getElementById("referrals");
const tapButton = document.getElementById("tapButton");

const referralLinkInput =
    document.getElementById("referralLinkInput");

const friendsList =
    document.getElementById("friendsList");

if (user.id) {

    usernameEl.textContent =
        "👤 " + (user.username ? "@" + user.username : user.first_name);

    accountIdEl.textContent =
        "Telegram ID: " + user.id;
}
