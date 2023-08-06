# Pretix verify mails against ldap
This is a pretix plugin that can be used to verify the user provided mails
against an ldap server. This does not verify the users password.<br>
WARNING: This does verify that the user registering is the owner of the mail address.

## Usage
1. Install 
2. Configure in admin settings
3. Enable the plugin for your event.

## Security Conserns
### Query
While we use a function of `python-ldap` to sanitize user input there might still be a possible exploit by inserting
custom code into the ldap query. You should definitely use a read only user for ldap. User data should not be exposed 
as we do not print user data to the end user.

### Brutforcing
Via a brutforcing attack this opens up the user to find valid mail adresses in your ldap. This is not different to a
password reset feature telling you that it has (not) found an mail address. 