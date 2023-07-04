# ITStep-Bank-WebSite
StepIT graduate work

<img src="https://github.com/anigilyatornayapushka/ITStep-Bank-WebSite/raw/main/tools/stepitlogo.png">

## Functionality

- Registration and authorization using jwt.

- Activation of account by email.

- Forget password function.

- Change Password.

- Creation and binding of virtual cards to the user.

- Currency convertation.

- Money transfer between users.

- Money replenishment and withdrawing.

- Check all transactions with ability to filter it.

## Requirements

To use this project, you will need the following:

- Create .env file in root directory and add following values:

```dotenv
SECRET_KEY=<your secret key>
DEBUG=True
SENTRY_SDK_DSN=<your sentry-sdk link>
DB_NAME=<your database name>
DB_USER=<your database username>
DB_PASS=<your database password>
DB_HOST=127.0.0.1
DB_PORT=5432
EMAIL_HOST_PASSWORD=<your email host password>
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=<your email>
FERNET_KEY=<your fernet secret key, for-example, cV--O0imNTvZIIn0rKCumCSzCWeRvD0sjJsJmqmLc0Q= >
EXCHANGE_RATES_URL=https://v6.exchangerate-api.com/v6/d095554f583b273fcad2ae46/latest/
RABBITMQ_USERNAME=guest
RABBITMQ_PASSWORD=guest
```

- Required libraries: See [req.txt](tools/requirements/req.txt) for the list of required libraries.

- Redis: Install Redis from the official website. You can find the installation instructions [here](https://redis.io/docs/getting-started/installation/).

- PostgreSQL: Download and install PostgreSQL from the official website. You can find the installation instructions [here](https://www.postgresql.org/download/).

Make sure to install the necessary libraries, set up Redis, and configure PostgreSQL according to the provided links before running the project.

Feel free to customize this section with any additional instructions or information that may be relevant to your project.

## License

This project is licensed under the MIT License. You can find the full text of the license [here](LICENSE).
