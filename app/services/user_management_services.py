import pyotp
from app.dtos.login_dto import LoginDto
from app.dtos.register_dto import RegisterDto
from app.models.user import User
from app.repositories.user_management_repository import UserManagementRepository
from datetime import timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import abort, url_for
from flask_jwt_extended import create_access_token, decode_token, current_user
from flask_sqlalchemy import SQLAlchemy
from injector import inject
from pathlib import Path
import json
import smtplib

class UserManagementServices:
    @inject
    def __init__(
        self,
        register_dto: RegisterDto,
        login_dto: LoginDto,
        repository: UserManagementRepository,
        users_table: User,
        db: SQLAlchemy):
        
        self.repository = repository
        self.register_dto = register_dto
        self.login_dto = login_dto
        self.users_table = users_table
        self.db = db
        

    def register(self, data):
        errors = self.register_dto.validate(data)
        
        if errors:
            abort(400, description={'ValidationErrors': errors})
            return
        
        user = self.register_dto.load(data)
        
        self.repository.register(user)
        

    def login(self, data):
        errors = self.login_dto.validate(data)
        
        if errors:
            abort(401, description='Invalid credentials')
            return
        
        user = self.login_dto.load(data)
        log = self.repository.login(user)
        print(log)
        if log:
            self.totp = self.handle_2FA_Send_OTP_Email(log)
            return '2FA'


    def forgot_password(self, email):
        user = self.repository.get_user_by_email(email)
        if not user:
            abort(404, description='Invalid email')

        reset_token = create_access_token(identity=user.username, expires_delta=timedelta(hours=1), fresh=True)
        
        reset_link = url_for('auth.reset_password', token=reset_token, _external=True)
        
        email_content = self.create_email(email_type='reset_password', additional_data={'reset_url': reset_link})
        
        self.send_email(email_content=email_content, receiver_email=user.email)


    def reset_password(self, reset_token, new_password):
        try:
            decoded_token = decode_token(reset_token)
            user_identity = decoded_token['sub']
        except Exception as ex:
            abort(400, description='Invalid or expired token')

        user = self.db.session.query(User).filter_by(username=user_identity).one_or_none()       
        
        if not user:
            abort(400, description='User not found')

        self.repository.reset_password(user=user, new_password=new_password)


    def enable_2FA(self):
        user = current_user
        self.repository.enable_2FA(user)        


    def send_email(self, receiver_email, email_content):
        configs = f'{Path(__file__).resolve().parent.parent}\config.json'
        with open(configs, 'r') as config_file:
            config = json.load(config_file)
        
        smtp_server = config['EMAIL']['SMTP_SERVER']
        port = config['EMAIL']['PORT']
        app_password = config['EMAIL']['APP_PASSWORD']
        sender_email = config['EMAIL']['SENDER']

        
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = email_content['subject']

        msg.attach(MIMEText(email_content['html'], 'html'))
        try:
            server = smtplib.SMTP(smtp_server, port)
            server.starttls()
            server.login(sender_email, app_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        except Exception as e:
            abort(500, description=f'{e}')
        finally:
            server.quit()


    def handle_2FA_Send_OTP_Email(self, user):
        totp = pyotp.TOTP(user.secret_key, interval=500)
        otp = totp.now()
        email_content = self.create_email(email_type='2FA_OTP', additional_data={'OTP': otp})
        self.send_email(receiver_email=user.email, email_content=email_content)
        return totp
        

    def handle_2FA_OTP_login(self, username, entered_otp):
        user = self.repository.get_user_by_username(username)
        totp = pyotp.TOTP(user.secret_key, interval=500)
        print(totp.now())
        if not totp.verify(entered_otp):
            abort(401, 'Invalid token')
        user = self.repository.get_user_by_username(username)
        self.repository.login_with_otp(user)
        
        
    def create_email(self, email_type, additional_data=None):
        html = ''
        subject = ''
        if email_type == 'reset_password':
            subject = 'SASTify password reset'
            html = f"""
            <html>
                <body>
                    <a href="{additional_data['reset_url']}" style="background-color:#800020 ; color: white; padding: 10px 20px; text-decoration: none; border-radius: 100px;">
                        Reset Password
                    </a>
                </body>
            </html>
            """
        elif email_type == '2FA_OTP':
            subject = 'SASTify login OTP'
            html = f"""
            <html>
                <body>
                <h1>Here is your OTP<h1>
                <h3>{additional_data['OTP']}<h3>
                <h5>Don't share it with anyone<h5>
                </body>
            </html>
            """
        return {
            'subject': subject,
            'html': html
        }