from sqlalchemy.orm import Session


def update_query(db: Session, query, values: dict) -> int:
    """
    in order to update via a query in sqlite we have to no synchronize the session
    after this operation all db objects are expired (same as if you access the object
    after the transaction)

    :return: number of elements updated
    """
    res = query.update(values, synchronize_session=False)
    db.expire_all()
    return res


def delete_query(db: Session, query) -> int:
    """
    in order to delete via a query in sqlite we have to not synchronize the session
    after this operation all db objects are expired (same as if you access the object
    after the transaction)

    :return: number of elements deleted
    """
    res = query.delete(synchronize_session=False)
    db.expire_all()
    return res
