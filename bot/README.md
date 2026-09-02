# Telegram reporting

There is no long-running Telegram bot process here. GitHub Actions invokes the Telegram Bot API after each update, which is much more reliable and cost-efficient for a scheduled reporting use case.

Set:

- `BOT_TOKEN`
- `CHAT_ID`

in GitHub repository secrets.
