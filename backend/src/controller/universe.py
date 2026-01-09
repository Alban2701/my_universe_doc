from models.universe import Universe, InputUniverse, PartialUniverse
from db_connection import DbConnection
from typing import List

async def create_universe(universe: InputUniverse, creator_id: int, db: DbConnection) -> PartialUniverse:
    """
    create a new universe in the database

    Parameters:
    - universe: the universe data to insert
    - creator_id: the id of the user creating the universe

    Returns:
    PartialUniverse: the created universe
    """
    sql = (
        "INSERT INTO universe (creator_id, name, description, version) "
        "VALUES (%(creator_id)s, %(name)s, %(description)s, %(version)s) "
        "RETURNING *"
    )
    model_universe = universe.model_dump()
    model_universe["creator_id"] = creator_id
    rows = await db.execute(sql, model_universe)
    returned_universe = PartialUniverse.model_validate(rows[0])
    return returned_universe


async def get_universe_by_id(universe_id: int, db: DbConnection) -> PartialUniverse | None:
    """
    get a universe in the database with the provided id

    Parameters:
    - universe_id (int): the id of the universe

    Returns:
    PartialUniverse: the universe retrieved or None if not found
    """
    sql = "SELECT * FROM universe WHERE id = %(id)s"
    rows = await db.execute(sql, {"id": universe_id})
    if not rows:
        return None
    returned_universe = PartialUniverse.model_validate(rows[0])
    return returned_universe


async def get_universes_by_creator(creator_id: int, db: DbConnection) -> List[PartialUniverse]:
    """
    get all universes created by a user

    Parameters:
    - creator_id (int): the id of the creator

    Returns:
    List[PartialUniverse]: list of universes
    """
    sql = "SELECT * FROM universe WHERE creator_id = %(creator_id)s"
    rows = await db.execute(sql, {"creator_id": creator_id})
    return [PartialUniverse.model_validate(row) for row in rows]


async def update_universe(universe_id: int, universe_patch: PartialUniverse, db: DbConnection) -> PartialUniverse | None:
    """
    update a universe with new data

    Parameters:
    - universe_id (int): the id of the universe to update
    - universe_patch (PartialUniverse): the fields to update

    Returns:
    PartialUniverse: the updated universe or None if not found
    """
    sql = (
        "UPDATE universe SET "
        "name = COALESCE(%(name)s, name), "
        "description = COALESCE(%(description)s, description), "
        "version = COALESCE(%(version)s, version), "
        "updated_at = NOW() "
        "WHERE id = %(id)s "
        "RETURNING *"
    )
    model_patch = universe_patch.model_dump()
    model_patch["id"] = universe_id
    rows = await db.execute(sql, model_patch)
    if not rows:
        return None
    returned_universe = PartialUniverse.model_validate(rows[0])
    return returned_universe


async def delete_universe(universe_id: int, db: DbConnection) -> bool:
    """
    delete a universe from the database

    Parameters:
    - universe_id (int): the id of the universe to delete

    Returns:
    bool: True if deleted, False otherwise
    """
    sql = "DELETE FROM universe WHERE id = %(id)s RETURNING id"
    rows = await db.execute(sql, {"id": universe_id})
    return bool(rows)
