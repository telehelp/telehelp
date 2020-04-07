# Telehelp - Bridge the Digital Divide

Call a volunteer nearby if you need help with buying your groceries, or anything else, if you belong to an at-risk group during the coronavirus pandemic.

## Features
 - No fancy tech required, just call the number +46766861551 from your phone to request help if you are self-isolating.
 - Built for use by minimally tech literate users
 - Signing up to be a local volunteer allows you to feel good about yourself (and do good).
 - Minimal user data collected
 - Uses ZIP codes to match you with local users

## Installation
There are two parts to the project
 - Server &mdash; handles the data and api calls
 - Client &mdash; handles the user interface

### Dependencies
The following libs needs to be installed
```
sqlcipher libsqlcipher-dev
```

### External resources

The project relies on the following APIs:

- [Google Cloud Text-to-speech](https://cloud.google.com/text-to-speech)
- [46elks telephony](https://46elks.se/)

### Server

The server is written in Python (`3.7.5`) and can be installed (from the root directory) with
```
cd server && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt
```
If(when) you install new dependencies, add them with `pip freeze > requirements.txt` and make sure you are running in a virtual environment, otherwise **all** of your installed packages will be added to the release. If anything is missing the deployment will fail.

To run the api simply navigate to the `server` folder and do `flask run`, the server will be available on port 5000 by default.

### Client
To be determined, but I think that [create-react-app](https://github.com/facebook/create-react-app) is worth considering.

It can be started by navigating to the `client` directory, build the yarn environment with `yarn`, and start it with `yarn start`.

If you haven't started the server you can also do it from this folder by running `yarn start-api`.


## Deployment
In order to initialize the deployment add the remote for the server.
```
git remote add production user@deploy_server:matkrasslig.git
```
Then push the changes to  the deployment server
```
git push production master
```
Your changes should now be deployed on the server

## Quick Git Guide

Ideally every issue should be given a pull request, this also allows for other people to check your changes as a quick code review. An extra set of eyes on code is always good.

### CLI
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
and force-push your branch to remote once it's synced. This keeps the history relatively clean as there won't be any unnecessary merge conflicts that way. **Never force push master**, this  breaks everybody's history.

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
