"""This module is for all inventory_status related queries
"""
from typing import List
from typing import Tuple

from bierproductie_api.core.db import DB
from bierproductie_api.domain.inventory_statuses import inventory_status_model
from bierproductie_api.domain.inventory_statuses import \
    inventory_status_schemas

CreateSchema = inventory_status_schemas.Create
UpdateSchema = inventory_status_schemas.Update
Model = inventory_status_model.Model


class Queries():
    """Queries
    """

    async def create(self, inventory_status: CreateSchema) -> Model:
        return await Model.create(**inventory_status.__dict__)

    async def get_list(self, page_size: int,
                       page: int) -> Tuple[List[Model], int]:
        inventory_statuses: List[Model] = await Model.query.order_by(
            Model.name.asc()).offset(page_size * (page - 1)
                                     ).limit(page_size).gino.all()

        count = await DB.func.count(Model.name).gino.scalar()
        return inventory_statuses, count

    async def get_by_id(self, name: str) -> Model:
        return await Model.get(name)

    async def delete(self, name: str) -> Model:
        inventory_status = await self.get_by_id(name)
        await inventory_status.delete()
        return inventory_status

    async def update(self, old_inventory_status: Model,
                     new_inventory_status: UpdateSchema) -> Model:
        to_update = {}
        if new_inventory_status.current_value:
            to_update["current_value"] = new_inventory_status.current_value
        if new_inventory_status.name:
            to_update["name"] = new_inventory_status.name
        if new_inventory_status.max_value:
            to_update["max_value"] = new_inventory_status.max_value
        updated_inventory_status = await old_inventory_status.update(**to_update).apply()
        return updated_inventory_status._instance  # pylint: disable=protected-access
