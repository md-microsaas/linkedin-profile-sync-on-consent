"""
linkedin_profile_sync.py

Example: Sync a user's LinkedIn profile after explicit consent.

Prerequisites:
- User has completed LinkedIn OAuth 2.0 authentication.
- You have a valid access token with the required scopes.
- Never fetch or store LinkedIn data without explicit user consent.
"""

import os
import requests

LINKEDIN_PROFILE_ENDPOINT = "https://api.linkedin.com/v2/userinfo"


class LinkedInSync:
    def __init__(self, access_token: str):
        self.access_token = access_token

    def fetch_profile(self):
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

        response = requests.get(
            LINKEDIN_PROFILE_ENDPOINT,
            headers=headers,
            timeout=10,
        )

        response.raise_for_status()
        return response.json()


def sync_profile(user_id: str, consent: bool):
    """
    Sync LinkedIn profile only after explicit consent.
    """

    if not consent:
        return {
            "status": "skipped",
            "reason": "User did not grant consent."
        }

    access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")

    if not access_token:
        raise RuntimeError("Missing LINKEDIN_ACCESS_TOKEN")

    linkedin = LinkedInSync(access_token)
    profile = linkedin.fetch_profile()

    # Example mapping
    user_profile = {
        "user_id": user_id,
        "linkedin_id": profile.get("sub"),
        "name": profile.get("name"),
        "given_name": profile.get("given_name"),
        "family_name": profile.get("family_name"),
        "email": profile.get("email"),
        "picture": profile.get("picture"),
        "locale": profile.get("locale"),
    }

    # Replace this with your database update logic.
    print("Synced profile:")
    print(user_profile)

    return {
        "status": "success",
        "profile": user_profile,
    }


if __name__ == "__main__":
    result = sync_profile(
        user_id="12345",
        consent=True,  # Explicit user consent required
    )

    print(result)
