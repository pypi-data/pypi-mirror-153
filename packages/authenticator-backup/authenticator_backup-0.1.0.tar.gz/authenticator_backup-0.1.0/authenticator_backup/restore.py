import fileinput
from pathlib import Path

import cv2
import gnupg

from authenticator_backup.gui import DisplayCodeWindow, create_window
from authenticator_backup.utils import GPGError


def restore(infile=None, gnupghome=None):
    """Restore accounts to Google Authenticator from an encrypted file.  This
    decypts the backup file, generates a QR code form the payload(s), and opens
    a window to display the QR to be scanned by the app.  Then it uses GnuPG to
    decrypt the payloads.

    :param infile: (:code:`str`) - Path the the encrypted backup file
    :param gnupghome: (:code:`str`) - Home dir for GnuPG (default:
        :code:`$HOME/.gnupg`)
    """
    gpg = gnupg.GPG(gnupghome=gnupghome)
    encoder = cv2.QRCodeEncoder()
    contents = b""

    if infile is not None:
        print(f"Opening {infile}")
        with Path(infile).expanduser().resolve().open() as fp:
            contents = fp.read()
    else:
        contents = "\n".join([line for line in fileinput.input(encoding="utf-8")])

    if not contents:
        raise ValueError("Nothing to decrypt")

    ws = create_window()

    decrypted = gpg.decrypt(contents)

    if not decrypted.ok:
        raise GPGError(decrypted.status or decrypted.stderr)

    decrypted_payloads = decrypted.data.split(b"\n")

    print(f"Decrypted {len(decrypted_payloads)} payloads")

    for payload in decrypted_payloads:
        DisplayCodeWindow(ws, payload)

    ws.mainloop()
