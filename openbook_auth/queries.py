from django.db.models import Q

from openbook_posts.queries import make_only_posts_with_hashtag_with_id, make_exclude_soft_deleted_posts_query, \
    make_only_published_posts_query, make_exclude_reported_and_approved_posts_query, \
    make_exclude_reported_posts_by_user_with_id_query, make_exclude_community_posts_banned_from_for_user_with_id_query, \
    make_exclude_closed_posts_query, make_only_public_posts_query, make_exclude_blocked_posts_for_user_with_id_query


def make_get_hashtag_posts_query_for_user(hashtag, user):
    # Retrieve posts with the given hashtag
    hashtag_posts_query = make_only_posts_with_hashtag_with_id(hashtag_id=hashtag.pk)

    # Only retrieve public posts
    hashtag_posts_query.add(make_only_public_posts_query(), Q.AND)

    # Dont retrieve soft deleted posts
    hashtag_posts_query.add(make_exclude_soft_deleted_posts_query(), Q.AND)

    # Dont retrieve posts from blocked people
    hashtag_posts_query.add(make_exclude_blocked_posts_for_user_with_id_query(user_id=user.pk), Q.AND)

    # Only retrieve published posts
    hashtag_posts_query.add(make_only_published_posts_query(), Q.AND)

    # Don't retrieve items that have been reported and approved
    hashtag_posts_query.add(make_exclude_reported_and_approved_posts_query(), Q.AND)

    # Dont retrieve items we have reported
    hashtag_posts_query.add(make_exclude_reported_posts_by_user_with_id_query(user_id=user.pk), Q.AND)

    # Dont retrieve posts from communities we're  banned from
    hashtag_posts_query.add(make_exclude_community_posts_banned_from_for_user_with_id_query(user_id=user.pk), Q.AND)

    # Dont retrieve closed posts
    hashtag_posts_query.add(make_exclude_closed_posts_query(), Q.AND)

    return hashtag_posts_query