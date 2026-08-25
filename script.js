const API_URL = "https://onrender.com";
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

// DOM Elements
const balanceEl = document.getElementById("balance");
const batteryEl = document.getElementById("battery");
const processingEl = document.getElementById("processing");
const usernameEl = document.getElementById("username");
const accountIdEl = document.getElementById("accountId");
const referralsEl = document.getElementById("referrals");
const tapButton = document.getElementById("tapButton");
const referralLinkInput = document.getElementById("referralLinkInput");
const friendsList = document.getElementById("friendsList");

// Initial Setup when DOM is loaded
document.addEventListener("DOMContentLoaded", () => {
    if (user.id) {
        if (usernameEl) usernameEl.textContent = "👤 " + (user.username ? "@" + user.username : user.first_name);
        if (accountIdEl) accountIdEl.textContent = "Telegram ID: " + user.id;
        
        // Generate and display referral link
        if (referralLinkInput) {
            referralLinkInput.value = `https://t.me{user.id}`;
        }

        // Fetch existing data from Backend Server
        loadUserData();
    } else {
        console.error("Telegram User Data not found! Please open inside Telegram.");
    }

    // Tap Button Click Event
    if (tapButton) {
        tapButton.addEventListener("click", () => {
            handleTap();
        });
    }
});

// Function to fetch user details from Render Python Backend
async function loadUserData() {
    try {
        const response = await fetch(`${API_URL}/api/user?id=${user.id}&referrer=${referrerId || ''}`);
        if (response.ok) {
            const data = await response.json();
            // Update UI elements with backend data
            if (balanceEl) balanceEl.textContent = data.balance || 0;
            if (batteryEl) batteryEl.textContent = (data.energy || 100) + "%";
            if (referralsEl) referralsEl.textContent = data.referral_count || 0;
            
            // Render Friends List if available
            if (friendsList && data.friends) {
                friendsList.innerHTML = "";
                data.friends.forEach(friend => {
                    const li = document.createElement("li");
                    li.textContent = `👤 ${friend.username || friend.first_name}`;
                    friendsList.appendChild(li);
                });
            }
        }
    } catch (error) {
        console.error("Error fetching user data from backend:", error);
    }
}

// Function to handle Coin Tapping and Sync with Server
async function handleTap() {
    if (!balanceEl) return;
    let currentBalance = parseInt(balanceEl.textContent) || 0;
    
    // Optimistic UI update (Instant feedback for user)
    currentBalance += 1;
    balanceEl.textContent = currentBalance;

    try {
        const response = await fetch(`${API_URL}/api/tap`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                id: user.id,
                balance: currentBalance
            })
        });
        
        if (!response.ok) {
            console.error("Failed to sync tap with server");
        }
    } catch (error) {
        console.error("Error syncing tap:", error);
    }
}
