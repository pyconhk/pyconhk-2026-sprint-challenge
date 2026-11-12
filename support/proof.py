"""Turn a Sprint report and contact details into one encrypted string."""

from base64 import b64encode
from os import urandom
from pathlib import Path

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from pydantic import BaseModel, ConfigDict, Field

from .challenge import normalise_login

GAME_SEED = "pycon-hk-sprint-2026"
PROOF_CONTEXT = b"pyconhk-2026-sprint-proof-v3"
NONCE_BYTES = 12
SUPPORT = Path(__file__).resolve().parent


class ContactDetails(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, str_strip_whitespace=True)

    first_name: str = Field(
        min_length=1, max_length=100, pattern=r"^[^\x00-\x1f\x7f]+$"
    )
    last_name: str = Field(min_length=1, max_length=100, pattern=r"^[^\x00-\x1f\x7f]+$")
    email: str = Field(max_length=254, pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class Submission(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    login: str
    answer_digest: str = Field(pattern=r"^[0-9a-f]{64}$")
    contact: ContactDetails


def wrapping_padding() -> padding.OAEP:
    return padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=PROOF_CONTEXT,
    )


def write_proof(login: str, digest: str, contact: ContactDetails) -> Path:
    submission = Submission(
        login=normalise_login(login), answer_digest=digest, contact=contact
    )
    public_key = serialization.load_pem_public_key(
        (SUPPORT / "public.pem").read_bytes()
    )
    if not isinstance(public_key, rsa.RSAPublicKey):
        raise ValueError("The organizer public key must be RSA.")

    key = AESGCM.generate_key(bit_length=256)
    nonce = urandom(NONCE_BYTES)
    ciphertext = AESGCM(key).encrypt(
        nonce, submission.model_dump_json().encode(), PROOF_CONTEXT
    )
    wrapped_key = public_key.encrypt(key, wrapping_padding())
    output = SUPPORT.parent / "tickets" / f"{submission.login}.txt"
    output.write_bytes(b64encode(wrapped_key + nonce + ciphertext) + b"\n")
    return output
