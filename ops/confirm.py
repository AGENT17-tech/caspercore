PENDING = None  # holds pending action


def set_pending(action_packet):
    global PENDING
    PENDING = action_packet


def clear_pending():
    global PENDING
    PENDING = None


def get_pending():
    return PENDING
