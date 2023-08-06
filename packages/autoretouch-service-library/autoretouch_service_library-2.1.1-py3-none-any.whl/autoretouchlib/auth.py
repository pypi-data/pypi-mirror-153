from typing import Optional
import logging

import google.auth.transport.requests
import google.oauth2.id_token
import google.auth


def get_id_token(url) -> str:
    """"""
    token = get_id_token_from_environment(url) or get_id_token_from_default()
    if token is None:
        raise RuntimeError("could neither fetch id token from metadata server nor from the gcloud auth command "
                           "line. Please make sure that ")
    return token


def get_id_token_from_default() -> Optional[str]:
    try:
        auth_req = google.auth.transport.requests.Request()
        creds, _ = google.auth.default()
        creds.refresh(auth_req) 
        return creds.id_token
    except Exception as e:
        logging.info(f"Could not fetch IdToken from gcloud cli", str(e))
        return None


def get_id_token_from_environment(url: str) -> Optional[str]:
    """when running within a Cloud Run Service"""
    try:
        auth_req = google.auth.transport.requests.Request()
        return google.oauth2.id_token.fetch_id_token(auth_req, url)
    except Exception as e:
        logging.info(f"Could not fetch IdToken for {url} from environment", str(e))
        return None

