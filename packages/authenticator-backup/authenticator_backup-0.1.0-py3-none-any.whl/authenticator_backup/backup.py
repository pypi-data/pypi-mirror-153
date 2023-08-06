from pathlib import Path

import gnupg

from authenticator_backup.gui import CaptureCodeWindow, create_window
from authenticator_backup.utils import GPGError


def backup(recipients, outfile=None, gnupghome=None):
    """Backup accounts from Google Authenticator to an encrypted file.  This
    opens a window and starts your Web cam to capture the QR code displayed by
    the app.  Then it uses GnuPG to encrypt the payloads.

    :param recipients: (:code:`List[str]`) - List of GPG public keys that can
        decrypt the backup file.
    :param outfile: (:code:`str`) - Path the the encrypted backup file
    :param gnupghome: (:code:`str`) - Home dir for GnuPG (default:
        :code:`$HOME/.gnupg`)
    """
    gpg = gnupg.GPG(gnupghome=gnupghome)

    ws = create_window()
    ws.captured = []
    CaptureCodeWindow(ws)
    ws.mainloop()

    if ws.captured and len(ws.captured) > 0:
        encrypted = gpg.encrypt(b"\n".join(ws.captured), recipients)

        if not encrypted.ok:
            raise GPGError(encrypted.status or encrypted.stderr)

        if outfile:
            with Path(outfile).expanduser().resolve().open("w") as fp:
                fp.write(str(encrypted))
        else:
            print(str(encrypted))
    else:
        print("Nothing to backup")
