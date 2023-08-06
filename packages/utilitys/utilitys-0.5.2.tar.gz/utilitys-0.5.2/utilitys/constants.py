import logging


class PrjEnums:
    ADD_TYPE_MERGE = "merge"
    ADD_TYPE_NEW = "new"

    # Logging level for 'attention': Like logging.INFO, but requests more of the user's attention
    LOG_LVL_ATTN = logging.INFO + 1
