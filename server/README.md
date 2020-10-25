# Server

### Environmental Varialbles

In order for the server to operate as intended you need to set a few environmental variables before you start. It is recommended to put these in a .env file that Flask can read automatically.

```
cp .env.example .env
```

The example file include the following fields

```
DATABASE_KEY=your_secret_key
ELK_USERNAME=your_user
ELK_PASSWORD=your_pass
ELK_NUMBER=your_number
DATABASE=test.db
BASE_URL=https://mysite.org
SECRET_KEY=your_secret_key #can be generated with for example: secrets::token_urlsafe
HOOK_URL=optional-discord-hook-url

POSTGRES_PASSWORD=postgres
POSTGRES_USER=postgres

REDIS_HOST=localhost
REDIS_PORT=6379

PGADMIN_DEFAULT_EMAIL=test@telehelp.se
PGADMIN_DEFAULT_PASSWORD=postgres
```

### Running the server

The server is deployed with docker so just navigate to the root directory and do

```
docker-compose up --build
```

The api will be available on port 5000.

### Database access

The first time running the project you have to create the database manually.

Open up pgadmin that is available at http://localhost:54321

Next, login with the following credentials:

- **email:** _test@telehelp.se_
- **password:** _postgres_

Then follow these instructions:

- Click "Add New Server"
- Enter "telehelp" in the name field
- Click the "connection" tab
- Enter "db" in the host name/address field
- Enter "postgres" in the username field
- Enter "postgres" in the password field

You should now have access to the database, on the left side panel.

### External resources

The project relies on the following APIs:

- [Google Cloud Text-to-speech](https://cloud.google.com/text-to-speech)
- [46elks telephony](https://46elks.se/)
