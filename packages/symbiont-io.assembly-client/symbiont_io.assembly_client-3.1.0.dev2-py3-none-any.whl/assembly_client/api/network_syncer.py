import time
from datetime import datetime

from assembly_client.api import node_api_client
from assembly_client.api.timeout import DEFAULT_TIMEOUT


def sync_sessions(origin_session, tx_index, sessions, timeout=None):
    """
    an implementation of multi-node syncing logic. this works by polling each node specified
    until it has reached the target tx_index
    """

    timeout = DEFAULT_TIMEOUT if timeout is None else timeout

    # to store the called node's reset index if necessary
    reset_index = None
    interval = 0.1

    # create a dictionary to keep track of the nodes that remain unsynced
    unsynced = {session.hostname: None for session in sessions}

    # time the entire procedure so it can exit if it takes longer than 30s
    start = time.time()
    startUTC = datetime.now()
    while True:
        for session in sessions:
            # skip checking the status of nodes that are known to be synced
            if session.hostname not in unsynced:
                continue

            status = node_api_client.statusz(session)

            # if the tx_index is None then check that the node is at the
            # the same reset index as the called node
            if tx_index is None:
                if reset_index is None:
                    reset_index = node_api_client.statusz(origin_session).get(
                        "last_reset_index", None
                    )

                condition = status["last_reset_index"] == reset_index
            # else check if the last transaction index of the node is gte
            # the tx_index passed in
            else:
                condition = status["last_tx_index"] >= tx_index

            if condition:
                del unsynced[session.hostname]

        # if the unsynced dict is empty then all nodes are synced
        if not bool(unsynced):
            return

        end = time.time()
        # if procedure has been running for gte the timeout, break
        if (end - start) >= timeout:
            break

        # sleep
        time.sleep(interval)

    # todo : re-add support for reporting component statuses when failing
    raise Exception(
        f"the network has gone out of sync for more than {timeout} seconds,"
        f" desired tx index is {tx_index}, started at {startUTC} time now is {datetime.now()}"
    )
