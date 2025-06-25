# telegram_bot/utils/context_cleanup.py

def clear_profile_context(context):
    keys = [
        "state",
        "profile_state",
        "selected_section",
        "selected_section_id",
        "selected_subsection",
        "selected_subsection_id",
        "current_section_id",
        "current_subsection",
        "navigation_context"
    ]
    for key in keys:
        context.user_data.pop(key, None)


def clear_friends_context(context):
    keys = [
        "state",
        "friends_state",
        "selected_friend_id",
        "selected_friend_name",
        "friends"
    ]
    for key in keys:
        context.user_data.pop(key, None)
