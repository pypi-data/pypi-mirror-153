# Authenticator Backup

Tool to backup (and restore) [Google Authenticator](https://play.google.com/store/apps/details?id=com.google.android.apps.authenticator2)
to GPG encrypted files.

**NOTE**: This has only been tested on Linux.  If you find any issues or would
like to share any solutions, [please submit an issue](https://github.com/mikeshultz/authenticator_backup).

## Quickstart

### System Dependencies

You will need to have `opencv` and `gpg` installed on your system for this
package to work.  You should install them before installing this package.  For
instance, on Arch Linux (other distributions may use different package managers
or package names):

    pacman -S opencv gnupg

Install Authenticator Backup:

    pip install --user authenticator_backup

## Backup

You'll need the public key for the PGP account(s) that can decrypt the file (the
recipients).  Each one separated by a space.

    python -m authenticator_backup backup 636ABA5F59810D7D97EF05035B705B8C90A02377 > /tmp/backup.txt

This will open a Window displaying video from  your Web cam to scan the export
QR code with.  To get this code:

1) Open up Google Authenticator
2) Tap the triple-dot in the top right-hand corner
3) Tap "Transfer Accounts"
4) Tap "Export Accounts"
5) Select the accounts you want to backup (probably all of them), and tap "Next"
6) Show this code to your Web cam

The window will close and the encrypted backup will be output once it
successfully captures the QR code.

## Restore

To restore, the recipient GPG account must be on the system to decrypt it.

    cat /tmp/backup.txt | python -m authenticator_backup restore

This will display a QR code yo ucan scan with Google Authenticator to re-import
the accounts.  **DO NOT DISPLAY THIS IN A PUBLIC PLACE**  

1) Open up Google Authenticator
2) Tap the triple-dot in the top right-hand corner
3) Tap "Transfer Accounts"
4) Tap "Import Accounts"
5) Tap "Scan QR code"
6) Scan QR code displayed in the window
6) Close the window when complete

If you had a lot of accounts, multiple windows showing QR code may be displayed,
one after another.
