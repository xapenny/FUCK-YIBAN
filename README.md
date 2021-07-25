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
- [x] Non-GUI mode to reduce hardware utilization

## Requirements

```powershell
pip install -r requirements.txt
```

## Target Users

SU_T students :D

## Usage

1. Install requirements via pip
2. Install ` chromedriver` and `Google Chrome`
3. Run `python3 config.py` then choose initialize and go through the whole settings
4. Run `python3 main.py` and enjoy

## Change Log

- 2021.07.25

> 1. Add custom location support
> 2. Add config functionality

- 2021.06.11

  > 1. Fixed: Bark notifications may not send properly when QQbot is disabled
  > 2. Add support for Linux
  > 3. Some random optimization 

- 2021.05.29

  > **IMPORTANT NOTICE : You have to regenerate `account.ini` by running `config.py`, or it will NOT compatible with this version**
  >
  > 1.  Changed browser UA to Safari on iOS
  > 2.  Now the url can be auto-renewed while it expired
  > 3.  Add a backup mode 

- 2021.05.25

  > 1. Fixed: Bark push not working

- 2021.05.24

  > 1. Fully rewrite the code.
  > 2. Removed support for Mirai framework due to the insane instability.

- 2021.05.19

  > 1. Added support for XiaoLz framework
  > 2. Optimized code structure
  > 3. Reduced system resource consumption

- 2021.04.13

  > 1. Fixed a bug caused sending notification to unexpected person
  > 2. Add Bark push for iOS

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