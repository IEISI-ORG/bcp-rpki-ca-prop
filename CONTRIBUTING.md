# Working on this draft

This repo auto-submits new revisions of `draft-sweetser-bcp-rpki-ca` to the IETF
datatracker. That makes ordinary pushes to `main` consequential — each one that
changes the draft's body becomes a real, public revision. Work on a branch and
merge via PR instead of pushing directly to `main`.

## Branch and PR workflow

```bash
# 1. Branch off main
git checkout -b editorial/short-description

# 2. Edit draft-sweetser-bcp-rpki-ca-NN.md (whatever NN currently is), commit
#    as many times as you like -- none of this touches main or the datatracker.
git add -A
git commit -m "docs(draft): ..."

# 3. Push the branch and open a PR
git push -u origin editorial/short-description
gh pr create --base main --head editorial/short-description --title "..." --body "..."

# 4. Merge when ready
gh pr merge <number> --squash --delete-branch
```

A GitHub push event fires once per `git push`, regardless of how many commits
it carries — so merging a PR, however many commits happened on the branch,
counts as **one** push to `main`. That's the natural batching point: a whole
round of edits becomes exactly one new revision and one submission, not one
per commit.

## What CI does automatically

On every push (including from a PR branch, before merge) and every PR,
`.github/workflows/build-draft.yml`:

1. Builds the current `draft-sweetser-bcp-rpki-ca-NN.md` via `mmark` into XML,
   then `xml2rfc` into `.txt`/`.html`.
2. Validates the XML with `xml2rfc --strict`.

Two further steps run **only on a push to `main`** (never on a PR branch, so a
branch's build failing or its content changing never has side effects until
it's actually merged):

3. **Auto-bump the revision.** Hashes the draft body (excluding the `date =`
   and `value = "draft-sweetser-bcp-rpki-ca-NN"` frontmatter lines, so CI's own
   edits to those never trigger a repeat bump) and compares it against
   `.ietf-content-hash`, recorded at the last bump. If the body actually
   changed, CI renames the four build files to the next revision number,
   rewrites those two frontmatter lines, and records the new hash. You never
   need to rename files or touch the version number by hand — just edit the
   body.
4. **Submit to the datatracker.** If the revision number changed (tracked in
   `.ietf-submission-state`), CI POSTs the built XML to
   `https://datatracker.ietf.org/api/submission`.

## The one step that can't be automated

The datatracker emails a confirmation link to the registered author address
(`tcsweetser@gmail.com`) after every submission, and the revision stays
unpublished until that link is clicked. This is the datatracker's
anti-impersonation control — it can't be scripted around, by design. Expect
one confirmation email per merged PR that changes the draft body.

## State files

- `.ietf-content-hash` — hash of the last-bumped revision's body. Don't edit by
  hand; if it's ever out of sync with what's actually on the datatracker,
  recompute it from the last successfully *submitted* content
  (`git show <submitted-commit>:draft-sweetser-bcp-rpki-ca-NN.md`), the same
  way it was seeded originally -- not from whatever's currently in the working
  tree, or CI will submit a revision number that's already taken.
- `.ietf-submission-state` — last revision number actually POSTed to the
  datatracker.
