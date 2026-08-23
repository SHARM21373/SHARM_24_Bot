document.addEventListener("DOMContentLoaded", async function () {
    const tg = window.Telegram?.WebApp;
    const telegramUser = tg?.initDataUnsafe?.user;
    
    const telegramId = telegramUser?.id || "8746453103"; 
    const username = telegramUser?.username || "";
    const firstName = telegramUser?.first_name || "";

    const urlParams = new URLSearchParams(window.location.search);
    const referralId = urlParams.get('tgWebAppStartParam') || null;

    const scoreDisplay = document.getElementById("score");
    const tapBtn = document.getElementById("tapBtn");
    
    let score = 0;

    async function loadUserData() {
        try {
            const response = await fetch('/api/auth/telegram', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    telegramId: telegramId,
                    username: username,
                    firstName: firstName,
                    referralId: referralId
                })
            });
            const data = await response.json();
            
            if (data.success && data.user) {
                score = Number(data.user.balance);
                updateScoreDisplay();
            }
        } catch (error) {
            console.error("Failed to load user data from database:", error);
            score = Number(localStorage.getItem("sharmBalance")) || 0;
            updateScoreDisplay();
        }
    }

    function updateScoreDisplay() {
        if (scoreDisplay) {
            scoreDisplay.textContent = score.toLocaleString();
        }
    }

    async function sendTapToDatabase(count) {
        try {
            const response = await fetch('/api/tap', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    telegramId: telegramId,
                    tapCount: count
                })
            });
            const data = await response.json();
            if (data.success) {
                score = Number(data.currentBalance);
                localStorage.setItem("sharmBalance", score);
                updateScoreDisplay();
            }
        } catch (error) {
            console.error("Failed to save tap score to database:", error);
        }
    }

    if (tapBtn) {
        tapBtn.addEventListener("click", function () {
            score += 1; 
            updateScoreDisplay();
            sendTapToDatabase(1);
        });
    }

    await loadUserData();
});
