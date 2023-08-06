import time
from functools import reduce
from datetime import datetime

from assembly_client.api.types.event_types import JobFailEvent, JobCompleteEvent
from assembly_client.api.timeout import DEFAULT_TIMEOUT


class ContractErrorInJob(Exception):
    def __init__(self, node_fqdn, job_id, msg, data):
        self.node_fqdn = node_fqdn
        self.job_id = job_id
        self.msg = msg
        self.data = data


class Job:
    def __init__(self, node_session, job_id, submitter, url):
        self.node_session = node_session
        self.job_id = job_id
        self.submitter = submitter
        self.url = url
        # we allow adding a NetworkClient to the `Job` later, enabling use of `sync_with` network-level operation
        self.network_client = None

    def start_waiting(self, timeout=None):

        timeout = DEFAULT_TIMEOUT if timeout is None else timeout

        node_fqdn = self.node_session.node_fqdn
        job_ids = [self.job_id]
        job_done_event = None

        start = time.time()
        startUTC = datetime.now()
        job_fail_event = None

        while True:
            from assembly_client.api import node_api_client

            events = node_api_client.events(self.node_session, job_ids=job_ids)

            if job_done_event is None:
                # find if there is any job fail event for the root job_id
                job_fail_event = next(
                    (
                        e
                        for e in events
                        if is_fail_event(e)
                        and e["job_id"] == self.job_id
                        and e["signing_key_alias"] == self.submitter
                    ),
                    job_fail_event,
                )

                # find if there are any job completed event for the root job_id
                job_done_event = next(
                    (
                        e
                        for e in events
                        if is_completion_event(e) and e["job_id"] == self.job_id
                    ),
                    None,
                )

            # remove the job ids of the completed jobs
            job_ids_done = [
                e["job_id"] for e in events if is_known_completion_event(e, job_ids)
            ]
            job_ids = deduplicate(
                [job_id for job_id in job_ids if job_id not in job_ids_done]
            )

            # if there are no more job ids to track exit the loop
            if job_ids == []:
                break

            if time.time() - start >= timeout:
                break

        # if there are no job complete events simply return the response
        if not job_done_event:
            raise Exception(
                f"a JobComplete event was expected for job_id {self.job_id} "
                f"but was not found after waiting for {timeout}s "
                f"starting at {startUTC} ending at {datetime.now()}."
            )

        # else we must wait for all the other nodes to be caught up to the
        # transaction index provided by the job complete event
        tx_index = job_done_event["tx_index"] if "tx_index" in job_done_event else None

        self.node_session.event_cache.event_completed(job_done_event["job_id"])

        if job_fail_event is not None:
            if "DuplicatePublishError" in str(job_done_event["data"]):
                # in this case we are in the inevitable race that multiple publishes happened at once and while
                # we try to catch by making sure not already published, the txes could be in smartlog but not
                # fully processed by txe. as we know the contract is already there if encountering this we
                # can safely disregard
                # todo : check the hash of the code to make sure it is an exact match
                pass
            else:
                # TODO (mgorelik): Check on impact of the url being removed from the returned error message.
                # Was this needed at all? Let's see who screams
                error = (
                    job_fail_event["data"]["error"]
                    if "error" in job_fail_event["data"]
                    else None
                )
                error_msg = error["message"] if error and "message" in error else None
                error_data = error["data"] if error and "data" in error else None
                raise ContractErrorInJob(node_fqdn, self.job_id, error_msg, error_data)

        return CompleteJob(self, job_done_event, tx_index, [])

    def sync_with(self, timeout=None):
        """
        to sync with others you must first complete, so this simply calls `await` an then delegates
        to `sync_with` on the completed job
        """
        completed_job = self.start_waiting(timeout=timeout)
        return completed_job.sync_with(timeout=timeout)


class CompleteJob:
    def __init__(self, job, event, tx_index, synced_with):
        self.node_session = job.node_session
        self.job_id = job.job_id
        self.submitter = job.submitter
        self.url = job.url
        self.event = event
        self.result = event["data"]
        self.key_alias = (
            self.event["signing_key_alias"]
            if "signing_key_alias" in self.event
            else None
        )
        self.tx_index = tx_index
        self.synced_with = synced_with
        if job.network_client:
            self.network_client = job.network_client

    def sync_with(self, timeout=None):
        """
        for a completed job, we can sync arbitrary nodes in the network such that they are guaranteed
        to have finished executing the workflow too. this is to allow submitting to node 1, but immediately
        reading from node 2. as the second node could be behind, for safe reads you must ensure it is not.
        """
        sessions = set(self.network_client.node_sessions.values())

        # remove the original submitter, we know they are already synced
        sessions.discard(self.node_session)

        self.network_client.sync_sessions(
            self.node_session, self.tx_index, sessions, timeout=timeout
        )

        return self


def is_completion_event(event):
    return event["type"] == JobCompleteEvent.type


def is_fail_event(event):
    return event["type"] == JobFailEvent.type


def is_known_completion_event(event, job_ids):
    return is_completion_event(event) and event["job_id"] in job_ids


def deduplicate(l):
    return list(set(l))


def flatten(l):
    if len(l) == 0:
        return l
    return reduce(lambda x, y: x + y, l)
