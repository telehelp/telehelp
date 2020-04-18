# Server

### Dependencies

The following libs needs to be installed for sqlcipher support.

```
sqlcipher libsqlcipher-dev libpython3.6-dev libsqlite3-dev
```

For redis support

```
sudo apt-get install redis-server && sudo systemctl enable redis-server.service

# Edit the maxmemory(256/512 mb) and eviction policy(allkeys-lru)
sudo vim /etc/redis/redis.conf
sudo systemctl restart redis-server.service
```

Check that it's functional by checking

```
redis-cli
127.0.0.1:6379> ping
PONG
127.0.0.1:6379>
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

### Environmental Varialbles

In order for the server to operate as intended you need to set a few environmental variables before you start. It is recommended to put these in a .env file that Flask can read automatically.

```bash
#.env
DATABASE_KEY=your_secret_key
API_USERNAME=your_user
API_PASSWORD=your_pass
ELK_NUMBER=your_number
DATABASE=test.db
BASE_URL=https://mysite.org
SECRET_KEY=your_secret_key #can be generated with for example: secrets::token_urlsafe
```

## Database

Write this in order to read the database

```
sqlcipher database.db
```

Then type in your key

```
PRAGMA key="x'your_secret_32B_hex_key'"
```
