from oauthenticator.generic import GenericOAuthenticator
from jupyterhub.auth import LocalAuthenticator

class LocalGenericOAuthenticator(LocalAuthenticator, GenericOAuthenticator):
    pass

c.JupyterHub.ssl_key = "/etc/ssl/certs/my_cert.key"
c.JupyterHub.ssl_cert = "/etc/ssl/certs/my_cert-combined.crt"
c.GenericOAuthenticator.tls_verify = False

c.JupyterHub.authenticator_class = LocalGenericOAuthenticator

OIDC_BASE = "https://api.hostname:81"

# OAuth2 application info
# -----------------------
c.GenericOAuthenticator.client_id = "jupyterhub-client"
c.GenericOAuthenticator.client_secret = "jupyterhub-secret"

# Identity provider info
# ----------------------
c.GenericOAuthenticator.authorize_url = f"{OIDC_BASE}/authorize"
c.GenericOAuthenticator.token_url = f"{OIDC_BASE}/token"
c.GenericOAuthenticator.userdata_url = f"{OIDC_BASE}/userinfo"

# JupyterHub's own callback URL (must match redirect_uri registered in IdP)
c.GenericOAuthenticator.oauth_callback_url = "https://jupyterhub.hostname:8000/hub/oauth_callback"

# What we request about the user
# ------------------------------
# scope represents requested information about the user, and since we configure
# this against an OIDC based identity provider, we should request "openid" at
# least.
#
# In this example we include "email" and "groups" as well, and then declare that
# we should set the username based on the "email" key in the response, and read
# group membership from the "groups" key in the response.
#
#c.GenericOAuthenticator.scope = ["openid", "profile", "email", "groups"]
c.GenericOAuthenticator.scope = ["openid", "profile", "email"]
# Map username from the userinfo response
# Your /userinfo returns: { "sub", "email", "name" }
c.GenericOAuthenticator.username_claim = "sub"
#c.GenericOAuthenticator.auth_state_groups_key = "oauth_user.groups"

# Authorization
# -------------
#c.GenericOAuthenticator.allowed_users = {"user1@example.com"}
#c.GenericOAuthenticator.allowed_groups = {"staff"}
#c.GenericOAuthenticator.admin_users = {"user2@example.com"}
#c.GenericOAuthenticator.admin_groups = {"administrator"}

# If you want to allow any authenticated user:
c.GenericOAuthenticator.allow_all = True
c.LocalAuthenticator.create_system_users = True
c.Authenticator.delete_invalid_users = True
c.LocalAuthenticator.add_user_cmd = ['useradd', '-m']
