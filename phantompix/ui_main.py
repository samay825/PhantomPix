"""
Developed by: Zork
"""
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QTextEdit, QLineEdit, QLabel, 
                             QFileDialog, QMessageBox, QStatusBar, QGroupBox,
                             QGraphicsDropShadowEffect, QProgressBar, QCheckBox,
                             QFrame, QSizePolicy)
from PyQt6.QtCore import (Qt, QPropertyAnimation, QEasingCurve, QPoint, QSize, 
                         pyqtProperty, QTimer, QParallelAnimationGroup, QSequentialAnimationGroup)
from PyQt6.QtGui import QPixmap, QFont, QColor, QPalette, QIcon, QCursor
import os
from .encryptor import MessageEncryptor
from .steganography import ImageSteganography


class AnimatedButton(QPushButton):
    
    
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self._glow_intensity = 0
        self._is_processing = False
        self.setup_effects()
    
    def setup_effects(self):
        
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(20)
        self.shadow.setColor(QColor(0, 0, 0, 160))
        self.shadow.setOffset(0, 4)
        self.setGraphicsEffect(self.shadow)
    
    def enterEvent(self, event):
        
        if not self._is_processing:
            self.animate_glow(35)
            self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        
        if not self._is_processing:
            self.animate_glow(20)
        super().leaveEvent(event)
    
    def animate_glow(self, target_blur):
        
        self.anim = QPropertyAnimation(self.shadow, b"blurRadius")
        self.anim.setDuration(250)
        self.anim.setStartValue(self.shadow.blurRadius())
        self.anim.setEndValue(target_blur)
        self.anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.anim.start()
    
    def set_processing(self, processing):
        
        self._is_processing = processing
        self.setEnabled(not processing)


class PhantomPix(QMainWindow):
    
    
    def __init__(self):
        super().__init__()
        self.selected_image_path = None
        self.show_password = False
        self.setup_dark_theme()
        self.init_ui()
        self.setup_animations()
        self.show_welcome_animation()
    
    def setup_dark_theme(self):
        
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0f0c29, stop:0.5 #302b63, stop:1 #24243e);
            }
            QWidget {
                color: #e0e0e0;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QGroupBox {
                background: rgba(255, 255, 255, 0.05);
                border: 2px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                margin-top: 12px;
                padding: 12px;
                font-size: 12px;
                font-weight: bold;
                color: #00d4ff;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 4px 12px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 6px;
                color: white;
            }
            QTextEdit, QLineEdit {
                background: rgba(255, 255, 255, 0.08);
                border: 2px solid rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                padding: 12px;
                color: #ffffff;
                font-size: 13px;
                selection-background-color: #667eea;
            }
            QTextEdit:focus, QLineEdit:focus {
                border: 2px solid #00d4ff;
                background: rgba(255, 255, 255, 0.12);
            }
            QLabel {
                color: #e0e0e0;
            }
            QStatusBar {
                background: rgba(0, 0, 0, 0.3);
                color: #00d4ff;
                font-weight: bold;
            }
        """)
    
    def init_ui(self):
        
        self.setWindowTitle("👻 PhantomPix - Steganography Tool")
        self.setGeometry(100, 100, 750, 680)
        self.setMinimumSize(650, 600)
        
        # Set window icon
        icon_path = os.path.join(os.path.dirname(__file__), 'python.png')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(15, 10, 15, 10)
        main_layout.setSpacing(10)
        
        
        title = QLabel("👻 PHANTOMPIX")
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title_font.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 2)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00d4ff, stop:0.5 #667eea, stop:1 #f093fb);
                padding: 10px;
            }
        """)
        
        
        title_shadow = QGraphicsDropShadowEffect()
        title_shadow.setBlurRadius(25)
        title_shadow.setColor(QColor(0, 212, 255, 160))
        title_shadow.setOffset(0, 0)
        title.setGraphicsEffect(title_shadow)
        main_layout.addWidget(title)
        
        
        subtitle = QLabel("🛡️ Hide Messages in Plain Sight • Military-Grade Encryption")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("""
            color: #a0a0a0;
            font-size: 10px;
            margin-bottom: 5px;
            letter-spacing: 0.5px;
        """)
        main_layout.addWidget(subtitle)
        
        
        image_group = QGroupBox("📸 Cover Image")
        image_group_layout = QVBoxLayout()
        image_group_layout.setSpacing(10)
        image_group_layout.setContentsMargins(10, 25, 10, 10)
        
        
        image_container = QWidget()
        image_container.setFixedHeight(110)
        image_container_layout = QVBoxLayout(image_container)
        image_container_layout.setContentsMargins(0, 0, 0, 0)
        
        
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setFixedHeight(110)
        self.image_label.setText("📷 No Image Selected")
        self.image_label.setWordWrap(True)
        
        
        self.empty_image_style = """
            border: 2px dashed rgba(0, 212, 255, 0.4);
            background: rgba(0, 0, 0, 0.3);
            border-radius: 10px;
            color: #00d4ff;
            font-size: 12px;
            font-weight: bold;
        """
        
        
        self.loaded_image_style = """
            border: 2px solid rgba(0, 212, 255, 0.6);
            background: rgba(0, 0, 0, 0.5);
            border-radius: 10px;
        """
        
        self.image_label.setStyleSheet(self.empty_image_style)
        image_container_layout.addWidget(self.image_label)
        image_group_layout.addWidget(image_container)
        
        
        self.select_btn = AnimatedButton("📁 BROWSE IMAGE")
        self.select_btn.clicked.connect(self.select_image)
        self.select_btn.setFixedHeight(38)
        self.select_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.select_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 12px;
                font-weight: bold;
                letter-spacing: 1px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #764ba2, stop:1 #667eea);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5a3d7a, stop:1 #4a5fc1);
            }
        """)
        image_group_layout.addWidget(self.select_btn)
        
        image_group.setLayout(image_group_layout)
        main_layout.addWidget(image_group)
        
        
        message_group = QGroupBox("Secret Message")
        message_layout = QVBoxLayout()
        message_layout.setContentsMargins(8, 20, 8, 8)  # Extra top margin for title
        
        self.message_text = QTextEdit()
        self.message_text.setPlaceholderText("✍️ Type your secret message here...")
        self.message_text.setFixedHeight(85)  # Fixed height
        self.message_text.setStyleSheet("""
            QTextEdit {
                background: rgba(0, 0, 0, 0.4);
                border: 2px solid rgba(102, 126, 234, 0.3);
                border-radius: 10px;
                padding: 10px;
                color: #ffffff;
                font-size: 12px;
                line-height: 1.4;
            }
            QTextEdit:focus {
                border: 2px solid #667eea;
                background: rgba(0, 0, 0, 0.5);
            }
        """)
        message_layout.addWidget(self.message_text)
        
        message_group.setLayout(message_layout)
        main_layout.addWidget(message_group)
        
        
        password_group = QGroupBox("Password")
        password_layout = QVBoxLayout()
        password_layout.setSpacing(6)
        password_layout.setContentsMargins(8, 20, 8, 8)  # Extra top margin for title
        
        password_label = QLabel("🔑 Master Password")
        password_label.setStyleSheet("color: #00d4ff; font-weight: bold; font-size: 11px;")
        password_layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("🔐 Enter password (min 6 chars)...")
        self.password_input.setFixedHeight(36)
        self.password_input.textChanged.connect(self.update_password_strength)
        self.password_input.setStyleSheet("""
            QLineEdit {
                background: rgba(0, 0, 0, 0.4);
                border: 2px solid rgba(240, 147, 251, 0.3);
                border-radius: 10px;
                padding: 8px 12px;
                color: #ffffff;
                font-size: 12px;
                letter-spacing: 1.5px;
            }
            QLineEdit:focus {
                border: 2px solid #f093fb;
                background: rgba(0, 0, 0, 0.5);
            }
        """)
        password_layout.addWidget(self.password_input)
        
        password_group.setLayout(password_layout)
        main_layout.addWidget(password_group)
        
        
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        self.encode_btn = AnimatedButton("🔐 ENCODE")
        self.encode_btn.clicked.connect(self.encode_message)
        self.encode_btn.setFixedHeight(45)
        self.encode_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.encode_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #11998e, stop:1 #38ef7d);
                color: white;
                border: none;
                border-radius: 12px;
                font-size: 13px;
                font-weight: bold;
                letter-spacing: 1.5px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #38ef7d, stop:1 #11998e);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0d7a6f, stop:1 #2bc963);
            }
        """)
        button_layout.addWidget(self.encode_btn)
        
        self.decode_btn = AnimatedButton("🔓 DECODE")
        self.decode_btn.clicked.connect(self.decode_message)
        self.decode_btn.setFixedHeight(45)
        self.decode_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.decode_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #fc466b, stop:1 #3f5efb);
                color: white;
                border: none;
                border-radius: 12px;
                font-size: 13px;
                font-weight: bold;
                letter-spacing: 1.5px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3f5efb, stop:1 #fc466b);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2d43b8, stop:1 #c93551);
            }
        """)
        button_layout.addWidget(self.decode_btn)
        
        main_layout.addLayout(button_layout)
        
        
        options_layout = QHBoxLayout()
        options_layout.setSpacing(15)
        
        
        self.show_password_check = QCheckBox("👁️ Show Password")
        self.show_password_check.stateChanged.connect(self.toggle_password_visibility)
        self.show_password_check.setStyleSheet("""
            QCheckBox {
                color: #a0a0a0;
                font-size: 10px;
                spacing: 5px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border-radius: 4px;
                border: 2px solid rgba(0, 212, 255, 0.4);
                background: rgba(0, 0, 0, 0.3);
            }
            QCheckBox::indicator:checked {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                border: 2px solid #00d4ff;
            }
            QCheckBox::indicator:hover {
                border: 2px solid #00d4ff;
            }
        """)
        options_layout.addWidget(self.show_password_check)
        
        
        self.strength_label = QLabel("🔒 Strength: None")
        self.strength_label.setStyleSheet("""
            color: #888;
            font-size: 10px;
            font-weight: bold;
        """)
        options_layout.addWidget(self.strength_label)
        
        options_layout.addStretch()
        main_layout.addLayout(options_layout)
        
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(4)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background: rgba(0, 0, 0, 0.3);
                border: none;
                border-radius: 2px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:0.5 #00d4ff, stop:1 #f093fb);
                border-radius: 2px;
            }
        """)
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)
        
        
        footer = QLabel("💡 PNG format recommended • AES-256 encryption • Zero-knowledge security")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setStyleSheet("""
            color: rgba(255, 255, 255, 0.3);
            font-size: 9px;
            padding: 5px;
            margin-top: 2px;
        """)
        main_layout.addWidget(footer)
        
        
        credit = QLabel("⚡ Developed by Zork")
        credit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        credit.setStyleSheet("""
            QLabel {
                color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #f093fb);
                font-size: 10px;
                font-weight: bold;
                padding: 3px;
                margin-top: 0px;
            }
        """)
        
        
        credit_shadow = QGraphicsDropShadowEffect()
        credit_shadow.setBlurRadius(15)
        credit_shadow.setColor(QColor(102, 126, 234, 100))
        credit_shadow.setOffset(0, 0)
        credit.setGraphicsEffect(credit_shadow)
        main_layout.addWidget(credit)
        
        
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.setStyleSheet("""
            QStatusBar {
                background: rgba(0, 0, 0, 0.5);
                color: #00d4ff;
                font-weight: bold;
                border-top: 1px solid rgba(0, 212, 255, 0.3);
                padding: 5px;
            }
        """)
        self.status_bar.showMessage("⚡ Ready • Waiting for input...")
    
    def setup_animations(self):
        
        self.setWindowOpacity(0.0)
        self.fade_in = QPropertyAnimation(self, b"windowOpacity")
        self.fade_in.setDuration(600)
        self.fade_in.setStartValue(0.0)
        self.fade_in.setEndValue(1.0)
        self.fade_in.setEasingCurve(QEasingCurve.Type.OutCubic)
    
    def show_welcome_animation(self):
        
        QTimer.singleShot(100, self.fade_in.start)
    
    def toggle_password_visibility(self, state):
        
        if state == Qt.CheckState.Checked.value:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
    
    def update_password_strength(self, password):
        
        if not password:
            self.strength_label.setText("🔒 Strength: None")
            self.strength_label.setStyleSheet("color: #888; font-size: 10px; font-weight: bold;")
            return
        
        strength = 0
        if len(password) >= 6:
            strength += 1
        if len(password) >= 10:
            strength += 1
        if any(c.isupper() for c in password):
            strength += 1
        if any(c.isdigit() for c in password):
            strength += 1
        if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            strength += 1
        
        if strength <= 1:
            self.strength_label.setText("🔴 Strength: Weak")
            self.strength_label.setStyleSheet("color: #ff4444; font-size: 10px; font-weight: bold;")
        elif strength <= 3:
            self.strength_label.setText("🟡 Strength: Medium")
            self.strength_label.setStyleSheet("color: #ffaa00; font-size: 10px; font-weight: bold;")
        else:
            self.strength_label.setText("🟢 Strength: Strong")
            self.strength_label.setStyleSheet("color: #00ff88; font-size: 10px; font-weight: bold;")
    
    def show_progress(self, message):
        
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate
        self.status_bar.showMessage(message)
        self.encode_btn.set_processing(True)
        self.decode_btn.set_processing(True)
    
    def hide_progress(self):
        
        self.progress_bar.setVisible(False)
        self.encode_btn.set_processing(False)
        self.decode_btn.set_processing(False)
    
    def select_image(self):
        
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Cover Image",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp);;All Files (*.*)"
        )
        
        if file_path:
            self.selected_image_path = file_path
            self.display_image_preview(file_path)
            self.status_bar.showMessage(f"✅ Image loaded: {os.path.basename(file_path)}")
    
    def display_image_preview(self, file_path):
        
        try:
            pixmap = QPixmap(file_path)
            
            if pixmap.isNull():
                self.image_label.setText("❌ Invalid Image")
                return
            
            
            label_width = self.image_label.width() - 20
            label_height = self.image_label.height() - 20
            
            scaled_pixmap = pixmap.scaled(
                label_width,
                label_height,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            
            
            self.image_label.setText("")
            self.image_label.setPixmap(scaled_pixmap)
            self.image_label.setStyleSheet(self.loaded_image_style)
            
           
            glow = QGraphicsDropShadowEffect()
            glow.setBlurRadius(18)
            glow.setColor(QColor(0, 212, 255, 90))
            glow.setOffset(0, 0)
            self.image_label.setGraphicsEffect(glow)
            
        except Exception as e:
            self.image_label.setText(f"❌ Error loading image")
            self.image_label.setStyleSheet(self.empty_image_style)
    
    def encode_message(self):
        
        
        if not self.selected_image_path:
            self.show_styled_warning("No Image Selected", "Please select an image first to hide your message.")
            return
        
        message = self.message_text.toPlainText().strip()
        if not message:
            self.show_styled_warning("No Message", "Please enter a secret message to encode.")
            return
        
        password = self.password_input.text()
        if not password:
            self.show_styled_warning("No Password", "Please enter a password to encrypt your message.")
            return
        
        if len(password) < 6:
            self.show_styled_warning("Weak Password", "Password should be at least 6 characters long for security.")
            return
        
        try:
            
            output_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save Encoded Image",
                "encoded_image.png",
                "PNG Image (*.png)"
            )
            
            if not output_path:
                return
            
            self.show_progress("🔄 Encrypting and encoding message...")
            
            
            QTimer.singleShot(100, lambda: self._perform_encoding(message, password, output_path))
            
        except Exception as e:
            self.hide_progress()
            self.status_bar.showMessage("❌ Encoding failed")
            msg = QMessageBox(self)
            msg.setWindowTitle("❌ Error")
            msg.setText("Encoding Failed")
            msg.setInformativeText(f"Failed to encode message:\n{str(e)}")
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setStyleSheet(self.get_messagebox_style())
            msg.exec()
    
    def _perform_encoding(self, message, password, output_path):
        
        try:
            
            encrypted_data = MessageEncryptor.encrypt_message(message, password, compress=True)
            
            
            ImageSteganography.encode_message(self.selected_image_path, encrypted_data, output_path)
            
            self.hide_progress()
            self.status_bar.showMessage("✅ Message encoded successfully!")
            
            
            msg = QMessageBox(self)
            msg.setWindowTitle("🎉 Success")
            msg.setText("Message Successfully Encoded!")
            msg.setInformativeText(f"Your encrypted message is now hidden inside:\n{os.path.basename(output_path)}\n\n🔐 Keep your password safe!")
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setStyleSheet(self.get_messagebox_style())
            msg.exec()
        except Exception as e:
            self.hide_progress()
            self.status_bar.showMessage("❌ Encoding failed")
            msg = QMessageBox(self)
            msg.setWindowTitle("❌ Error")
            msg.setText("Encoding Failed")
            msg.setInformativeText(f"Failed to encode message:\n{str(e)}")
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setStyleSheet(self.get_messagebox_style())
            msg.exec()
    
    def decode_message(self):
        
        
        if not self.selected_image_path:
            self.show_styled_warning("No Image Selected", "Please select an encoded image to decode.")
            return
        
        password = self.password_input.text()
        if not password:
            self.show_styled_warning("No Password", "Please enter the password used during encoding.")
            return
        
        try:
            self.show_progress("🔄 Decoding and decrypting message...")
            
            
            QTimer.singleShot(100, lambda: self._perform_decoding(password))
            
        except Exception as e:
            self.hide_progress()
            self.status_bar.showMessage("❌ Decoding failed")
            msg = QMessageBox(self)
            msg.setWindowTitle("🔒 Decoding Failed")
            msg.setText("Failed to Decode Message")
            msg.setInformativeText(
                f"{str(e)}\n\n"
                "Possible reasons:\n"
                "• Wrong password\n"
                "• Image doesn't contain encoded data\n"
                "• Image has been modified or corrupted"
            )
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setStyleSheet(self.get_messagebox_style())
            msg.exec()
    
    def _perform_decoding(self, password):
        
        try:
            
            encrypted_data = ImageSteganography.decode_message(self.selected_image_path)
            
           
            decrypted_message = MessageEncryptor.decrypt_message(encrypted_data, password, compressed=True)
            
            
            self.message_text.setPlainText(decrypted_message)
            
            self.hide_progress()
            self.status_bar.showMessage("✅ Message decoded successfully!")
            
            
            msg = QMessageBox(self)
            msg.setWindowTitle("🎉 Success")
            msg.setText("Message Successfully Decoded!")
            msg.setInformativeText("Your secret message has been revealed and displayed in the text area.")
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setStyleSheet(self.get_messagebox_style())
            msg.exec()
        except Exception as e:
            self.hide_progress()
            self.status_bar.showMessage("❌ Decoding failed")
            msg = QMessageBox(self)
            msg.setWindowTitle("🔒 Decoding Failed")
            msg.setText("Failed to Decode Message")
            msg.setInformativeText(
                f"{str(e)}\n\n"
                "Possible reasons:\n"
                "• Wrong password\n"
                "• Image doesn't contain encoded data\n"
                "• Image has been modified or corrupted"
            )
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setStyleSheet(self.get_messagebox_style())
            msg.exec()
    
    def show_styled_warning(self, title, message):
        
        msg = QMessageBox(self)
        msg.setWindowTitle(f"⚠️ {title}")
        msg.setText(title)
        msg.setInformativeText(message)
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setStyleSheet(self.get_messagebox_style())
        msg.exec()
    
    def get_messagebox_style(self):
        
        return """
            QMessageBox {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1a1a2e, stop:1 #16213e);
                color: #ffffff;
            }
            QMessageBox QLabel {
                color: #ffffff;
                font-size: 13px;
            }
            QMessageBox QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 20px;
                font-weight: bold;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #764ba2, stop:1 #667eea);
            }
        """
