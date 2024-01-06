# SDLDiscord

## Dependencies
  - `discord.py`
  - `matplotlib`
  - `pandas`

## Building
1. Make sure you have [docker](https://www.docker.com/) installed and running
2. Create a file named `.env` in folder.
3. In the `.env` file, add 2 lines: 
   - `TOKEN="(your bot token)"`
   - `DEVELOPER_ID="(your discord user id)"`
4. Run `docker compose up --build` in the project directory.