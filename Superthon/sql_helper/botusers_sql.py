import threading

from sqlalchemy import Column, String, UnicodeText, distinct, func

from . import BASE, SESSION


class SuperthonBroadcast(BASE):
    __tablename__ = "Superthonbroadcast"
    keywoard = Column(UnicodeText, primary_key=True)
    group_id = Column(String(14), primary_key=True, nullable=False)

    def __init__(self, keywoard, group_id):
        self.keywoard = keywoard
        self.group_id = str(group_id)

    def __repr__(self):
        return "<Superthon Broadcast channels '%s' for %s>" % (
            self.group_id,
            self.keywoard,
        )

    def __eq__(self, other):
        return bool(
            isinstance(other, SuperthonBroadcast)
            and self.keywoard == other.keywoard
            and self.group_id == other.group_id
        )


SuperthonBroadcast.__table__.create(checkfirst=True)

SuperthonBROADCAST_INSERTION_LOCK = threading.RLock()


class BROADCAST_SQL:
    def __init__(self):
        self.BROADCAST_CHANNELS = {}


BROADCAST_SQL_ = BROADCAST_SQL()


def add_to_broadcastlist(keywoard, group_id):
    with SuperthonBROADCAST_INSERTION_LOCK:
        broadcast_group = SuperthonBroadcast(keywoard, str(group_id))

        SESSION.merge(broadcast_group)
        SESSION.commit()
        BROADCAST_SQL_.BROADCAST_CHANNELS.setdefault(keywoard, set()).add(str(group_id))


def rm_from_broadcastlist(keywoard, group_id):
    with SuperthonBROADCAST_INSERTION_LOCK:
        broadcast_group = SESSION.query(SuperthonBroadcast).get((keywoard, str(group_id)))
        if broadcast_group:
            if str(group_id) in BROADCAST_SQL_.BROADCAST_CHANNELS.get(keywoard, set()):
                BROADCAST_SQL_.BROADCAST_CHANNELS.get(keywoard, set()).remove(
                    str(group_id)
                )

            SESSION.delete(broadcast_group)
            SESSION.commit()
            return True

        SESSION.close()
        return False


def is_in_broadcastlist(keywoard, group_id):
    with SuperthonBROADCAST_INSERTION_LOCK:
        broadcast_group = SESSION.query(SuperthonBroadcast).get((keywoard, str(group_id)))
        return bool(broadcast_group)


def del_keyword_broadcastlist(keywoard):
    with SuperthonBROADCAST_INSERTION_LOCK:
        broadcast_group = (
            SESSION.query(SuperthonBroadcast.keywoard)
            .filter(SuperthonBroadcast.keywoard == keywoard)
            .delete()
        )
        BROADCAST_SQL_.BROADCAST_CHANNELS.pop(keywoard)
        SESSION.commit()


def get_chat_broadcastlist(keywoard):
    return BROADCAST_SQL_.BROADCAST_CHANNELS.get(keywoard, set())


def get_broadcastlist_chats():
    try:
        chats = SESSION.query(SuperthonBroadcast.keywoard).distinct().all()
        return [i[0] for i in chats]
    finally:
        SESSION.close()


def num_broadcastlist():
    try:
        return SESSION.query(SuperthonBroadcast).count()
    finally:
        SESSION.close()


def num_broadcastlist_chat(keywoard):
    try:
        return (
            SESSION.query(SuperthonBroadcast.keywoard)
            .filter(SuperthonBroadcast.keywoard == keywoard)
            .count()
        )
    finally:
        SESSION.close()


def num_broadcastlist_chats():
    try:
        return SESSION.query(func.count(distinct(SuperthonBroadcast.keywoard))).scalar()
    finally:
        SESSION.close()


def __load_chat_broadcastlists():
    try:
        chats = SESSION.query(SuperthonBroadcast.keywoard).distinct().all()
        for (keywoard,) in chats:
            BROADCAST_SQL_.BROADCAST_CHANNELS[keywoard] = []

        all_groups = SESSION.query(SuperthonBroadcast).all()
        for x in all_groups:
            BROADCAST_SQL_.BROADCAST_CHANNELS[x.keywoard] += [x.group_id]

        BROADCAST_SQL_.BROADCAST_CHANNELS = {
            x: set(y) for x, y in BROADCAST_SQL_.BROADCAST_CHANNELS.items()
        }

    finally:
        SESSION.close()


__load_chat_broadcastlists()