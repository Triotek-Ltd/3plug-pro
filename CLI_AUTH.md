# 3plug-pro CLI Auth Guidance

## Current situation

The current GitHub CLI login on this machine is invalid for `kimash-255`.

That means publishing to `Triotek-Ltd` cannot proceed until auth is fixed.

## Recommended secure auth method

Use GitHub CLI browser login:

```powershell
gh auth logout -h github.com -u kimash-255
gh auth login -h github.com
```

Recommended choices:

* GitHub.com
* HTTPS
* Login with a web browser

## If a token must be used

Use a token only through GitHub CLI or a secure environment variable.

Do not paste a token into:

* chat
* markdown files
* committed scripts
* plain-text repo config files

## Organization requirement

The authenticated account must be able to create repositories in:

* `Triotek-Ltd`

## Recommended token type

Prefer a fine-grained personal access token if the organization allows it.

GitHub documents that fine-grained token access may depend on organization policy and may require approval depending on org settings. Source: [GitHub Docs](https://docs.github.com/en/organizations/managing-programmatic-access-to-your-organization/setting-a-personal-access-token-policy-for-your-organization)

## Minimum practical capability needed

The authenticated account needs enough repository and organization access to:

* create repos in the org
* read and write repo contents
* push branches and tags

If the org requires token approval, the token may not work until approved by the organization. Source: [GitHub Docs](https://docs.github.com/en/organizations/managing-programmatic-access-to-your-organization/setting-a-personal-access-token-policy-for-your-organization)

## Safe verification commands

After login, run:

```powershell
gh auth status
gh repo list Triotek-Ltd --limit 5
```

If those work, the next step is repo creation.
