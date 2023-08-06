import logging
import time
import requests
import os
import beeline

from beeline.trace import marshal_trace_context
from assembly_client.api.util.json import dumps, loads
from assembly_client.api.types.error_types import BaseContractError, ContractError
from assembly_client.api.job_management import Job


logger = logging.getLogger(__name__)

# this file provides the core infrastructure for making api calls against a symbiont assembly node,
# including basic session management and caching of events.

# this is the error message provided by txe when it encounters and error
# not associated with any error type
ASYNC_CALL_FAILED = "Async call failed"


class NodeSession:
    """
    all state related to existing sessions with a node
    """

    def __init__(
        self,
        hostname,
        node_fqdn,
        admin_certs=None,
        client_certs=None,
        tracer=None,
    ):
        self.node_fqdn = node_fqdn
        self.hostname = hostname
        self.admin_certs = admin_certs
        self.client_certs = client_certs
        self.recreate_http_sessions()
        self.event_cache = EventCache()
        self.tracer = tracer

    def init_session(self, certs):
        session = requests.Session()
        session.cert = certs
        session.verify = True
        return session

    def recreate_http_sessions(self):
        """Close existing sessions and recreate them."""
        if hasattr(self, "admin_session"):
            self.admin_session.close()
            del self.admin_session
        if hasattr(self, "session"):
            self.session.close()
            del self.session

        self.admin_session = (
            self.init_session(self.admin_certs) if self.admin_certs else None
        )
        self.session = (
            self.init_session(self.client_certs) if self.client_certs else None
        )

    # region Pickling/unpickling helpers
    def __getstate__(self) -> dict:
        """Pickling helper: sessions cannot be marshalled across process boundaries, so we marshal the data pieces only
        in order to reconstruct them on the other side. This makes the object marshallable across process boundaries.
        TODO: the same problem must be solved for the `event_cache` in general (can be too big) and across processes.
        """
        state = self.__dict__.copy()
        # remove the sessions - they are not pickle-able
        del state["session"]
        del state["admin_session"]
        return state

    def __setstate__(self, state: dict):
        """Unpickling helper: recreates the properties `session` and `admin_session`"""
        self.__dict__.update(state)
        # reconstruct the sessions
        self.recreate_http_sessions()

    # endregion


class EventCache:
    def __init__(self):
        self.reset()

    def reset(self):
        self.tracked_job_ids = {}

    def get(self, job_id):
        tracked_job_ids = self.tracked_job_ids
        next_index = tracked_job_ids.get(job_id, None)
        if next_index is None:
            next_index = tracked_job_ids[job_id] = 1
        return next_index

    def event_received(self, job_id, index):
        index = index + 1
        tracked_job_ids = self.tracked_job_ids
        next_index = tracked_job_ids.get(job_id, None)
        if next_index is None:
            next_index = tracked_job_ids[job_id] = index
        if index > next_index:
            tracked_job_ids[job_id] = index

    def event_completed(self, job_id):
        tracked_job_ids = self.tracked_job_ids
        if job_id in tracked_job_ids:
            del tracked_job_ids[job_id]


class InvalidCertificateRoleError(Exception):
    pass


def query_node(
    node_session,
    method,
    path,
    params,
    role="client",
    language_version=2,
    key_alias=None,
    retries=5,
):
    """
    makes an http call against the node using the specified params
    """
    prefix = "/api/v1"
    url = node_session.hostname + prefix + path
    headers = {"Symbiont-Node-Fqdn": node_session.node_fqdn}

    tracer = node_session.tracer
    if tracer is not None:
        span = tracer.span
        # We only want to use the active trace for the main process and
        # not the process pool because we get missing spans for some reason.
        if tracer.pid == os.getpid():
            span = beeline.get_beeline().tracer_impl.get_active_span().id
        else:
            span = tracer.span
        nonce = f"{tracer.trace_id}-{tracer.get_nonce()}"
        headers["X-Honeycomb-Trace"] = marshal_trace_context(nonce, span, {})

    if key_alias:
        headers["Symbiont-Key-Alias"] = key_alias

    params_copy = params
    if method in ["POST", "PUT"]:
        params_key = "data"
        headers["Content-Type"] = "application/json"
        params = dumps(params)
    else:
        params_key = "params"

    if node_session.admin_session:
        http_session = node_session.admin_session
    elif node_session.session:
        http_session = node_session.session
    else:
        raise InvalidCertificateRoleError(f"Unsupported role for client certs: {role}")

    request_arguments = {
        **{
            "headers": headers,
            params_key: params,
            "verify": False,
        },
    }

    def maybe_retry(exception, session):
        if retries > 0:
            logger.info(f"retrying in 1 second: exception calling node: {exception}")
            time.sleep(1)
            return query_node(
                session,
                method,
                path,
                params_copy,
                language_version=language_version,
                key_alias=key_alias,
                retries=retries - 1,
                role=role,
            )
        else:
            logger.info(f"stopping retries: exception calling node: {exception}")
            raise exception

    logger.debug(_format_request(url, method, request_arguments))
    try:
        response = http_session.request(method, url, **request_arguments)
        logger.debug(_format_response(response))
    except requests.exceptions.SSLError as e:
        # http sessions may be corrupted, recreate and try again
        node_session.recreate_http_sessions()
        return maybe_retry(e, node_session)
    except Exception as e:
        return maybe_retry(e, node_session)
    try:
        _check_errors(response, language_version)
    except BaseContractError as e:
        raise e
    except Exception as e:
        return maybe_retry(e, node_session)

    if response.text == "":
        return None

    body = loads(response.text)
    if "data" in body:
        data = body["data"]
        if "job_id" in data:
            job_id = data["job_id"]
            return Job(node_session, job_id, key_alias, url)
        else:
            return data

    return body


def _check_errors(response, language_version):
    status = response.status_code
    if status in [200, 202]:
        return

    try:
        error = loads(response.text)["error"]
    except Exception:
        request = response.request
        raise Exception(
            "request failed: {} {} {} \n {}".format(
                request.method, request.url, response.status_code, response.text
            )
        )
    if (
        not isinstance(error, str)
        and (
            ("type" in error and error["type"] == "ContractRequestServerError")
            or ("message" in error and error["message"] == ASYNC_CALL_FAILED)
        )
    ) or ("type" in error and error["type"] == "NotFoundError" and status == 404):
        raise ContractError(error.get("message"))

    raise Exception("{}\n\nerror contacting node, code {}".format(error, status))


def _format_request(url, method, request_arguments):
    """format request for logging"""
    if method in ("GET", "POST", "PUT", "DELETE"):
        return "{} {} {}".format(url, method, request_arguments)
    else:
        assert False, "unsupported method: {}".format(method)


def _format_response(response):
    return f"{response.status_code} {response.text}"
