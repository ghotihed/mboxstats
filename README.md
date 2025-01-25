This is a simple tool for collecting various statistics about an `mbox` file. It displays the following:

- The size of the file in human form
- The number of messages contained in the file
- The number of _unseen_ messages (i.e., those not yet displayed to the user)
- The number of unread messages (i.e., those not marked as read by the user)
- The number of messages replied to
- The number of messages that have been flagged
- The number of messages in draft mode
- The number of messages that have been deleted

Note that the deleted messages in an `mbox` file will likely not be displayed to the end user in their
mail client. It is not unusual to have a mailbox that appears to be empty, but actually has a number
of messages in their `mbox`, but they're all deleted. This is up to when the IMAP server chooses to
purge the messages.

While processing the file, a progress bar will be displayed so you don't get discouraged when a very large file with tens of thousands of messages gets processed.
