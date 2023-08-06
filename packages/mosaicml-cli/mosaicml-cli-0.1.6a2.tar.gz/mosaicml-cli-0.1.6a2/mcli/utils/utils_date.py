"""This Module stores utils for pretty printing Datetime objects"""
from datetime import datetime


def time_since(date: datetime, short: bool = False) -> str:
    seconds = (datetime.now() - date).total_seconds()
    interval = seconds / 31536000
    if interval > 1:
        if short:
            return f'{int(interval)}yr'
        return f'{int(interval)} years'
    interval = seconds / 2592000
    if interval > 1:
        if short:
            return f'{int(interval)}mo'
        return f'{int(interval)} months'
    interval = seconds / 86400
    if interval > 1:
        if short:
            return f'{int(interval)}d'
        return f'{int(interval)} days'
    interval = seconds / 3600
    if interval > 1:
        if short:
            return f'{int(interval)}h'
        return f'{int(interval)} hours'
    interval = seconds / 60
    if interval > 1:
        if short:
            return f'{int(interval)}m'
        return f'{int(interval)} minutes'

    if short:
        return f'{int(interval)}s'
    return f'{int(interval)} seconds'
