import pyotp
from app.dtos.change_password import ChangePasswordDto
from app.dtos.login_dto import LoginDto
from app.dtos.register_dto import RegisterDto
from app.dtos.reset_password import ResetPasswordDto
from app.dtos.update_dto import UpdateDto
from app.models.user import User
from app.repositories.user_repository import UserRepository
from datetime import timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import abort, url_for
from flask_jwt_extended import create_access_token, decode_token, current_user, get_jwt
from flask_sqlalchemy import SQLAlchemy
from injector import inject
from pathlib import Path
import json
import smtplib
from app.schemas.user_profile_schema import UserProfileSchema

class UserServices:
    @inject
    def __init__(
        self,
        register_dto: RegisterDto,
        login_dto: LoginDto,
        repository: UserRepository,
        users_table: User,
        user_profile_schema: UserProfileSchema,
        update_dto: UpdateDto,
        reset_password_dto: ResetPasswordDto,
        change_password_dto: ChangePasswordDto,
        db: SQLAlchemy):
        self.change_password_dto = change_password_dto
        self.reset_password_dto = reset_password_dto
        self.update_dto = update_dto
        self.user_profile_schema = user_profile_schema
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
        if isinstance(log, User):
            self.totp = self.handle_2FA_Send_OTP_Email(log)
            return '2FA'
        return log

    def logout(self):
        # jti = get_jwt()['jti']
        self.repository.logout()
        
    def forgot_password(self, email):
        user = self.repository.get_user_by_email(email)
        if not user.is_activated_account:
            return "not_activated_account"
        if not user:
            abort(404, description='Invalid email')
        reset_token = create_access_token(identity=user.username, expires_delta=timedelta(hours=1), fresh=True)
        reset_link = url_for('user.reset_password', token=reset_token, _external=True)
        email_content = self.create_email(email_type='reset_password', additional_data={'reset_url': reset_link})
        self.send_email(email_content=email_content, receiver_email=user.email)

    def reset_password(self, reset_token, data):
        try:
            decoded_token = decode_token(reset_token)
            user_identity = decoded_token['sub']
        except Exception as ex:
            abort(400, description='Invalid or expired token')
        errors = self.reset_password_dto.validate(data) 
        if errors:
            abort(400, description={'ValidationErrors': errors})
            return
        new_password = self.reset_password_dto.dump(data)['new_password']

        user = self.db.session.query(User).filter_by(username=user_identity).one_or_none()       
        if not user:
            abort(400, description='User not found')
        self.repository.reset_password(user=user, new_password=new_password)

    def change_password(self, data):
        user = current_user
        if not user.is_activated_account:
            return 'not_activated_account'
        errors = self.change_password_dto.validate(data) 
        if errors:
            abort(400, description={'ValidationErrors': errors})
            return
        new_password = self.change_password_dto.dump(data)['new_password']
        self.repository.change_password(user=user, new_password=new_password)

    def enable_2FA(self):
        user = current_user
        if not user.is_activated_account:
            return 'not_activated_account'
        self.repository.enable_2FA(user)
    
    def disable_2FA(self):
        user = current_user        
        if not user.is_activated_account:
            return 'not_activated_account'
        self.repository.disable_2FA(user)        
    
    def handle_2FA_Send_OTP_Email(self, user):
        totp = pyotp.TOTP(user.secret_key, interval=500)
        otp = totp.now()
        email_content = self.create_email(email_type='2FA_OTP', additional_data={'OTP': otp})
        self.send_email(receiver_email=user.email, email_content=email_content)
        return totp

    def handle_2FA_OTP_login(self, username, entered_otp):
        user = self.repository.get_user_by_username(username)
        totp = pyotp.TOTP(user.secret_key, interval=500)
        if not totp.verify(entered_otp):
            abort(401, 'Invalid token')
        token = self.repository.create_user_access_token(user)
        return token
    
    def get_current_user_profile(self):
        user = current_user        
        if not user.is_activated_account:
            return 'not_activated_account'
        user = self.user_profile_schema.dump(user)
        return user
    
    def update_user_data(self, data):
        user = current_user        
        if not user.is_activated_account:
            return 'not_activated_account'
        errors = self.update_dto.validate(data) 
        if errors:
            abort(400, description={'ValidationErrors': errors})
            return
        updated_user = self.update_dto.load(data)
        updated_user = self.repository.update_user_data(user, updated_user)

    def send_activation_code(self):
        user = current_user
        otp = pyotp.TOTP(user.secret_key, interval=500).now()
        email_content = self.create_email(email_type='account_activation', additional_data={'OTP': otp})
        self.send_email(email_content=email_content, receiver_email=current_user.email)
  
    def activate_account(self, entered_otp):
        user = current_user
        totp = pyotp.TOTP(user.secret_key, interval=500)
        if not totp.verify(entered_otp):
            abort(401, 'Invalid token')
            return
        self.repository.activate_account(user)
  
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
        
    def create_email(self, email_type, additional_data=None):
        ####################!###################
        # TODO: To be improved by UI designers #
        ####################!###################
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
        elif email_type == 'account_activation':
            subject = 'SASTify account activation code'
            html = f"""
            <html>
                <body>
                <h1>Here is your account activation code<h1>
                <h3>{additional_data['OTP']}<h3>
                <h5>Don't share it with anyone<h5>
                </body>
            </html>
            """
        return {
            'subject': subject,
            'html': html
        }