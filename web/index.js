// We are using local time

const get_current_password = () => {
    let date = new Date();
  	date = date.now();
    const current_hour = parseInt(date.getHours());
    return date_to_four_digits(current_hour);
}


// valid password in the next hour
const get_future_password = () => {
    let date = new Date();
  	date = date.now();
    const current_hour = parseInt(date.getHours());
    return date_to_four_digits((current_hour + 1) % 24);
}


const date_to_four_digits = (hour) => {
 		let date = new Date();
  	date = date.now();
    const today = date.getDate() + date.getMonth() + date.getFullYear();

    // Linear Congruential Generator
    const a = 1140671485;
    const c = 128201163;
    const m = 2 ** 24;

    const seed = parseInt(String(hour) + today);
    const rand = (a * seed + c) % m;
    const password = String(rand / m);

    return password.substring(0, 15);
}

console.log(get_current_password())
console.log(get_future_password())
