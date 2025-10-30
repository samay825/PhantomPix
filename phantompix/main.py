"""
PhantomPix - Advanced Steganography Application
Entry point for the application.

Developed by: Zork
"""
import sys
from PyQt6.QtWidgets import QApplication
from phantompix import PhantomPix


def main():
   
    app = QApplication(sys.argv)
    app.setApplicationName("PhantomPix")
    app.setApplicationVersion("1.0.0")
    app.setStyle('Fusion')
    window = PhantomPix()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()


