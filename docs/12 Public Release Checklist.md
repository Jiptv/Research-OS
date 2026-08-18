# Public Release Checklist

Use this before putting Research OS in a public or broadly shared Git repository.

## Never Publish

- `.env` or `.env.*` files with real API keys
- project folders under `../Projects`
- generated feedback signals or local learning state
- `.dashboard-settings.json`
- company logos, brand assets or deliverable artwork that is not cleared for reuse
- project-specific command shortcuts
- backup status files

## Check Locally

From the `Research OS` folder:

```sh
rg -n --hidden '(OPENAI_API_KEY|api[_-]?key|secret|token|password|Authorization|Bearer|sk-[A-Za-z0-9_-]+|ghp_|github_pat_|xox[baprs]-|BEGIN .* PRIVATE KEY)' .
```

Expected findings are references in code or docs, not real values.

Also check for personal or company-specific strings:

```sh
rg -n --hidden '(your-name|company-name|internal-project-name|/Users/|Mobile Documents|CloudDocs)' .
```

Expected findings should either be generic examples, local-only documentation, or deliberately excluded from the share package.

## GitHub Repository Recommendation

Keep these outside the public repository:

```text
UX Research/Projects/
Research OS/.env
Research OS/.dashboard-settings.json
Research OS/.backup-status.json
Research OS/08-looped-learning/feedback-signals.jsonl
Research OS/08-looped-learning/learning-loop-state.json
Research OS/08-looped-learning/review-decisions.json
Research OS/branding/company-logo.png
Research OS/branding/company-footer.png
Research OS/local-branding/
```

For public distribution, publish the Docker image from clean source and let colleagues keep their own local `Projects` folder.
