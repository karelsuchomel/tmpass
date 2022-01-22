const convertToTwoDigitString = (number)=>{
    if (number > 31) {
        throw "You have supplied suspiciously large number";
    }
    const numStr = String(number);
    return numStr.length === 1 ? "0" + numStr : numStr;
};
const getCurrentHours = ()=>{
    return new Date().getHours();
};
const get_current_password = ()=>{
    return date_to_four_digit_password(getCurrentHours());
};
const get_future_password = ()=>{
    const current_hour = (getCurrentHours() + 1) % 24;
    return date_to_four_digit_password(current_hour);
};
const date_to_four_digit_password = (hour)=>{
    let date = new Date();
    const today = convertToTwoDigitString(date.getDate()) + convertToTwoDigitString(date.getMonth() + 1) + date.getFullYear();
    const m = 2 ** 24;
    const seed = parseInt(convertToTwoDigitString(hour) + today);
    const rand = (1140671485 * seed + 128201163) % m;
    const psw = parseFloat(String(rand / m)).toFixed(4);
    return psw.substring(psw.length - 4, psw.length);
};
const renderCurrentPasswords = (currentPassword, futurePassword)=>{
    const curPswEl = document.getElementById('current-password');
    const futurePswEl = document.getElementById('future-password');
    if (curPswEl && futurePswEl) {
        curPswEl.innerText = currentPassword;
        futurePswEl.innerText = futurePassword;
    }
};
const renderTicker = ()=>{
    const tickerEl = document.getElementById('ticker');
    const minutesText = document.getElementById('minutes-text');
    if (tickerEl && minutesText) {
        const date = new Date();
        const minutes = date.getMinutes();
        if (String(minutesText.innerHTML) !== String(minutes)) {
            minutesText.innerHTML = String(60 - minutes);
            const percentage = 100 / 60 * minutes;
            tickerEl.setAttribute('stroke-dasharray', percentage + ", " + (100 - percentage));
        }
    }
};
const render = ()=>{
    renderCurrentPasswords(get_current_password(), get_future_password());
    renderTicker();
};
const initPasswordRendering = ()=>{
    render();
    setInterval(()=>{
        render();
    }, 1000);
};
initPasswordRendering();
