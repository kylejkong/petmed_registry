from flask import render_template, redirect, request, session, url_for, flash

from functools import wraps


def apology(message, redirect_url=None, code=400):
    """Render message as an apology to user and redirect to the specified URL"""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s

    if redirect_url:
        flash(message)
        return redirect(url_for(redirect_url))
    else:
        flash(message)
        return redirect(url_for(request.endpoint))



def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

