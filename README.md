# SDLDiscord

## Dependencies
 - applications
   - docker
   - python
 - python modules
   - `discord.py`
   - `ffmpeg`
   - `youtube_dl`
   - `matplotlib`
   - `pandas`

## Building
1. create a file named `.env` in folder
2. in `.env` file, add 2 lines: `TOKEN="(your bot token)"`, `DEVELOPER_ID="(your discord user id)"`
3. run `docker compose up --build`