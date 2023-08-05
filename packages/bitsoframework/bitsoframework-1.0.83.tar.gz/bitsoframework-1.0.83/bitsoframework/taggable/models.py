from taggit.managers import TaggableManager


class TaggableModel(object):
    tags = TaggableManager(blank=True)
