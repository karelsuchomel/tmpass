const convertToTwoDigitString = (number)=>{
    if (number > 31) {
        throw "You have supplied suspiciously large number";
    }
    const numStr = String(number);
    console.log(numStr);
    return numStr.length === 1 ? "0" + numStr : numStr;
};
const getCurrentHours = ()=>{
    let date = new Date();
    return date.getHours();
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
    console.log(seed);
    const rand = (1140671485 * seed + 128201163) % m;
    const psw = parseFloat(String(rand / m)).toFixed(4);
    return psw.substring(psw.length - 4, psw.length);
};
console.log(get_current_password());
console.log(get_future_password());
