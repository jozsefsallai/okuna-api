from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

import logging
import json

from openbook_common.tests.helpers import make_user, make_authentication_headers_for_user, \
    make_community

logger = logging.getLogger(__name__)
fake = Faker()


class CommunityAdministratorsAPITest(APITestCase):

    def test_can_get_community_administrators_if_admin(self):
        """
        should be able to retrieve the community administrators if user is admin of community
        """
        user = make_user()
        headers = make_authentication_headers_for_user(user)

        other_user = make_user()
        community = make_community(creator=other_user)
        community_name = community.name

        user.join_community_with_name(community_name)
        other_user.add_administrator_with_username_to_community_with_name(username=user.username,
                                                                          community_name=community.name)

        amount_of_administrators = 5
        administrators_ids = [
            user.pk,
            other_user.pk
        ]

        for i in range(0, amount_of_administrators):
            community_member = make_user()
            community_member.join_community_with_name(community_name)
            other_user.add_administrator_with_username_to_community_with_name(username=community_member,
                                                                              community_name=community.name)
            administrators_ids.append(community_member.pk)

        url = self._get_url(community_name=community.name)
        response = self.client.get(url, **headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_administrators = json.loads(response.content)

        self.assertEqual(len(response_administrators), len(administrators_ids))

        for response_administrator in response_administrators:
            response_administrator_id = response_administrator.get('id')
            self.assertIn(response_administrator_id, administrators_ids)

    def test_can_get_community_administrators_if_mod(self):
        """
        should be able to retrieve the community administrators if user is admin of community
        """
        user = make_user()
        headers = make_authentication_headers_for_user(user)

        other_user = make_user()
        community = make_community(creator=other_user)
        community_name = community.name

        user.join_community_with_name(community_name)
        other_user.add_moderator_with_username_to_community_with_name(username=user.username,
                                                                      community_name=community.name)

        amount_of_administrators = 5
        administrators_ids = [
            other_user.pk
        ]

        for i in range(0, amount_of_administrators):
            community_member = make_user()
            community_member.join_community_with_name(community_name)
            other_user.add_administrator_with_username_to_community_with_name(username=community_member,
                                                                              community_name=community.name)
            administrators_ids.append(community_member.pk)

        url = self._get_url(community_name=community.name)
        response = self.client.get(url, **headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_administrators = json.loads(response.content)

        self.assertEqual(len(response_administrators), len(administrators_ids))

        for response_administrator in response_administrators:
            response_administrator_id = response_administrator.get('id')
            self.assertIn(response_administrator_id, administrators_ids)

    def test_cant_get_community_administrators_if_member(self):
        """
        should be able to retrieve the community administrators if user is member of community
        """
        user = make_user()
        headers = make_authentication_headers_for_user(user)

        other_user = make_user()
        community = make_community(creator=other_user, type='P')
        community_name = community.name

        user.join_community_with_name(community_name)

        url = self._get_url(community_name=community.name)
        response = self.client.get(url, **headers)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cant_get_community_administrators(self):
        """
        should be able to retrieve the community administrators if user is member of community
        """
        user = make_user()
        headers = make_authentication_headers_for_user(user)

        other_user = make_user()
        community = make_community(creator=other_user, type='P')

        url = self._get_url(community_name=community.name)
        response = self.client.get(url, **headers)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_can_add_community_administrator_if_creator(self):
        """
        should be able to add a community administrator if user is creator of community
        """
        user = make_user()
        headers = make_authentication_headers_for_user(user)

        community = make_community(creator=user, type='P')

        user_to_make_admnistrator = make_user()
        user_to_make_admnistrator.join_community_with_name(community_name=community.name)

        url = self._get_url(community_name=community.name)
        response = self.client.put(url, {
            'username': user_to_make_admnistrator.username
        }, **headers)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertTrue(
            user_to_make_admnistrator.is_administrator_of_community_with_name(community_name=community.name))

    def test_logs_community_administrator_added(self):
        """
        should create a log when community administrator was added
        """
        user = make_user()
        headers = make_authentication_headers_for_user(user)

        community = make_community(creator=user, type='P')

        administrator_to_add = make_user()
        administrator_to_add.join_community_with_name(community_name=community.name)

        url = self._get_url(community_name=community.name)
        self.client.put(url, {
            'username': administrator_to_add.username
        }, **headers)

        self.assertTrue(community.logs.filter(action_type='AA',
                                              source_user=user,
                                              target_user=administrator_to_add).exists())

    def test_cant_add_community_administrator_if_mod(self):
        """
        should not be able to add a community administrator if user is moderator of community
        """
        user = make_user()
        other_user = make_user()
        headers = make_authentication_headers_for_user(user)

        community = make_community(creator=other_user, type='P')

        user.join_community_with_name(community_name=community.name)
        other_user.add_moderator_with_username_to_community_with_name(username=user.username,
                                                                      community_name=community.name)

        user_to_make_admnistrator = make_user()
        user_to_make_admnistrator.join_community_with_name(community_name=community.name)

        url = self._get_url(community_name=community.name)
        response = self.client.put(url, {
            'username': user_to_make_admnistrator.username
        }, **headers)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertFalse(
            user_to_make_admnistrator.is_administrator_of_community_with_name(community_name=community.name))

    def test_cant_add_community_administrator_if_member(self):
        """
        should not be able to add a community administrator if user is member of community
        """
        user = make_user()
        other_user = make_user()
        headers = make_authentication_headers_for_user(user)

        community = make_community(creator=other_user, type='P')

        user.join_community_with_name(community_name=community.name)

        user_to_make_admnistrator = make_user()
        user_to_make_admnistrator.join_community_with_name(community_name=community.name)

        url = self._get_url(community_name=community.name)
        response = self.client.put(url, {
            'username': user_to_make_admnistrator.username
        }, **headers)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertFalse(
            user_to_make_admnistrator.is_administrator_of_community_with_name(community_name=community.name))

    def test_cant_add_community_administrator_if_not_member(self):
        """
        should not be able to add a community administrator if user is not member of community
        """
        user = make_user()
        other_user = make_user()
        headers = make_authentication_headers_for_user(user)

        community = make_community(creator=other_user, type='P')

        user_to_make_admnistrator = make_user()
        user_to_make_admnistrator.join_community_with_name(community_name=community.name)

        url = self._get_url(community_name=community.name)
        response = self.client.put(url, {
            'username': user_to_make_admnistrator.username
        }, **headers)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertFalse(
            user_to_make_admnistrator.is_administrator_of_community_with_name(community_name=community.name))

    def _get_url(self, community_name):
        return reverse('community-administrators', kwargs={
            'community_name': community_name
        })


class CommunityAdministratorAPITest(APITestCase):
    def test_can_remove_community_administrator_if_creator(self):
        """
        should be able to remove a community administrator if user is creator of the community
        """
        user = make_user()
        headers = make_authentication_headers_for_user(user)

        community = make_community(creator=user, type='P')

        administrator_to_remove = make_user()
        administrator_to_remove.join_community_with_name(community_name=community.name)
        user.add_administrator_with_username_to_community_with_name(username=administrator_to_remove.username,
                                                                    community_name=community.name)

        url = self._get_url(community_name=community.name, username=administrator_to_remove.username)
        response = self.client.delete(url, **headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertFalse(
            administrator_to_remove.is_administrator_of_community_with_name(community_name=community.name))

    def test_logs_community_administrator_removed(self):
        """
        should create a log when community administrator was removed
        """
        user = make_user()
        headers = make_authentication_headers_for_user(user)

        community = make_community(creator=user, type='P')

        administrator_to_remove = make_user()
        administrator_to_remove.join_community_with_name(community_name=community.name)
        user.add_administrator_with_username_to_community_with_name(username=administrator_to_remove.username,
                                                                    community_name=community.name)

        url = self._get_url(community_name=community.name, username=administrator_to_remove.username)
        self.client.delete(url, **headers)

        self.assertTrue(community.logs.filter(action_type='RA',
                                              source_user=user,
                                              target_user=administrator_to_remove).exists())

    def test_cant_remove_creator_from_community_administrators(self):
        """
        should not be able to remove the creator of the community from the administrators
        """
        user = make_user()
        other_user = make_user()
        headers = make_authentication_headers_for_user(user)

        community = make_community(creator=other_user, type='P')

        user.join_community_with_name(community.name)
        other_user.add_administrator_with_username_to_community_with_name(username=user.username,
                                                                          community_name=community.name)

        url = self._get_url(community_name=community.name, username=other_user.username)
        response = self.client.delete(url, **headers)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertTrue(
            other_user.is_administrator_of_community_with_name(community_name=community.name))

    def test_cant_remove_community_administrator_if_mod(self):
        """
        should not be able to remove a community administrator if user is moderator
        """
        user = make_user()
        other_user = make_user()
        headers = make_authentication_headers_for_user(user)

        community = make_community(creator=other_user, type='P')

        user.join_community_with_name(community.name)
        other_user.add_moderator_with_username_to_community_with_name(username=user.username,
                                                                      community_name=community.name)

        administrator_to_remove = make_user()
        administrator_to_remove.join_community_with_name(community_name=community.name)
        other_user.add_administrator_with_username_to_community_with_name(username=administrator_to_remove.username,
                                                                          community_name=community.name)

        url = self._get_url(community_name=community.name, username=administrator_to_remove.username)
        response = self.client.delete(url, **headers)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertTrue(
            other_user.is_administrator_of_community_with_name(community_name=community.name))

    def test_cant_remove_community_administrator_if_member(self):
        """
        should not be able to remove a community administrator if user is member
        """
        user = make_user()
        other_user = make_user()
        headers = make_authentication_headers_for_user(user)

        community = make_community(creator=other_user, type='P')

        user.join_community_with_name(community.name)

        administrator_to_remove = make_user()
        administrator_to_remove.join_community_with_name(community_name=community.name)
        other_user.add_administrator_with_username_to_community_with_name(username=administrator_to_remove.username,
                                                                          community_name=community.name)

        url = self._get_url(community_name=community.name, username=administrator_to_remove.username)
        response = self.client.delete(url, **headers)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertTrue(
            other_user.is_administrator_of_community_with_name(community_name=community.name))

    def _get_url(self, community_name, username):
        return reverse('community-administrator', kwargs={
            'community_name': community_name,
            'community_administrator_username': username
        })
