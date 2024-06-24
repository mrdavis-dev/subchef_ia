import streamlit as st
import streamlit.components.v1 as components
import requests


def button_click_action():
    query_params = st.experimental_get_query_params()
    if "code" in query_params:
        code_values = query_params.get("code")
        if isinstance(code_values, list):
            return code_values
        else:
            return code_values
    return None


def Google_auth(clientId, clientSecret, redirect_uri):
    st.subheader("Google Authentication")
    auth_url = "https://accounts.google.com/o/oauth2/auth"
    client_id = clientId
    client_secret = clientSecret
    redirect_uri = redirect_uri
    scope = "https://www.googleapis.com/auth/userinfo.email"
    auth_endpoint = f"{auth_url}?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}"
    custom_button = f"""
    <link
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css"
      rel="stylesheet"
      integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC"
      crossorigin="anonymous"
    />
    <link
      rel="stylesheet"
      type="text/css"
      href="//fonts.googleapis.com/css?family=Open+Sans"
    />
    <script
      src="https://code.jquery.com/jquery-3.2.1.slim.min.js"
      integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN"
      crossorigin="anonymous"
    ></script>
    <script
      src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"
      integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl"
      crossorigin="anonymous"
    ></script>
    <div style="background: transparent;">
        <div style="width:184px; height: 42px; background-color: #4285f4; border-radius: 2px; box-shadow: 0 3px 4px 0 rgba(0, 0, 0, 0.25); position: relative; cursor: pointer;" onclick="window.open('{auth_endpoint}', '_blank');">
            <div style="position: absolute; margin-top: 1px; margin-left: 1px; width: 40px; height: 40px; border-radius: 2px; background-color: #fff;">
                <img style="position: absolute; margin-top: 11px; margin-left: 11px; width: 18px; height: 18px;" src="https://upload.wikimedia.org/wikipedia/commons/5/53/Google_%22G%22_Logo.svg" />
            </div>
            <p style="float: right; margin: 11px 11px 0 0; color: #fff; font-size: 14px; letter-spacing: 0.2px; font-family: 'Roboto';"><b>Sign in with Google</b></p>
        </div>
    </div>
    """
    components.html(custom_button, height=50)
    security_code = button_click_action()

    if security_code:
        tokens = security_code
        token = ""
        for i in tokens:
            token += i
        verify_token_url = "https://oauth2.googleapis.com/token"
        payload = {
            "code": security_code,
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri,
        }

        response = requests.post(verify_token_url, data=payload)
        response_data = response.json()
        access_token = response_data.get("access_token")
        profile_url = (
            "https://www.googleapis.com/oauth2/v1/userinfo?access_token="
            + access_token
            + ""
        )
        fetch_profile = requests.get(profile_url)
        json_fetch_user_profile = fetch_profile.json()
        username = json_fetch_user_profile.get("email").split("@")[0].upper()
        if response.status_code == 200:
            st.success(f"Login successfully")
            st.write(f"Welcome! {username}")
            return response.status_code, "authenticated"
        else:
            st.warning("Login failed")
            return response.status_code, "login_failed"
