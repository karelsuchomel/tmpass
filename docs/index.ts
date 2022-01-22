const convertToTwoDigitString = (number: number): string => {
  if (number > 31) {
    throw "You have supplied suspiciously large number";
  }

  const numStr = String(number);

  return numStr.length === 1 ? ("0" + numStr) : numStr;
};

const getCurrentHours = (): number => {
  return new Date().getHours();
};

// We are using local time
const get_current_password = (): string => {
  return date_to_four_digit_password(getCurrentHours());
};

// valid password in the next hour
const get_future_password = (): string => {
  const current_hour = (getCurrentHours() + 1) % 24;
  return date_to_four_digit_password(current_hour);
};

const date_to_four_digit_password = (hour: number): string => {
  let date = new Date();
  const today = convertToTwoDigitString(date.getDate()) +
    convertToTwoDigitString(date.getMonth() + 1) + date.getFullYear();

  // Linear Congruential Generator
  const a = 1140671485;
  const c = 128201163;
  const m = 2 ** 24;

  const seed = parseInt(convertToTwoDigitString(hour) + today);
  const rand = (a * seed + c) % m;
  const psw = parseFloat(String(rand / m)).toFixed(4);

  return psw.substring((psw.length - 4), psw.length);
};

// Render passwords
const renderCurrentPasswords = (currentPassword: string, futurePassword: string): void => {
  const curPswEl = document.getElementById('current-password');
  const futurePswEl = document.getElementById('future-password');

  if(curPswEl && futurePswEl) {
    curPswEl.innerText = currentPassword;
    futurePswEl.innerText = futurePassword;
  }
};

const renderTicker = (): void => {
  const tickerEl = document.getElementById('ticker');
  const minutesText = document.getElementById('minutes-text');

  if (tickerEl && minutesText) {
    const date = new Date();
    const minutes = date.getMinutes();

    if (String(minutesText.innerHTML) !== String(minutes)) {
      minutesText.innerHTML = String(60 - minutes);
      const percentage = 100/60*minutes;
      tickerEl.setAttribute('stroke-dasharray',  percentage + ", " + (100 - percentage));
    }
  }
}

const render = ():void => {
  renderCurrentPasswords(
    get_current_password(),
    get_future_password()
  );
  renderTicker();
}

const initPasswordRendering = ():void => {
  // initial render
  render();

  setInterval(() => {
    render();
  }, 1000);
};

initPasswordRendering();