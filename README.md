# NΞTRU Subscription Updater

GitHub Actions-based subscription aggregator.

## What it does

Every 12 hours it:

1. Downloads two parent subscription URLs.
2. Decodes common subscription formats (Base64/plain text).
3. Parses common URI-based configs.
4. Removes duplicates and malformed entries.
5. Runs configurable health checks.
6. Selects up to 200 healthy configs.
7. Rewrites each remark to `@nitruStore` with a stable row number.
8. Encodes the published subscription as Base64.
9. Replaces the content of the same `output/subscription` file.
10. Sends a detailed Telegram report.

The output URL therefore stays constant:

`https://raw.githubusercontent.com/OWNER/REPO/main/output/subscription`

> Base64 is encoding, not encryption. Anyone who can obtain the subscription can decode it.

## GitHub Secrets

Create these repository secrets:

- `SOURCE_1`
- `SOURCE_2`
- `BOT_TOKEN`
- `CHAT_ID`

Optional variables:

- `MAX_CONFIGS` (default `200`)
- `HEALTH_CHECK_ENABLED` (default `true`)
- `HEALTH_TIMEOUT` (default `8`)
- `HEALTH_TARGET` (default `https://www.gstatic.com/generate_204`)

## Supported URI families

The parser handles common URI forms such as:

- `vmess://`
- `vless://`
- `trojan://`
- `ss://`

Unknown URI schemes are retained only when they have a syntactically valid URI shape.

## Important GitHub setting

The workflow needs permission to write the repository contents:

Settings → Actions → General → Workflow permissions → Read and write permissions.

## Schedule

The workflow is scheduled every 12 hours. GitHub Actions cron timing is UTC and may start with some delay. You can also run it manually from the Actions tab.

## Security

Secrets are never written to the repository. The generated subscription itself is public if the repository is public.

If the source subscriptions contain credentials, assume those credentials become public through the published subscription.

## Local test

Install:

```bash
pip install -r requirements.txt
```

Then set the environment variables and run:

```bash
python -m src.main
```
