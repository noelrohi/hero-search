# Guardian Tales Hero Search

## Slash Commands
 - `/lookup` 

## Commands
 - `nlookup` or `nlu`

## Run in local

[Fork](https://github.com/gneiru/hero-search/fork) or clone this repo
```bash
git clone https://github.com/gneiru/hero-search.git
```
```bash
cd hero-search
```
Make virtual environment for python
```bash
python -m venv env
```
Activate
```bash
env\scripts\activate
```
Rename `env.example` into `.env` then enter your [bot token](https://discord.com/developers/applications/)

Add the bot in your server using with:
`https://discord.com/api/oauth2/authorize?client_id=<BOT-ID>&permissions=2147494912&scope=bot`
Replace `BOT-ID` placeholder

```bash
pip install -r requirements.txt
```

Finally, run the bot
```bash
python main.py
```



