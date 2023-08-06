import base64
import hashlib

from assembly_client.api.node_client import query_node
from assembly_client.api.contracts import local_code_from_ref
from assembly_client.api.job_management import Job
from assembly_client.api.neo_transactions import (
    build_neo_publish_contracts,
    build_neo_upgrade_protocol,
)
from assembly_client.api.util.time import nanoseconds_to_isoformat
from assembly_client.api.util.date_time import DateTime, DateTimeDelta

###
### core platform apis
###


def register_key_alias(node_session):
    """
    creates a new key alias on the node
    :param node_session: node to target
    :return:a `Job`
    """
    maybe_job = query_node(node_session, "POST", "/key_aliases", {})
    return maybe_job


def deregister_key_alias(node_session, key_alias):
    """
    deregisters a key alias on the node
    :param node_session: node to target
    :param key_alias: key alias to deregister
    :return: a `Job`
    """
    maybe_job = query_node(
        node_session,
        "POST",
        "/key_aliases/deregister/{}".format(key_alias),
        {},
        role="admin",
    )
    return maybe_job


def call(
    node_session,
    key_alias,
    contract_ref,
    function,
    kwargs,
    retries=5,
    query_tx_index=None,
):
    """
    calls the specified contract function on a node
    :param node_session: node to target
    :param key_alias: key_alias to invoke as
    :param contract_ref: contract to call
    :param function: function to invoke
    :param kwargs: dictionary of arguments to the contract, will be json serialized
    :param retries: maximum number of retry attempts to make of the underlying call
    :param query_tx_index: a tuple of (tx_index, minor_tx_index) to run clientside as-of a point in time
    :return: returns a `Job`
    """
    version_to_use = contract_ref.version_to_use_on_api()

    query_params = {}
    if query_tx_index:
        (tx_index, minor_tx_index) = query_tx_index
        query_params["tx_index"] = tx_index
        query_params["minor_tx_index"] = minor_tx_index

    query_params_str = "&".join(["{}={}".format(k, r) for k, r in query_params.items()])

    path = "/contracts/{}/{}/{}?{}".format(
        contract_ref.name, version_to_use, function, query_params_str
    )

    result = query_node(
        node_session,
        "POST",
        path,
        kwargs,
        key_alias=key_alias,
        language_version=contract_ref.language,
        retries=retries,
    )

    if isinstance(result, Job):
        return result
    else:
        return result["result"]


def events(node_session, job_ids=[], start_index=None):
    """
    returns all events available
    :param node_session: node to target
    :param job_ids: job ids to filter the events by
    :return: a list of events in dictionary representation
    """
    max_count = 100
    timeout = 0
    job_ids_param = ",".join(job_ids)
    query_params = {"max_count": max_count, "timeout_secs": timeout}
    if job_ids_param != "":
        query_params["job_ids"] = job_ids_param
    event_cache = node_session.event_cache
    if start_index is None:
        if len(job_ids) > 0:
            start_index = min([event_cache.get(job_id) for job_id in job_ids])
        else:
            start_index = 1
    all_events = []
    while True:
        data = query_node(
            node_session, "GET", "/events/{}".format(start_index), query_params
        )

        events = data["events"]
        if len(events) > 0:
            for event in events:
                event_cache.event_received(event["job_id"], event["index"])
            all_events.extend(events)
            last_index = data["last_index"]
            start_index = last_index + 1
            max_index = data["max_index"]
            if last_index == max_index:
                break
        else:
            break
    return all_events


###
### development mode features
###


def reset(node_session):
    """
    reset the network, clearing all transaction history and all registered key_aliases
    :param node_session: node to target
    :return: new network-seed for the network
    """
    node_session.event_cache.reset()
    return query_node(node_session, "POST", "/config/reset", None, role="admin")


def restart_at(node_session, tx_index):
    """
    restart the node, clearing all transactions after (and including) the tx_index
    :param tx_index: only transactions < tx_index must remain
    :return: an error message in case of a problem
    """
    data = query_node(
        node_session, "POST", "/config/restart_at", {"tx_index": tx_index}, role="admin"
    )
    return data


def get_timeshift(node_session):
    """
    get the current time shift value
    :param node_session: node to target
    :return: current time shift in nanoseconds
    """
    data = query_node(node_session, "GET", "/config/timeshift", None, role="admin")
    return data["timeshift"]


def add_timeshift(node_session, timeshift):
    """
    set the current time shift value
    :param node_session: node to target
    :param timeshift: desired time shift value in nanoseconds
    :return: None
    """
    query_node(
        node_session,
        "POST",
        "/config/timeshift",
        {"timeshift": timeshift},
        role="admin",
    )


def set_time(node_session, timestamp):
    """
    set the current time to approximately the desired value. this is approximate as the time
    will change as this executes, resulting in drift similar in magnitude to the time it takes to
    call this function
    :param node_session: node to target
    :param timestamp: target timestamp in nanoseconds
    :return: None
    """
    server_time = current_time(node_session)
    add_timeshift(node_session, int(timestamp - server_time))


def get_datetime_shift(node_session):
    """
    get the current time shift value
    :param node_session: node to target
    :return: current time shift as DateTime
    """
    data = query_node(node_session, "GET", "/config/timeshift", None, role="admin")
    return DateTimeDelta.from_nanos(data["timeshift"])


def add_datetime_shift(node_session, timeshift):
    """
    set the current time shift value
    :param node_session: node to target
    :param timeshift: desired time shift value as DateTimeDelta
    :return: None
    """
    ts = timeshift.to_nanos()
    query_node(
        node_session, "POST", "/config/timeshift", {"timeshift": ts}, role="admin"
    )


def set_datetime(node_session, timestamp):
    """
    set the current time to approximately the desired value. this is approximate as the time
    will change as this executes, resulting in drift similar in magnitude to the time it takes to
    call this function
    :param node_session: node to target
    :param timestamp: target timestamp as DateTime
    :return: None
    """
    server_time = current_time(node_session)
    add_datetime_shift(
        node_session,
        timestamp
        - DateTime.fromisotimestamp(nanoseconds_to_isoformat(int(server_time))),
    )


###
### contract level inspections
###


def list_contracts(node_session):
    """
    inspection for contracts on a network
    :param node_session: node to target
    :return: information about each contract published
    """
    return query_node(node_session, "GET", "/contracts", None)


def list_key_aliases(node_session, locality=None, channel=None):
    """
    lists the key aliases registered and known
    :param node_session: node to target
    :param locality: one of 'local', 'remote', or None
    :param channel: channel for which the key aliases can see
    :return: list of key aliases known to the node
    """
    query_params = ""
    if locality is not None or channel is not None:
        query_params += "?"
    if locality is not None:
        query_params += "locality=" + locality
    if channel is not None:
        if locality is not None:
            query_params += "&"
        query_params += "channel=" + channel
    return query_node(node_session, "GET", "/key_aliases" + query_params, None)


def list_deregistered_key_aliases(node_session):
    """
    lists the deregistered key aliases
    :param node_session: node to target
    :return: list of deregistered key aliases
    """
    results = query_node(
        node_session, "GET", "/key_aliases/deregistered", None, role="admin"
    )
    return {result["key_alias"]: result["tx_index"] for result in results}


def contract_info(node_session, contract_ref):
    """
    detailed inspection of a specific contract, will include function signatures
    :param node_session: node to target
    :param contract_ref: contract to inspect
    :return: information about the contract
    """
    return query_node(
        node_session,
        "GET",
        "/contracts/{}/{}".format(
            contract_ref.name, contract_ref.version_to_use_on_api()
        ),
        None,
        language_version=contract_ref.language,
        role="admin",
    )


def storage(node_session, key_alias, contract_ref):
    """
    provides access to a contract's storage. this will not work on contracts with large
    amounts of data, as it dumps the full storage in one api call
    :param node_session: node to target
    :param key_alias: what alias to view as
    :param contract_ref: what contract namespace to target
    :return: a wrapper object holding the data as a large dictionary, providing trivial access methods
    """

    path = "/debug/storage/{}/{}".format(contract_ref.name, contract_ref.version)
    data = query_node(
        node_session,
        "GET",
        path,
        None,
        language_version=contract_ref.language,
        key_alias=key_alias,
        role="admin",
    )

    # todo : give this upgrades and shift impl elsewhere
    class StorageWrapper:
        def __init__(self, data):
            self.data = data

        def get(self, channel_name, key):
            if channel_name not in self.data:
                raise Exception("channel {} not in storage".format(channel_name))
            return self.data[channel_name].get(key, None)

        def all(self, channel_name="PUBLIC"):
            return self.data[channel_name]

    return StorageWrapper(data["storage"])


def channels(node_session, key_alias):
    """
    Provides the channels a key_alias has access to
    :param key_alias: filter channels by this key_alias
    :return: list of channels
    """
    path = "/debug/channels/{}".format(key_alias)
    data = query_node(node_session, "GET", path, None, role="admin")
    return data


def digest(node_session, tx_index=None):
    """
    Provides a digest of the node state
    :param as_of_index: state up to the provided tx_index, default to latest
    """
    path = f"/digest?"

    if tx_index:
        path += f"as_of_index={tx_index}"

    maybe_job = query_node(node_session, "GET", path, None, role="admin")

    return maybe_job


###
### general node status inspection
###


def current_time(node_session):
    """
    :param node_session: node to target
    :return: current network time in nanoseconds
    """
    return statusz(node_session)["current_time"]


def current_datetime(node_session):
    """
    :param node_session: node to target
    :return: current network time as DateTime
    """
    return DateTime.fromisotimestamp(
        nanoseconds_to_isoformat(statusz(node_session)["current_time"])
    )


def statusz(node_session):
    """
    get overall node status information
    :param node_session: node to target
    :return: dictionary of status information
    """
    return query_node(node_session, "GET", "/", None)


def status(node_session):
    """
    a binary yes/no on the health of the node, return 0 if healthy 1 otherwise
    :param node_session: node to target
    :return: 0 if healthy 1 otherwise
    """
    try:
        query_node(node_session, "GET", "/status", None, retries=0, role="admin")
        return 0
    except Exception:
        return 1


def assembly_status(node_session):
    """Retrieve the status of the node's services i.e. ApiServer, Txe and Smartlog.

    Parameters:
    node_session (NodeSession): Node to query the status of.

    Returns:
    dict: Dictionary of service name to status meta info.
    """

    return query_node(
        node_session, "GET", "/assembly_status", None, retries=0, role="admin"
    )


###
### smartlog operations
###


def append_smartlog_transaction(node_session, topics, data):
    """
    writes this transaction directly to the append transactions api on smartlog,
    bypassing epilog
    :param node_session: node to target
    :param topics: list of string topics
    :param data: transaction body in byte form
    :return:
    """

    topic_string = ",".join(topics)
    topic_bytes = topic_string.encode("utf-8")
    tx_hash = hashlib.sha256(topic_bytes + data).hexdigest()
    encoded_data = base64.standard_b64encode(data).decode("utf-8")
    transaction = {
        "topics": topic_string,
        "data": encoded_data,
        "hash": tx_hash,
    }
    transactions = {"transactions": [transaction]}

    result = query_node(
        node_session, "POST", "/smartlog/transactions", transactions, role="admin"
    )

    # here we add some extra info to the result, as these are the values that help us find
    # the tx later
    result["tx_hash"] = tx_hash
    result["topics"] = topics

    return result


def get_transactions(
    node_session,
    log_target,
    start_index,
    topics=None,
    max_count=100,
    include_invalid_transactions=False,
):
    """

    reads raw transactions directly from the smartlog api, as per
    /src/klyntar/network/distlog/api/rest/readme.md
    :param node_session: node to target
    :param log_target: either smartlog or epilog, which log to pull transactions from
    :param start_index: the first index to retrieve
    :param max_count: maximum number of transactions to return
    :param include_invalid_transactions: should invalid neo transactions also be returned
    :return: a list of transactions packaged up in a dictionary with metadata info
    """

    params = {
        "max_count": max_count,
        "include_invalid_transactions": include_invalid_transactions,
    }
    if topics:
        params["topics"] = topics

    return query_node(
        node_session,
        "GET",
        f"/{log_target}/transactions/{start_index}",
        params,
        role="admin",
    )


###
### neo operations
###


def neo_publish_contracts(node_session, contract_path, contract_refs, neo_key, neo_crt):
    (topics, byte_data) = build_neo_publish_contracts(
        contract_path, contract_refs, neo_key, neo_crt
    )
    return append_smartlog_transaction(node_session, ["neo/contracts"], byte_data)


def neo_upgrade_protocol(node_session, txe_protocol, sympl_version, neo_key, neo_crt):
    (topics, byte_data) = build_neo_upgrade_protocol(
        txe_protocol, sympl_version, neo_key, neo_crt
    )
    return append_smartlog_transaction(node_session, ["neo/upgrade"], byte_data)
