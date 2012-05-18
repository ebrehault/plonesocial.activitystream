from zope.interface import implements
from zope.component import adapts

from Products.ZCatalog.interfaces import ICatalogBrain
from Acquisition import aq_inner, aq_parent


from plonesocial.microblog.interfaces import IStatusUpdate
from plonesocial.activitystream.interfaces import IActivity


class StatusActivity(object):
    implements(IActivity)
    adapts(IStatusUpdate)

    is_status = True
    is_discussion = is_content = False

    def __init__(self, context):
        self.context = context
        self.text = context.text
        self.title = ''
        self.url = ''
        self.portal_type = 'StatusUpdate'
        self.render_type = 'status'
        self.Creator = context.creator
        self.userid = context.userid
        self.created = context.date


class BrainActivity(object):
    implements(IActivity)
    adapts(ICatalogBrain)

    is_status = False

    def __init__(self, context):
        self.context = context
        obj = context.getObject()
        self.title = obj.Title()
        self.url = context.getURL()
        self.portal_type = obj.portal_type
        self.Creator = obj.Creator()
        self.created = obj.creation_date

        if obj.portal_type == 'Discussion Item':
            self.render_type = 'discussion'
            self.userid = obj.author_username
            self.text = obj.getText()
            # obj: DiscussionItem
            # parent: Conversation
            # grandparent: content object
            _contentparent = aq_parent(aq_parent(aq_inner(obj)))
            self.title = _contentparent.Title()
        else:
            self.userid = obj.getOwnerTuple()[1]
            self.render_type = 'content'
            self.text = obj.Description()

    @property
    def is_discussion(self):
        return self.render_type == 'discussion'

    @property
    def is_content(self):
        return self.render_type == 'content'