from contentful_webhook_receiver.signals import contentful_publish_content_type, contentful_create_content_type, \
    contentful_save_content_type, contentful_delete_content_type, contentful_unpublish_content_type, \
    contentful_create_entry, contentful_save_entry, contentful_publish_entry, contentful_unpublish_entry, \
    contentful_delete_entry, contentful_unarchive_entry, contentful_archive_entry, contentful_autosave_entry, \
    contentful_create_asset, contentful_save_asset, contentful_autosave_asset, contentful_archive_asset, \
    contentful_unarchive_asset, contentful_publish_asset, contentful_unpublish_asset, contentful_delete_asset


class Topics:
    class ContentManagement:
        class ContentType:
            create = 'ContentManagement.ContentType.create'
            save = 'ContentManagement.ContentType.save'
            publish = 'ContentManagement.ContentType.publish'
            unpublish = 'ContentManagement.ContentType.unpublish'
            delete = 'ContentManagement.ContentType.delete'
        class Entry:
            create = 'ContentManagement.Entry.create'
            save = 'ContentManagement.Entry.save'
            autosave = 'ContentManagement.Entry.autosave'
            archive = 'ContentManagement.Entry.archive'
            unarchive = 'ContentManagement.Entry.unarchive'
            publish = 'ContentManagement.Entry.publish'
            unpublish = 'ContentManagement.Entry.unpublish'
            delete = 'ContentManagement.Entry.delete'
        class Asset:
            create = 'ContentManagement.Asset.create'
            save = 'ContentManagement.Asset.save'
            autosave = 'ContentManagement.Asset.autosave'
            archive = 'ContentManagement.Asset.archive'
            unarchive = 'ContentManagement.Asset.unarchive'
            publish = 'ContentManagement.Asset.publish'
            unpublish = 'ContentManagement.Asset.unpublish'
            delete = 'ContentManagement.Asset.delete'


topic_signal_mapping = {
    Topics.ContentManagement.ContentType.create : contentful_create_content_type,
    Topics.ContentManagement.ContentType.save : contentful_save_content_type,
    Topics.ContentManagement.ContentType.publish : contentful_publish_content_type,
    Topics.ContentManagement.ContentType.unpublish : contentful_unpublish_content_type,
    Topics.ContentManagement.ContentType.delete : contentful_delete_content_type,

    Topics.ContentManagement.Entry.create : contentful_create_entry,
    Topics.ContentManagement.Entry.save : contentful_save_entry,
    Topics.ContentManagement.Entry.autosave : contentful_autosave_entry,
    Topics.ContentManagement.Entry.archive : contentful_archive_entry,
    Topics.ContentManagement.Entry.unarchive : contentful_unarchive_entry,
    Topics.ContentManagement.Entry.publish : contentful_publish_entry,
    Topics.ContentManagement.Entry.unpublish : contentful_unpublish_entry,
    Topics.ContentManagement.Entry.delete : contentful_delete_entry,

    Topics.ContentManagement.Asset.create : contentful_create_asset,
    Topics.ContentManagement.Asset.save : contentful_save_asset,
    Topics.ContentManagement.Asset.autosave : contentful_autosave_asset,
    Topics.ContentManagement.Asset.archive : contentful_archive_asset,
    Topics.ContentManagement.Asset.unarchive : contentful_unarchive_asset,
    Topics.ContentManagement.Asset.publish : contentful_publish_asset,
    Topics.ContentManagement.Asset.unpublish : contentful_unpublish_asset,
    Topics.ContentManagement.Asset.delete : contentful_delete_asset,
}
