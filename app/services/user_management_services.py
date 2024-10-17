from datetime import timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask_jwt_extended import create_access_token
from flask_sqlalchemy import SQLAlchemy
from flask import abort, url_for
from injector import inject
from app.dtos.login_dto import LoginDto
from app.dtos.register_dto import RegisterDto
from app.models.user import User
from app.repositories.user_management_repository import UserManagementRepository
import smtplib
import json

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
        self.repository.login(user)
        


    def forgot_password(self, email):
        user = self.repository.get_user_by_email(email)
        if not user:
            abort(404, description='Invalid email')

        reset_token = create_access_token(identity=user.username, expires_delta=timedelta(hours=1))
        
        reset_link = url_for('auth.reset_password', token=reset_token, _external=True)
        
        email = self.create_email(email=user.email, reset_url=reset_link)
        self.send_email(email)

            

    def create_email(self, email, reset_url):
        with open(r'C:\Main\000\Projects\Graduation_Project\Sastify\app\config.json', 'r') as config_file:
            config = json.load(config_file)
        html = f"""
        <html>
            <body>
                <a href="{reset_url}" style="background-color:#800020 ; color: white; padding: 10px 20px; text-decoration: none; border-radius: 100px;">
                    Reset Password
                </a>
            </body>
        </html>
        """  
        smtp_server = config['EMAIL']['SMTP_SERVER']
        port = config['EMAIL']['PORT']
        app_password = config['EMAIL']['APP_PASSWORD']
        sender_email = config['EMAIL']['SENDER']
        receiver_email = email
        subject = 'SASTify password reset'
        
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        msg.attach(MIMEText(html, 'html'))
        return {
            'smtp_server': smtp_server,
            'subject': subject,
            'receiver_email': receiver_email,
            'sender_email': sender_email,
            'port': port,
            'app_password': app_password,
            'html': html,
            'msg': msg
        }
        
        

    def send_email(self, email):
        try:
            server = smtplib.SMTP(email['smtp_server'], email['port'])
            server.starttls()
            server.login(email['sender_email'], email['app_password'])
            server.sendmail(email['sender_email'], email['receiver_email'], email['msg'].as_string())
        except Exception as e:
            abort(500, description=f'{e}')
        finally:
            server.quit()
