#!/bin/bash
# Auto-commit and push the website whenever files change.
# Run by launchd (~/Library/LaunchAgents/com.techsutralabs.autosync.plist) on file changes and every 60s.
# Each push to main triggers .github/workflows/deploy.yml, which publishes the site.
set -u
export PATH="/usr/bin:/bin:/usr/sbin:/sbin:/opt/homebrew/bin:/usr/local/bin"
REPO="$HOME/techsutralabs-site"
LOG="$HOME/Library/Logs/techsutralabs-autosync.log"
LOCK="$REPO/.git/autosync.lock"
QUIET_SECS=15      # wait until nothing has changed for this long before committing

log(){ echo "$(date '+%Y-%m-%d %H:%M:%S') $*" >> "$LOG"; }

cd "$REPO" 2>/dev/null || exit 0
# one run at a time; clear a lock left by a crashed run after 10 minutes
if ! mkdir "$LOCK" 2>/dev/null; then
  [ -n "$(find "$LOCK" -maxdepth 0 -mmin +10 2>/dev/null)" ] && rmdir "$LOCK" && mkdir "$LOCK" || exit 0
fi
trap 'rmdir "$LOCK" 2>/dev/null' EXIT

# never interfere with a merge/rebase someone is doing by hand
[ -e .git/MERGE_HEAD ] || [ -d .git/rebase-merge ] || [ -d .git/rebase-apply ] && { log "skip: merge/rebase in progress"; exit 0; }

snapshot(){ { git status --porcelain; git diff; git ls-files -o --exclude-standard -z | xargs -0 cat 2>/dev/null; } | shasum | cut -c1-40; }

if [ -n "$(git status --porcelain)" ]; then
  prev=""
  for _ in $(seq 1 40); do          # debounce: wait for editing to settle (max ~10 min)
    cur=$(snapshot)
    [ "$cur" = "$prev" ] && break
    prev=$cur; sleep "$QUIET_SECS"
  done
  git add -A
  if ! git diff --cached --quiet; then
    files=$(git diff --cached --name-only | head -5 | tr '\n' ' ')
    n=$(git diff --cached --name-only | wc -l | tr -d ' ')
    [ "$n" -gt 5 ] && files="$files(+$((n-5)) more)"
    git commit -q -m "Auto-update: ${files% }" && log "committed $n file(s): $files"
  fi
fi

# push anything not yet on GitHub (also retries earlier failed pushes, e.g. when offline)
if [ "$(git rev-list --count @{u}..HEAD 2>/dev/null || echo 0)" -gt 0 ]; then
  if git push -q origin main 2>>"$LOG"; then
    log "pushed $(git rev-parse --short HEAD) -> deploy started"
  else
    log "push rejected; rebasing on GitHub's main and retrying"
    if git pull -q --rebase origin main 2>>"$LOG" && git push -q origin main 2>>"$LOG"; then
      log "pushed $(git rev-parse --short HEAD) after rebase -> deploy started"
    else
      git rebase --abort 2>/dev/null; log "push failed; will retry next run"
    fi
  fi
fi
