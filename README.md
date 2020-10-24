<a href="https://github.com/prettier/prettier/"><img alt="code style: prettier" src="https://img.shields.io/badge/code_style-prettier-ff69b4.svg?style=flat-square"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Actions Status](https://github.com/telehelp/telehelp/workflows/pre-commit/badge.svg)](https://github.com/telehelp/telehelp/actions)

# Telehelp - Bridge the Digital Divide

Call a volunteer nearby if you need help with buying your groceries, or anything else, if you belong to an at-risk group during the coronavirus pandemic.

## Features

- No fancy tech required, just call the number +46766861551 from your phone to request help if you are self-isolating.
- Built for use by minimally tech literate users
- Signing up to be a local volunteer allows you to feel good about yourself (and do good).
- Minimal user data collected
- Uses ZIP codes to match you with local users

## Components

There are two parts to the project

- Server &mdash; handles the data and api calls
  - Written in Python using the Flask framework
- Client &mdash; handles the user interface
  - Redux-react application

## Deployment

In order to initialize the deployment add the remote for the server.

```
git remote add production user@deploy_server:telehelp.git
```

Then push the changes to the deployment server

```
git push production master
```

Your changes should now be deployed on the server.

## Contributing

Ideally every issue should be given a pull request, this also allows for other people to check your changes as a quick code review. An extra set of eyes on code is always good.

## Git Hooks

We use the precommit hook to format code and the like. Add it with

```
pip install pre-commit
```

and install the hook with

```
pre-commit install
```

### Git CLI

Creating a new branch to work off of (make sure that you always branch from the master branch)

```
git checkout -b <my-branch-name>
```

Then add all the commits required to the branch for solving the issue.
When the feature is done, you can push it to remote with

```
git push origin <my-branch-name>
```

and then make a pull request.
If it has conflicts with the master branch, run

```
git pull --rebase origin master
```

and force-push your branch to remote once it's synced. This keeps the history relatively clean as there won't be any unnecessary merge conflicts that way. **Never force push master**, this breaks everybody's history.

### Commit messages

A commit message is usually structured in the form

```
short description of what this commit does (generally max ~50 chars)

longer description of why it does what it does
if the the issue is complicated
```

Commit messages are written in imperative mood i.e `If applied, this commit will <my-short-description>`

## Citations

The ZIP code database file (SE.txt) used in this project is attributed to [GeoNames](http://download.geonames.org/export/zip/) and is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/).
