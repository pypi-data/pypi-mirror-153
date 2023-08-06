import unittest
from aiounittest import async_test
from requests import Response

from algoralabs.admin.keycloak import (
    get_client_id, async_get_client_id, get_users, async_get_users, get_user, async_get_user,
    get_groups, async_get_groups, get_group_members, async_get_group_members,
    add_group_to_user, async_add_group_to_user, delete_group_from_user, async_delete_group_from_user,
    get_roles, async_get_roles, get_roles_for_user, async_get_roles_for_user,
    add_role_mapping_to_user, async_add_role_mapping_to_user
)


class TestRequests(unittest.TestCase):
    pass

    # TODO: Add in once we can configure the testing environment
    # @async_test
    # async def test_get_client_id(self):
    #     sequential_response = get_client_id()
    #     async_response = await async_get_client_id()
    #
    #     self.assertListEqual(sequential_response, async_response)
    #
    # @async_test
    # async def test_get_users(self):
    #     sequential_response = get_users()
    #     async_response = await async_get_users()
    #
    # @async_test
    # async def test_get_user(self):
    #     sequential_response = get_user("bd386ea7-eade-4261-ae9a-61feea1c1f96")
    #     async_response = await async_get_user("bd386ea7-eade-4261-ae9a-61feea1c1f96")
