## NoShell

Password manager and automation tool for SSH, SCP, etc.

### Installation

**WARNING**: Pre-alpha version. Ongoing development. Local server not using SSL. Database not encrypted. Use at your own risk.

### How it works?

#### Normal approach (ex: SSH)

- Open a terminal and type `ssh <username>@<host>`.
- On Password prompt, enter `<password>`.

#### Problem

Then command is relatively easy, however, if you have a ton of credentials and a bunch of passwords that are not easy to remember, management becomes a mess.
Next solution is to use a password manager. One issue, there is a separate User Interface and you need to switch windows to copy and paste the username, host, password, etc. "one by one".

#### Solution

- Password manager that is integrated to the terminal but being managed in a User-friendly User Interface.

#### How it really works?

- Fire up the terminal and execute `nosh` command. (By the time of this writing, the command does not exist since it is not yet up for production).
- A web-based user interface will pop up. (Using pywebview and Flask)
- User can register/login.
- User can add new credentials.
- To use a credential, just click the "Execute" button.
- The user interface terminates and an expect command is executed.
- You are now SSH'd to your machine and can execute new commands.

### Features

- [ ] User Interface (UI)
    - [X] Login
    - [X] Register
    - [X] Show Credentials
    - [X] Add Credential
    - [ ] Edit Credential
    - [ ] Private Keys
    - [ ] Browse files
- [ ] Execute commands
    - [X] SSH
    - [ ] SCP
    - [ ] FTP
    - [ ] rsync
- [X] Twofish password encryption/decryption
- [ ] Jump Server (Chained Commands)

### Known Issues

- Flask-SocketIO supports `eventlet` but it does not work properly with `concurrent.futures`.

### Libraries Used

- [bcrypt](https://github.com/pyca/bcrypt/)
- [Flask](https://github.com/pallets/flask)
- [Flask-Login](https://github.com/maxcountryman/flask-login)
- [Flask-SocketIO](https://github.com/miguelgrinberg/Flask-SocketIO)
- [Flask-SQLAlchemy](https://github.com/mitsuhiko/flask-sqlalchemy)
- [gevent](https://github.com/gevent/gevent)
- [Pexpect](https://github.com/pexpect/pexpect)
- [pyobjc](https://bitbucket.org/ronaldoussoren/pyobjc)
- [python-twofish](https://github.com/keybase/python-twofish)
- [pywebview](https://github.com/r0x0r/pywebview)
- [socketIO-client](https://github.com/invisibleroads/socketIO-client)

### Author

- [Ronie Martinez](ronmarti18@gmail.com)
