# IITM Discourse Repeatable Scraper

This exports an authenticated Discourse category using your logged-in Chrome profile.

It saves:

- `discourse_export.json` with topics, posts, user profiles, raw post/profile payloads, metadata, and local image paths
- `discourse_topics.csv`
- `discourse_posts.csv`
- `discourse_users.csv`
- `topic_errors.jsonl` when individual topics return errors such as `403` or `404`
- `profile_errors.jsonl` and `image_errors.jsonl` when those resources cannot be exported
- `topic_journal.jsonl` and `profile_journal.jsonl`, flushed immediately as each result completes
- `error.log` with a human-readable line for resource fetches that still fail after retries
- `imgs/` with images referenced inside post/reply content
- `state.json` in this scraper folder so reruns skip unchanged topics

The JSONL journals are written immediately. The larger JSON and CSV snapshots are atomically refreshed every few completed items, at each category-page boundary, and at the end. An interrupted write therefore leaves the last complete snapshot intact. While a run is still in progress, `discourse_export.json -> metadata.status` is `partial`; after a full run completes, it is `complete`.

Network calls use async `httpx` with one shared concurrency cap. By default, at most 10 requests are active across topic JSON fetches, image downloads, user profile fetches, and LLM fallback calls.

## 1. Install Dependencies

```powershell
cd C:\Users\jibzm\Documents\Codex\2026-07-11\i\outputs\discourse_scraper
python -m pip install -r requirements.txt
```

Playwright is only used to read authenticated cookies from Chrome over the DevTools port. It does not need to install a separate browser.

## 2. Pick the Chrome Profile

```powershell
python scrape_discourse.py profiles
```

On this machine, the likely DS profiles are:

- `Profile 4`: `ds.study.iitm.ac.in` / `21f1001895@ds.study.iitm.ac.in`
- `Profile 7`: `jessin ds.study.iitm.ac.in`

Because both include `ds.study`, use the exact folder or email if selection is ambiguous:

```powershell
python scrape_discourse.py profiles --profile "Profile 4"
python scrape_discourse.py profiles --profile "21f1001895"
```

## 3. Launch Chrome With Debugging Enabled

Run:

```powershell
python scrape_discourse.py launch --profile "Profile 4"
```

The command now waits for Chrome DevTools to become reachable before returning. A healthy launch prints a line like:

```text
Chrome DevTools: ready at http://127.0.0.1:9222 (Chrome/...)
```

Chrome now launches with a persistent non-standard debug user data directory:

```text
C:\Users\jibzm\Documents\Codex\2026-07-11\i\outputs\discourse_scraper\chrome_debug_user_data
```

Chrome should open to:

```text
https://discourse.onlinedegree.iitm.ac.in
```

This debug Chrome profile is separate from your normal Chrome profile. On the first run, log in to IITM Discourse inside this new Chrome window. After that, the login should persist in `chrome_debug_user_data`.

Confirm that this debug Chrome window can open:

```text
https://discourse.onlinedegree.iitm.ac.in/c/courses/mlt-kb/32
```

## 4. Check Authentication

```powershell
python scrape_discourse.py doctor
```

If this says Chrome DevTools is not reachable, launch Chrome again with the profile command above.

If `launch` says Chrome exited or DevTools timed out, close any scraper Chrome windows and try a fresh debug profile directory:

```powershell
python scrape_discourse.py launch --profile "Profile 4" --debug-user-data-dir .\chrome_debug_user_data_fresh
```

Then log in to Discourse inside that new Chrome window and rerun `doctor`.

If this says Discourse is not authenticated, log in inside that Chrome profile and rerun `doctor`.

## 5. Run the Scraper

```powershell
python scrape_discourse.py scrape
```

The default scrape target is:

```text
https://discourse.onlinedegree.iitm.ac.in/c/courses/mlt-kb/32
```

The default output folder is:

```text
C:\Users\jibzm\Documents\Codex\2026-07-11\i\outputs
```

## Useful Commands

Scrape only the first page while testing:

```powershell
python scrape_discourse.py scrape --max-pages 1
```

Refresh cached user profiles:

```powershell
python scrape_discourse.py scrape --refresh-users
```

Use a slower rate limit:

```powershell
python scrape_discourse.py scrape --rate-limit-seconds 1.5
```

Tune per-topic HTTP retries:

```powershell
python scrape_discourse.py scrape --topic-retries 4 --topic-retry-delay-seconds 2
```

`--topic-retries 2` is the default, meaning each topic gets 1 initial request plus 2 retries before being recorded as failed.

Tune the global async request cap:

```powershell
python scrape_discourse.py scrape --max-concurrent-requests 10
```

Category pagination remains sequential, but topics within each category page run concurrently under this cap. Image downloads, user profile fetches, and LLM calls share the same cap.

Use a custom Chrome debug profile directory:

```powershell
python scrape_discourse.py launch --profile "Profile 4" --debug-user-data-dir C:\path\to\chrome_debug_user_data
```

## Optional LLM Fallback

The scraper can use an OpenAI-compatible local LLM endpoint as a fallback when post metadata is missing, or as an audit pass.

Create `llm_config.json` in this folder:

```json
{
  "LLM_BASE_URL": "http://localhost:8317/v1",
  "LLM_MODEL": "xxx",
  "LLM_API_KEY": "xxx"
}
```

You can also use lowercase keys:

```json
{
  "base_url": "http://localhost:8317/v1",
  "model": "xxx",
  "api_key": "xxx"
}
```

If a value is missing from `llm_config.json`, the scraper falls back to these environment variables:

```powershell
$env:LLM_BASE_URL="http://localhost:8317/v1"
$env:LLM_MODEL="xxx"
$env:LLM_API_KEY="xxx"
```

Then run:

```powershell
python scrape_discourse.py scrape --llm-fallback missing
```

Use a custom config path:

```powershell
python scrape_discourse.py scrape --llm-fallback missing --llm-config C:\path\to\llm_config.json
```

Modes:

```text
off      default, no LLM
missing  use LLM only for incomplete post records
always   call LLM for every post as an audit/enrichment pass
```

The LLM prompt is strict: it says **do not make up data**, use only supplied evidence, return `null` or `[]` when evidence is missing, and include evidence for every non-empty field. The scraper rejects any LLM field that has a value but no evidence.

LLM audit entries are appended to:

```text
C:\Users\jibzm\Documents\Codex\2026-07-11\i\outputs\llm_fallback_log.jsonl
```

## Notes

- The scraper uses Discourse JSON endpoints instead of brittle rendered HTML scraping.
- It maintains `state.json` and only refetches topics whose Discourse summary changed. Corrupt interrupted state/export files are preserved with a `.corrupt-*` suffix and rebuilt safely.
- It uses async `httpx` requests after Chrome cookies are extracted from Playwright.
- Topics include every post ID advertised by Discourse, including replies omitted from the initial topic response. The topic data records stream and exported post counts for verification.
- If a topic, user profile, or image returns an error, the scraper retries transient errors first, records the failure, and continues with remaining data. `403` is retried because a freshly copied authenticated session may become usable.
- Images are downloaded only from post/reply content, not avatars. Failed image URLs remain in each post's `image_errors` metadata.
- Chrome requires a non-standard `--user-data-dir` for remote debugging, so the scraper uses `chrome_debug_user_data` instead of the normal Chrome profile directory.
- Do not commit or share `llm_config.json` if it contains a real API key.
- Use this only for content you are authorized to access and export.
