# FUCK YIBAN (Python ver.)

> The original script uses node.js + puppeteer. This repo is a re-written version using Python + selenium.

## ~~**THIS IS A WIP PROJECT WHICH MEANS IT NEEDS FURTHER MODIFICATION TO WORK PROPERLY! USE IT ON YOUR OWN RISK!**~~

## To-Do List

- [x] Auto report daily status
- [x] Check script
- [x] Captcha bypass
- [x] Multi-account support
- [x] QQ / Wechat notification
- [x] WebUI management
- [ ] ~~Failure warning from backup server~~ No longer needed, just go and subscribe the official wechat account to get the alarm.
- [ ] Non-GUI mode to reduce hardware utilization

## Requirements

```powershell
pip install -r requirements.txt
```

## Target Users

SU_T students :D

## Usage

1. Install requirements via pip
2. Install ` chromedriver` and `Google Chrome`
3. Toggle bot on/off through `main.py`
4. Type your accounts in `accounts.py`
5. Configure your `Miraibot` and `ServerChan`  stuff in `notification.py` 
6. Set your Chaoyiying accounts in `captcha.py`
7. Launch `cmd` and type `python main.py` to test if it works
8. Set schedule rule in Control Panel

## Change Log

- 2021.04.05

  > 1. Optimized code structure

- 2021.03.16

  > 1. Add bot toggles
  > 2. Add codes to flush DNS cache

- 2021.03.06

  > 1. Add support for new api
  >
  > 2. Update README.md
  >
  > 3. Update LICENSE 

- 2021.02.28

  > A LOT OF CHANGES

- 2021.02.27

  > Initial commit