""" TK GUI stuff """
from tkinter import Frame, Label, Tk

import cv2
import qrcode
from PIL import Image, ImageTk
from pyzbar import pyzbar


class CaptureCodeWindow(Frame):
    """Window to capture a QR code via Web cam"""

    def __init__(self, ws):
        """
        :param ws: (:class:`tkinter.Tk`) - Tk instance
        """
        self.ws = ws

        super().__init__(ws)

        self.cap = cv2.VideoCapture(0)

        self.frame = Frame(ws, width=600, height=500)
        self.frame.grid(row=0, column=0, padx=10, pady=2)

        self.img_label = Label(self.frame)
        self.img_label.grid(row=0, column=0)

        self.update()

    def update(self, event=None):
        """Update window with Web cam frame"""
        _, vid_frame = self.cap.read()

        # Look for a QR code and decode it
        detected_code = pyzbar.decode(vid_frame)

        if len(detected_code) > 0:
            # We'll relay data back via the Tk window object
            # TODO: Is there a better technique for these comms?
            self.ws.captured = [x.data for x in detected_code if x.type == "QRCODE"]

            self.cap.release()
            self.ws.quit()

        img = ImageTk.PhotoImage(
            image=Image.fromarray(cv2.cvtColor(vid_frame, cv2.COLOR_BGR2RGB))
        )

        self.img_label.imgtx = img
        self.img_label.configure(image=img)

        self.img_label.after(50, self.update)


class DisplayCodeWindow(Frame):
    """Window to display a generated QR code"""

    def __init__(self, ws, payload):
        """
        :param ws: (:class:`tkinter.Tk`) - Tk instance
        :param payload: (:code:`str`) - QR code payloads (probably
            :code:`otpauth-migration://` URIs)
        """
        self.ws = ws
        self.payload = payload

        super().__init__(ws)

        self.frame = Frame(ws, width=600, height=500)
        self.frame.grid(row=0, column=0, padx=10, pady=2)

        self.qr_label = Label(self.frame)
        self.qr_label.grid(row=0, column=0)

        self.show_code()

    def show_code(self):
        """Show the QR code created using the payload"""
        img = qrcode.make(self.payload)
        gui_image = ImageTk.PhotoImage(img)
        self.qr_label.imgtx = gui_image
        self.qr_label.configure(image=gui_image)


def create_window(title="authenticator_backup"):
    ws = Tk()
    ws.title(title)
    return ws
