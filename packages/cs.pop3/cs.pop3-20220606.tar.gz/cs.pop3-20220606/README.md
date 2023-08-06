POP3 stuff, particularly a streaming downloader and a simple command line which runs it.

*Latest release 20220606*:
Minor updates.

I spend some time on a geostationary satellite connection,
where round trip ping times are over 600ms when things are good.

My mail setup involves fetching messages from my inbox
for local storage in my laptop, usually using POP3.
The common standalone tools for this are `fetchmail` and `getmail`.
However, both are very subject to the link latency,
in that they request a message, collect it, issue a delete, then repeat.
On a satellite link that incurs a cost of over a second per message,
making catch up after a period offline a many minutes long exercise in tedium.

This module does something I've been meaning to do for literally years:
a bulk fetch. It issues `RETR`ieves for every message up front as fast as possible.
A separate thread collects the messages as they are delivered
and issues `DELE`tes for the saved messages as soon as each is saved.

This results in a fetch process which is orders of magnitude faster.
Even on a low latency link the throughput is much faster;
on the satellite it is gobsmackingly faster.

## Class `ConnectionSpec(ConnectionSpec, builtins.tuple)`

A specification for a POP3 connection.

*Method `ConnectionSpec.connect(self)`*:
Connect according to this `ConnectionSpec`, return the `socket`.

*Method `ConnectionSpec.from_spec(spec)`*:
Construct an instance from a connection spec string
of the form [`tcp:`|`ssl:`][*user*`@`]*[tcp_host!]server_hostname*[`:`*port*].

The optional prefixes `tcp:` and `ssl:` indicate that the connection
should be cleartext or SSL/TLS respectively.
The default is SSL/TLS.

*Property `ConnectionSpec.netrc_entry`*:
The default `NetrcEntry` for this `ConnectionSpec`.

*Property `ConnectionSpec.password`*:
The password for this connection, obtained from the `.netrc` file
via the key *user*`@`*host*`:`*port*.

## Function `main(argv=None)`

The `pop3` command line mode.

## Class `NetrcEntry(NetrcEntry, builtins.tuple)`

A `namedtuple` representation of a `netrc` entry.

*Method `NetrcEntry.by_account(account_name, netrc_hosts=None)`*:
Look up an entry by the `account` field value.

*Method `NetrcEntry.get(machine, netrc_hosts=None)`*:
Look up an entry by the `machine` field value.

## Class `POP3(cs.resources.MultiOpenMixin, cs.context.ContextManagerMixin)`

Simple POP3 class with support for streaming use.

*Method `POP3.client_auth(self, user, password)`*:
Perform a client authentication.

*Method `POP3.client_begin(self)`*:
Read the opening server response.

*Method `POP3.client_bg(self, rq_line, is_multiline=False, notify=None)`*:
Dispatch a request `rq_line` in the background.
Return a `Result` to collect the request result.

Parameters:
* `rq_line`: POP3 request text, without any terminating CRLF
* `is_multiline`: true if a multiline response is expected,
  default `False`
* `notify`: a optional handler for `Result.notify`,
  applied if not `None`

*Note*: DOES NOT flush the send stream.
Call `self.flush()` when a batch of requests has been submitted,
before trying to collect the `Result`s.

The `Result` will receive `[etc,lines]` on success
where:
* `etc` is the trailing portion of an ok response line
* `lines` is a list of unstuffed text lines from the response
  if `is_multiline` is true, `None` otherwise
The `Result` gets a list instead of a tuple
so that a handler may clear it in order to release memory.

Example:

    R = self.client_bg(f'RETR {msg_n}', is_multiline=True, notify=notify)

*Method `POP3.client_dele_bg(self, msg_n)`*:
Queue a delete request for message `msg_n`,
return ` Result` for collection.

*Method `POP3.client_quit_bg(self)`*:
Queue a QUIT request.
return ` Result` for collection.

*Method `POP3.client_retr_bg(self, msg_n, notify=None)`*:
Queue a retrieve request for message `msg_n`,
return ` Result` for collection.

If `notify` is not `None`, apply it to the `Result`.

*Method `POP3.client_uidl(self)`*:
Return a mapping of message number to message UID string.

*Method `POP3.dl_bg(self, msg_n, maildir, deleRs)`*:
Download message `msg_n` to Maildir `maildir`.
Return the `Result` for the `RETR` request.

After a successful save,
queue a `DELE` for the message
and add its `Result` to `deleRs`.

*Method `POP3.flush(self)`*:
Flush the send stream.

*Method `POP3.get_multiline(self)`*:
Generator yielding unstuffed lines from a multiline response.

*Method `POP3.get_ok(self)`*:
Read server response, require it to be `'OK+'`.
Returns the `etc` part.

*Method `POP3.get_response(self)`*:
Read a server response.
Return `(ok,status,etc)`
where `ok` is true if `status` is `'+OK'`, false otherwise;
`status` is the status word
and `etc` is the following text.
Return `(None,None,None)` on EOF from the receive stream.

*Method `POP3.readline(self)`*:
Read a CRLF terminated line from `self.recvf`.
Return the text preceeding the CRLF.
Return `None` at EOF.

*Method `POP3.readlines(self)`*:
Generator yielding lines from `self.recf`.

*Method `POP3.sendline(self, line, do_flush=False)`*:
Send a line (excluding its terminating CRLF).
If `do_flush` is true (default `False`)
also flush the sending stream.

*Method `POP3.shutdown(*a, **kw)`*:
Quit and disconnect.

*Method `POP3.startup(*a, **kw)`*:
Connect to the server and log in.

## Class `POP3Command(cs.cmdutils.BaseCommand)`

Command line implementation for POP3 operations.

Credentials are obtained via the `.netrc` file presently.

Connection specifications consist of an optional leading mode prefix
followed by a netrc(5) account name
or an explicit connection specification
from which to derive:
* `user`: the user name to log in as
* `tcp_host`: the hostname to which to establish a TCP connection
* `port`: the TCP port to connect on, default 995 for TLS/SSL or 110 for cleartext
* `sni_host`: the TLS/SSL SNI server name, which may be different from the `tcp_host`

The optional mode prefix is one of:
* `ssl:`: use TLS/SSL - this is the default
* `tcp:`: use cleartext - this is useful for ssh port forwards
  to some not-publicly-exposed clear text POP service;
  in particular streaming performs better this way,
  I think because the Python SSL layer does not buffer writes

Example connection specifications:
* `username@mail.example.com`:
  use TLS/SSL to connect to the POP3S service at `mail.example.com`,
  logging in as `username`
* `mail.example.com`:
  use TLS/SSL to connect to the POP3S service at `mail.example.com`,
  logging in with the same login as the local effective user
* `tcp:username@localhost:1110`:
  use cleartext to connect to `localhost:1110`,
  typically an ssh port forward to a remote private cleartext POP service,
  logging in as `username`
* `username@localhost!mail.example.com:1995`:
  use TLS/SSL to connect to `localhost:1995`,
  usually an ssh port forward to a remote private TLS/SSL POP service,
  logging in as `username` and passing `mail.exampl.com`
  as the TLS/SSL server name indication
  (which allows certificate verification to proceed correctly)

Note that the specification may also be a `netrc` account name.
If the specification matches such an account name
then values are derived from the `netrc` entry.
The entry's `machine` name becomes the TCP connection specification,
the entry's `login` provides a default for the username,
the entry's `account` host part provides the `sni_host`.

Example `netrc` entry:

    machine username@localhost:1110
      account username@mail.example.com
      password ************

Such an entry allows you to use the specification `tcp:username@mail.example.com`
and obtain the remaining detail via the `netrc` entry.

Command line usage:

    Usage: pop3 subcommand [...]
      Subcommands:
        dl [{ssl,tcp}:]{netrc_account|[user@]host[!sni_name][:port]} maildir
        help [-l] [subcommand-names...]
          Print the full help for the named subcommands,
          or for all subcommands if no names are specified.
          -l  Long help even if no subcommand-names provided.

*Method `POP3Command.cmd_dl(self, argv)`*:
Collect messages from a POP3 server and deliver to a Maildir.

Usage: {cmd} [{{ssl,tcp}}:]{{netrc_account|[user@]host[!sni_name][:port]}} maildir

# Release Log



*Release 20220606*:
Minor updates.

*Release 20220312*:
Make POP3Command.cmd_dl an instance method (static methods broke with the latest cs.cmdutils release).

*Release 20211208*:
* POP3.startup: do not start the worker queue until authenticated.
* POP3.get_response: return (None,None,None) at EOF.
* POP3.shutdown: catch exceptions from client QUIT.

*Release 20210407.2*:
Provide "pop3" console_script.

*Release 20210407.1*:
Bump for cs.cmdutils minor bugfix, also fix a few docstring typos.

*Release 20210407*:
Initial PyPI release.
