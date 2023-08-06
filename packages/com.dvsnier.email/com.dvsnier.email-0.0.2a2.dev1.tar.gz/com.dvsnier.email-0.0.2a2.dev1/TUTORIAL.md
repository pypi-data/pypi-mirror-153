# Tutorial

- [一. Introduce](#一-introduce)
- [二. Configuration](#二-configuration)
- [三. Usage](#三-usage)
- [四. History](#四-history)

## 一. Introduce

this is a simple email execution program, only a single email address can be mailed.

## 二. Configuration

We recommend using the user profile method to define:

```bash
~/.dvsrc
```

the `.dvsrc` configuration items are as follows:

```bash
##################### SERVER REGION ########################
# the setup server
mail_host = smtp.xx.com
# the Server SSL default port
mail_port = 465
##################### SENDER REGION ########################
# the user name
mail_user = xxx
# the secret key with password or token
mail_passwd = passwd_or_token
# the sender
mail_sender = xxx@xx.com
# the sender alias
sender_alias = xxx
################### RECIPIENT REGION #######################
# the recipient
mail_receiver = yyy@yy.com
# the recipient alias
receiver_alias = yyy
```

of course, you can also specify the configuration file, for specific usage, refer to the following section.

## 三. Usage

```bash
usage: dvs-email [-h] [-V] [-v] [-cfg config-file] [-mr mail-receiver] [-ra receiver-alias] [-f] [-s subject]
                 [-msg message [message ...] | -mf message-file]

this is a simple email execution program, only a single email address can be mailed.

optional arguments:
  -h, --help            show this help message and exit
  -V, --version         the show version and exit.
  -v, --verbose         if true, prepare to output detailed journal records, otherwise no.
  -cfg config-file, --config-file config-file
                        the current mail configuration file.
  -mr mail-receiver, --mail-receiver mail-receiver
                        the current mail recipient.
  -ra receiver-alias, --receiver-alias receiver-alias
                        the current mail recipient alias.
  -f, --mode-flag       if flags == true, email program is ssl mode, otherwise no, and the default value is True.
  -s subject, --subject subject
                        the current email subject and the default value is None when It is recommended that users fill in the email
                        subject by themselves.
  -msg message [message ...], --message message [message ...]
                        the current email message and the default value is None.
  -mf message-file, --message-file message-file
                        the current email message file.

the copyright belongs to DovSnier that reserve the right of final interpretation.
```

## 四. History

- [History](./HISTORY.md)
