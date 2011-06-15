'''
Created on 9 Jun 2011

@author: simon
'''

from trac.core import *
from trac.perm import IPermissionRequestor, IPermissionGroupProvider, IPermissionPolicy, PermissionSystem
from trac.ticket.model import Ticket
from trac.config import IntOption, ListOption
from trac.util.compat import set
from trac.db import with_transaction

class TicketComponentPolicy(Component):
    """Component based ticket access policy.
    
    If users have the TICKET_RESTRICT_COMPONENT permission, then they will only be allowed
    to view tickets for the component group that they are a member of.
    
    For example, in an environment with:
    Users: 
        user1 - member of group component1, with TICKET_RESTRICT_COMPONENT permission
        user2 - member of group component2, with TICKET_RESTRICT_COMPONENT permission
        user3 - member of no group, with TICKET_RESTRICT_COMPONENT permission
        user4 - member of no group, without TICKET_RESTRICT_COMPONENT permission
    
    Components:
        component1, component2, component3
    
    user1 will only be able to see tickets assigned to component1
    user2 will only be able to see tickets assigned to component2
    user3 will be able to see no tickets
    user4 will be able to see all tickets 
    
    """
    
    implements(IPermissionRequestor, IPermissionPolicy)
    
    group_providers = ExtensionPoint(IPermissionGroupProvider)
    
    #components = ListOption('component_policy', 'components', default='',
    #                       doc='Components that will be checked.')
    
    # IPermissionPolicy(Interface)
    def check_permission(self, action, username, resource, perm):
        
        if resource is not None and resource.realm == "ticket" \
            and action != "TICKET_RESTRICT_COMPONENT" and action.startswith('TICKET_') \
            and action != "TICKET_CREATE" \
            and perm.has_permission("TICKET_RESTRICT_COMPONENT") \
            and not perm.has_permission("TRAC_ADMIN"):
            
            # get the ticket
            try:
                ticket = Ticket(self.env, resource.id)
            except TracError:
                return None # Ticket doesn't exist
            
            # get the groups the current user is a member of
            groups = self._get_groups(username)
            
            if not ticket['component'] or ticket['component'] in groups:
                return True
                
            return False
        
        return None

    # IPermissionRequestor methods
    def get_permission_actions(self):
        return ['TICKET_RESTRICT_COMPONENT']
        
    def _get_groups(self, user):
        # Get initial subjects
        groups = set([user])
        for provider in self.group_providers:
            for group in provider.get_permission_groups(user):
                groups.add(group)
        
        perms = PermissionSystem(self.env).get_all_permissions()
        repeat = True
        while repeat:
            repeat = False
            for subject, action in perms:
                if subject in groups and not action.isupper() and action not in groups:
                    groups.add(action)
                    repeat = True 
        
        return groups