from wagtail.contrib.modeladmin.options import ModelAdmin
from wagtail_rest_pack.comments.models import Comment

class CommentsModelAdmin(ModelAdmin):
    model = Comment
    menu_label = 'Comments'
    menu_icon = 'form'
    menu_order = 200
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False  # or True to exclude pages of this type from Wagtail's explorer view
    list_display = ('body', 'created_on', 'created_by', 'parent',)
    list_filter = ('created_on',)
    search_fields = ('body', 'created_by',)
