import pyotp


a = pyotp.parse_uri("otpauth://totp/")

print(a.now())