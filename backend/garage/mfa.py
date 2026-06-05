import base64
import io

import pyotp
import qrcode
from django.core import signing

MFA_PENDING_SALT = 'riflet-admin-mfa-pending'
MFA_PENDING_MAX_AGE = 600
MFA_ISSUER = 'Riflet Automobile'


def create_pending_token(user_id: int) -> str:
    return signing.TimestampSigner(salt=MFA_PENDING_SALT).sign(str(user_id))


def verify_pending_token(token: str) -> int:
    user_id = signing.TimestampSigner(salt=MFA_PENDING_SALT).unsign(
        token,
        max_age=MFA_PENDING_MAX_AGE,
    )
    return int(user_id)


def generate_totp_secret() -> str:
    return pyotp.random_base32()


def get_totp_uri(secret: str, username: str, issuer: str = MFA_ISSUER) -> str:
    return pyotp.TOTP(secret).provisioning_uri(name=username, issuer_name=issuer)


def generate_qr_base64(otpauth_url: str) -> str:
    image = qrcode.make(otpauth_url)
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    encoded = base64.b64encode(buffer.getvalue()).decode('ascii')
    return f'data:image/png;base64,{encoded}'


def verify_totp(secret: str, code: str) -> bool:
    if not secret or not code:
        return False
    normalized = str(code).strip().replace(' ', '')
    if not normalized.isdigit() or len(normalized) != 6:
        return False
    return pyotp.TOTP(secret).verify(normalized, valid_window=1)
