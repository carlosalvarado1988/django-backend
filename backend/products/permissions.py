from rest_framework import permissions

# This is a custom file to perform permissoons manually

class IsStaffEditorPermission(permissions.DjangoModelPermissions):
    # From the definition of DjangoModelPermissions I followed this snippet of code:
    # Map methods into required permission codes.
    # Override this if you need to also provide 'view' permissions,
    # or if you want to provide custom permission codes.
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'], #added the format here that was empty, and adapted to say view_
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }

    # by commenting this section, also the persmissions can be added directly in the views.py definitions, if form of an array
    # def has_permission(self, request, view):
    #     print('into IsStaffEditorPermission')
    #     if not request.user.is_staff:
    #         return False
        
    #     # this is the default permission in
    #     return super().has_permission(request, view)
    
    # All this method is a little weak, because if one condition is met, then it return TRUE giving all access as permission.
    # This custom method would need more work, so intead of going deep, better check the method above.
    # def has_permission(self, request, view):
        # user = request.user
        # print(user.get_all_permissions())
        # if user.is_staff:
        #     if user.has_perm("products.add_product"): #the format is: "app_name.verb_model_name"
        #         return True
        #     if user.has_perm("products.view_product"):
        #         return True
        #     if user.has_perm("products.change_product"):
        #         return True
        #     if user.has_perm("products.delete_product"):
        #         return True
        #     return False
        # return False

        
    
    # This is an example of an object permission
    # def has_object_permission(self, request, view, obj):
    #     return obj.owner == request.user

    