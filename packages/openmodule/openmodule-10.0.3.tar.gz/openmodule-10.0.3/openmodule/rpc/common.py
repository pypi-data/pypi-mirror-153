def channel_to_response_topic(channel: bytes):
    return b"rpc-rep-" + channel


def channel_to_request_topic(channel: bytes):
    return b"rpc-req-" + channel
