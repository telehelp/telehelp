# Matkrasslig

Call a volunteer nearby if you need help with buying your groceries, or anything else.

## Features
 - No buttons required, just call the number: XXX-XXX XX XX
 - Allows you to feel good about yourself

## Installation
There are two parts to the project
 - Server &mdash; handles the data and api calls
 - Client &mdash; handles the user interface

### Server
The server is (probably going to be) written in python (`3.7.5`) and can be installed (from the root directory) with
```
cd server && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt
```
If(when) you install new dependencies, add them with `pip freeze > requirements.txt` and make sure you are running in a virtual environment, otherwise **all** of your installed packages will be added to the release. If anything is missing the deployment will fail.

To run the api simply navigate to the `server` folder and do `flask run`, the server will be available on port 5000 by default.

### Client
To be determined, but I think that [create-react-app](https://github.com/facebook/create-react-app) is worth considering. Although, [Vue](https://cli.vuejs.org/guide/creating-a-project.html) is also an option.

Currently I have just setup a simple react frontend that shows the current time.
It can be started by navbigating to the `client` directory and running `yarn start`.
If you haven't started the server you can also do it from this folder by running `yarn start-api`.


## Usage and ideas
- Login authentication can be done with JSON webtokens and the [Flask-JWT](https://pythonhosted.org/Flask-JWT/) package to allow access to protected endpoints.
- The protected endpoints handle access to account management and the [46elks api](https://46elks.se/docs/overview).
- Potentially use [Marshmallow](https://marshmallow.readthedocs.io/en/stable/) for object (de)serialization of user data.

### Hosting
- Digital ocean [droplet](https://www.digitalocean.com/products/droplets/)
- GCloud/Aws
- Linode
- Heroku PaaS
- Our own hardware
- We could use gh-pages probably if we handle the CORS, but I think that is more trouble than it's worth. We could just put our server behind CF anyway, since most the entire frontend should be cacheable. But we are not expecting that amount of users anytime soon.

## Quick Git Guide

I need to create a new branch (always branch off of master)
```
git checkout master && git pull --rebase origin master && git checkout -b <my-branch-name>
```

Either merge through a pull request or be brave and go to master and do
```
git merge <my-branch-name>
```
Branch and master conflicts are usually resolved best by rebasing as it gives a cleaner history
