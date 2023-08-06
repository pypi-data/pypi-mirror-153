
def post_admin_autodiscover(callback):
    from django.contrib import admin
    admin_old_autodiscover = admin.autodiscover
    def admin_new_autodiscover():
        admin_old_autodiscover()
        callback()
    admin.autodiscover = admin_new_autodiscover

def pre_admin_autodiscover(callback):
    from django.contrib import admin
    admin_old_autodiscover = admin.autodiscover
    def admin_new_autodiscover():
        callback()
        admin_old_autodiscover()
    admin.autodiscover = admin_new_autodiscover

