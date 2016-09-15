import logging
from pymongo import MongoClient
from utils import properties as props


client_host_map = {
    props.CLIENT_LOCAL: props.LOCAL_HOST
}

coll_db_map = {
    props.COLL_BHARAT_PETROLEUM: props.DB_FUELSTATION,
    props.COLL_HPCL: props.DB_FUELSTATION
}

db_client_map = {
    props.DB_FUELSTATION: props.CLIENT_LOCAL
}

''' To avoid redundant connections to mongo database. '''
__coll_map = {}

__db_map = {}

__client_map = {}


# TODO -- Authorization to be added.
def get_coll(coll_name):
    if coll_name not in __coll_map or __coll_map[coll_name] is None:
        db_name = coll_db_map[coll_name]
        if db_name not in __db_map or __db_map[db_name] is None:
            client_name = db_client_map[db_name]
            if client_name not in __client_map or __client_map[client_name] is None:
                host_name = client_host_map[client_name]
                __client_map[client_name] = MongoClient("%s:%s" % (props.LOCALHOST, props.LOCALHOST_PORT))
                logging.info("Mongo connected to {0} host: {1} and port: {2}".format(client_name, host_name,
                                                                                        props.LOCALHOST_PORT))
            __db_map[db_name] = __client_map[client_name][db_name]

        __coll_map[coll_name] = __db_map[db_name][coll_name]

    return __coll_map[coll_name]


def insert_dto(collname, dto):
    coll = get_coll(coll_name=collname)
    coll.insert(dto)
