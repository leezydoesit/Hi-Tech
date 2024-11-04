# Credentials Store
Credentials are the login, password and optionally the stored session (aka cookies)

## Proposed Worfklow
- User start the app
- User is presented with the choice of existing logins and the option to select a new login [^1]
- User selects one of the options
  - Selecting new login will cause a credentials prompt to be shown
  - Selecting existing login will cause the app to
    - Check if a session is stored for the account, if it is use it
      - If the session is not valid, use known username and password
    - If there is no session stored with the login and password, use the login and password
- As the app performs action, it keeps storing the session in the igBot object
- On exit, the app stores the session in the credentials file

## Proposed Storage
- A directory called `Accounts` that stores JSON files
- Each JSON file has the username, password and optionally the session
- Each JSON file must be named `{username}.json`
  - For example, the credentials for Seanny Murphy will be stored in `./Accounts/seannymurphy669.json`
- Each JSON file must have the following structure:
```json
{
  "username": "seannymurphy669",
  "password": "abc123",
  "session": ""
}
```
- Session can be empty


## Notes
[^1]: While a simple account selector is created for this POC, it is expected to have something more robust at launch