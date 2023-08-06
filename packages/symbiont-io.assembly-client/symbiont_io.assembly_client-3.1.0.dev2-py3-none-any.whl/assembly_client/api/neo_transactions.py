import base64
import hashlib
import json
import secrets
import gzip
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

from assembly_client.api.contracts import local_code_from_ref
from typing import Optional


###
### internal helpers for building and signing properly formatted neo transactions
###


def _build_neo_transaction(payload, neo_key, neo_crt):
    """
    takes in a payload built for a particular tx (as dictionary), then handles nonce insertion and final
    assembly
    :return:
    """

    # this is technically part of the payload, but eliminates duplication to add here
    payload["nonce"] = base64.b64encode(secrets.token_bytes(32)).decode("utf-8")

    byte_payload = json.dumps(payload).encode("utf-8")
    signatures = [_make_neo_signature(neo_key, neo_crt, byte_payload)]
    base64_payload = base64.b64encode(byte_payload).decode("utf-8")

    data = {
        "data": base64_payload,
        "signatures": signatures,
    }
    byte_data = json.dumps(data).encode("utf-8")

    return byte_data


def _make_neo_signature(neo_private_key_pem_bytes, neo_cert_pem_bytes, data):
    """
    builds a neo signature for the provided byte data
    """

    if len(neo_private_key_pem_bytes) == 0 or len(neo_cert_pem_bytes) == 0:
        # This is here to support the mock network which doesn't
        # validate any neo signatures.
        signature = {}
    else:
        private_key = serialization.load_pem_private_key(
            neo_private_key_pem_bytes, password=None, backend=default_backend()
        )

        signature = {
            "signature": base64.b16encode(
                private_key.sign(data, ec.ECDSA(hashes.SHA384()))
            ).decode("utf-8"),
            "neo_id": hashlib.sha256(neo_cert_pem_bytes).hexdigest(),
        }

    return signature


###
### public api for signed neo transactions
###


def build_neo_publish_contracts(contract_path, contract_refs, neo_key, neo_crt):

    contracts = [
        {
            "ref": {
                "name": contract_ref.name,
                "version": contract_ref.version_to_use_on_api(),
            },
            "code": base64.b64encode(
                gzip.compress(
                    local_code_from_ref(contract_path, contract_ref).encode("utf-8")
                )
            ).decode("utf-8"),
        }
        for contract_ref in contract_refs
    ]

    payload = {
        "command": "publish contracts",
        "contracts": contracts,
    }

    byte_data = _build_neo_transaction(payload, neo_key, neo_crt)

    return (["neo/contracts"], byte_data)


def build_neo_upgrade_protocol(
    txe_protocol: Optional[int], sympl_version: Optional[int], neo_key, neo_crt
):

    payload = {"command": "upgrade protocol", "version": 1}

    if txe_protocol is not None:
        payload["txe"] = {"version": txe_protocol}

    if sympl_version is not None:
        payload["language"] = {"version": sympl_version}

    byte_data = _build_neo_transaction(payload, neo_key, neo_crt)

    return (["neo/upgrade"], byte_data)
