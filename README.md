# Dank Memer Captcha API
A simple Dank Memer captcha-solving API. Some code credit to **[@BridgeSenseDev](https://github.com/BridgeSenseDev)**.<br>
For support (NOT STUPID QUESTIONS), join our [Discord Server](https://discord.gg/AwzRJcN6By).<br>
<br>
## Installation
This list assumes you understand how to use your computer's terminal/PowerShell and have Python [installed](https://www.python.org/downloads).<br>
1. Clone the repo: `git clone https://github.com/VillainsRule/DankCaptchaAPI.git`
2. Open the directory: `cd DankCaptchaAPI`
3. Install dependencies (this WILL take a while): `pip install -r requirements.txt`
4. Run it!<br>
  a. macs: `python3 main.py`<br>
  b. win: `py main.py`<br>
  c. linux: `python main.py`<br>
  d. if the specified for your OS doesn't work, try the others :)<br>

## Usage
#### Browser Script
```js
const data = { // fill in with your own URLs
  captcha: "https://media.discordapp.net/attachments/0/0/captcha.webp",
  opts: {
    0: "https://cdn.discordapp.com/emojis/0.webp?size=96&quality=lossless",
    1: "https://cdn.discordapp.com/emojis/0.webp?size=96&quality=lossless",
    2: "https://cdn.discordapp.com/emojis/0.webp?size=96&quality=lossless",
    3: "https://cdn.discordapp.com/emojis/0.webp?size=96&quality=lossless",
    4: "https://cdn.discordapp.com/emojis/0.webp?size=96&quality=lossless"
  }
};

fetch('/solve', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(data)
}).then((res) => res.json()).then(res => {
  console.log(res);
});
```
#### Node Script
Make sure to properly install `axios` before usage.
```js
const axios = require('axios');

const data = { // fill in with your own URLs
  captcha: "https://media.discordapp.net/attachments/0/0/captcha.webp",
  opts: {
    0: "https://cdn.discordapp.com/emojis/0.webp?size=96&quality=lossless",
    1: "https://cdn.discordapp.com/emojis/0.webp?size=96&quality=lossless",
    2: "https://cdn.discordapp.com/emojis/0.webp?size=96&quality=lossless",
    3: "https://cdn.discordapp.com/emojis/0.webp?size=96&quality=lossless",
    4: "https://cdn.discordapp.com/emojis/0.webp?size=96&quality=lossless"
  }
};

axios.post('http://localhost:42003/solve', data).then((res) => {
  console.log(res.data);
});
```
<br>
<br>
enjoy the solver :)
