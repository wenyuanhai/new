from django.http import HttpResponseRedirect

def login(func):
    def login_func(request,*args,**kwargs):
        if request.session.has_key("user_id"):
            return func(request,*args,**kwargs)
        else:

            rep = HttpResponseRedirect("/user/login")
            rep.set_cookie("url",request.get_full_path())
            return rep
    return login_func