# Developer UI documentation for ProjectTBD

__This document describes the functionality and effects of the user interface, for the purposes of developer documentation. It isn't intended as a manual for end users.__ It doesn't go into the detailed inner workings of the UI, as this is at the time of writing subject to change. However, as the input, output and effects (stored files) have been finalised, this doc can be helpful to any developer in writing code that interacts with the UI (eg. the IgBot class.)

The purpose of the UI is to configure and start the automated Instagram messaging system (aka *IgBot*).

The configuration part is done by the user, who uses the UI to select:

- The *account* that IgBot will log into Instagram with
- The set of *addressees*, users that IgBot will send messages to
- A set of *messages*

The user selects the *account*, *addressees*, and *messages* by clicking on the row in the top 3 listboxes in the UI.

The user also chooses whether *IgBot* should only message an *addressee* if they haven't been messaged from the account before. This is done by checking or unchecking the checkbox next to the `Start` button.

When *addressees* and *messages* are selected by the user, the system automatically matches a randomly selected message from the set to each addressee. *Addressees* can optionally have names as well as usernames (username is Instagram username like `mike@example.com`, name is the addressees name, nickname, etc, eg `Mike`). *Messages* can optionally mention the name, by including `{name}` in the text, eg "Hi, {name} how are you?". The system will prioritise matching named *addressees* with named *messages*. When there is not enough *messages* for each *addressee* to be assigned a unique one, messages will be repeated. *Addressees* that are not named, cannot be assigned named *messages*. If there is no unnamed *message* in the set, but the *addressee* set has unnamed *addressees*, no messages will be assigned to any *addressees* - this highlights that the *message* set can't be used with the *addressee* set.

The user can upload and delete *account*, *addressee* and *message* sets using the buttons under the respective listboxes. The sets have to be either in the CSV or XLSX format.

*Account* sets must two columns, headed `username` and `password`. Both columns are mandatory.

*Addressee* sets must have two columns, headed `username` and `name`. `username` data must always be present. `name` data is optional, but the column heading must still be present.

*Message* sets must have a single column headed `message`.

Please note that the column headings must be exactly as described, with no variations in spelling or casing permitted.

The user can also add a single *account* information by clicking on the `Add` button under the account listbox.

All uploaded data is stored as JSON files in `accounts`, `message_sets` and `addressee_sets` directories in the platorm-appropriate application support folder:

- `~/.config/ProjectTBD/` on Linux
- `~/Library/Application Support/ProjectTBD/` on macOS
- `C:\Users\<username>\AppData\Roaming\ProjectTBD\` on Windows

The listboxes hold:

- one *account* information per row
- one *addressee* __set__ information per row
- one *message* __set__ information per row

The underlying data structure is the `AutomationData` class. This holds the following data:

- the `credentials` that will be used to log into the given instagram account
- the list of message objects, with the addressee username, name (if available) and the text of the message to send them.
- whether *IgBot* should only message previously not-contacted *addressees*.

When the user selects the *account*, the username is displayed in the `Sending from:` label. The label also shows if session information is available for the account, i.e. if the might be logged in automatically or if IgBot will need to attempt login procedure, possibly including 2FA. The account information is added to the instance of `AutomationData`.

When the user selects the *addressees* set only, with no *messages* set being selected, the bottom table will show all *addressees* in the set. Analogically, when the user selects a *messages* set and  no *addressees* set is selected, the bottom table will display all the *messages* in the set.

When both *addressees* and *messages* sets are selected, the bottom table will be populated with the result of *addressee* - *message* matching described above. The data will be also added to the `AutomationData` instance.

When the user clicks on the `Start` button, a new instance of *IgBot* is created and passed the current `AutomationData` instance.
