import pyotp

secret= 'youssef'
totp = pyotp.TOTP(secret)
otp = totp.now()

print(otp)

totp2 = pyotp.TOTP(secret)
otp2 = totp2.now()
print(otp)
