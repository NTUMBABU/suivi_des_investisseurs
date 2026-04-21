from functools import wraps
from django.shortcuts import redirect

def session_login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.session.get('utilisateur_id'):
            return redirect('connexion')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
