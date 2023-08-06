import django.dispatch


contentful_create_content_type = django.dispatch.Signal()
contentful_save_content_type = django.dispatch.Signal()
contentful_publish_content_type = django.dispatch.Signal()
contentful_unpublish_content_type = django.dispatch.Signal()
contentful_delete_content_type = django.dispatch.Signal()

contentful_create_entry = django.dispatch.Signal()
contentful_save_entry = django.dispatch.Signal()
contentful_autosave_entry = django.dispatch.Signal()
contentful_archive_entry = django.dispatch.Signal()
contentful_unarchive_entry = django.dispatch.Signal()
contentful_publish_entry = django.dispatch.Signal()
contentful_unpublish_entry = django.dispatch.Signal()
contentful_delete_entry = django.dispatch.Signal()

contentful_create_asset = django.dispatch.Signal()
contentful_save_asset = django.dispatch.Signal()
contentful_autosave_asset = django.dispatch.Signal()
contentful_archive_asset = django.dispatch.Signal()
contentful_unarchive_asset = django.dispatch.Signal()
contentful_publish_asset = django.dispatch.Signal()
contentful_unpublish_asset = django.dispatch.Signal()
contentful_delete_asset = django.dispatch.Signal()
