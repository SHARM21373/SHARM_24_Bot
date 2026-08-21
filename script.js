
document.addEventListener("DOMContentLoaded", function () {

    let score = Number(localStorage.getItem("sharmBalance")) || 0;

    const scoreDisplay = document.getElementById("score");
    const tapBtn = document.getElementById("tapBtn");

    function updateScore() {
        scoreDisplay.textContent = score.toLocaleString();
    }

    tapBtn.addEventListener("click", function () {
        score += 1;
        localStorage.setItem("sharmBalance", score);
        updateScore();
    });

    updateScore();
});
