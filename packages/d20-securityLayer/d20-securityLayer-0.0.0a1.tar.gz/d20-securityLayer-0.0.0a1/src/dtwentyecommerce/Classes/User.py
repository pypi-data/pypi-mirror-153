from .Element import Element
from dtwentyorm import Metadata
from ..Error import *
import datetime

class User(Element):

    @classmethod
    def get_collection(cls):
        return 'Users'

    def get_class(self):
        return 'User'
    
    def isEdge(self):
        return False

    def unicity_check(self):
        p = Metadata.Parameter('find', {'_key' : 'unicity_fields'})
        unicity_fields = p.get('value')
        for c in unicity_fields:
            if self.get(c) != None:
                if self.get('_key') == None:
                    query = 'for m in '+ self.get_collection() +'\
                            FILTER m.@f == @v\
                            return m'
                    qp = { 'f': c, 'v':self.get(c) }
                else:
                    query = 'for m in '+ self.get_collection() +'\
                            FILTER m.@f == @v\
                            FILTER m._key != @k\
                            return m'
                    qp = { 'f': c, 'v':self.get(c), 'k':self.get('_key') }
                found = self.db.AQLQuery(query, rawResults=True, batchSize=1, bindVars=qp)
                if len(found) > 0:
                        return False
        return True

    def create(self):
        self.date_created = datetime.datetime.utcnow()
        self.date_updated = self.date_created
        if self.get('username') == None or self.get('username') == '':
            p = Metadata.Parameter('find', {'_key' : 'mem_key'})
            mem_key = p.get('value')
            self.username = self.get(mem_key)
        if not self.unicity_check():
            self._key = None
            raise UserDuplicateKeyException
        to_insert = self.to_dict()
        for key in self.attributes:
            if key in to_insert and to_insert[key] == None:
                to_insert.pop(key)
        ins_obj = self.db[self.get_collection()].createDocument(to_insert)
        ins_obj.save()
        self._key = ins_obj._key 
        return self._key != None

    def update(self):
        self.date_updated = datetime.datetime.utcnow()
        if not self.unicity_check():
            self._key = None
            raise UserDuplicateKeyException
        to_update = self.to_dict()
        to_update.pop('date_created', None)
        to_update.pop('user_created', None)
        for key in self.attributes:
            if key in to_update and to_update[key] == None:
                to_update.pop(key)
        update_obj = self.db[self.get_collection()].fetchDocument(self._key)
        if (update_obj.getStore().get('username') == None or update_obj.getStore().get('username') == '') and (to_update.get('username') == None or to_update.get('username') == ''):
            p = Metadata.Parameter('find', {'_key' : 'mem_key'})
            mem_key = p.get('value')
            to_update['username'] = self.get(mem_key)
        before = update_obj['_rev']
        update_obj.set(to_update)
        update_obj.patch()
        after = update_obj['_rev']
        return before != after
    
    def find(self):
        lfound=[]
        if self.get('_key') != None and self.get('_key') != '':
            try:
                lfound = [self.db[self.get_collection()].fetchDocument(self.get('_key'))]
            except:
                lfound = []
        if len(lfound) <= 0:
            if self.get('username') != None and self.get('username') != '':
                try:
                    lfound = [self.db[self.get_collection()].fetchDocument(self.get('username'))]
                except:
                    lfound = []
                if len(lfound) <= 0:
                    p = Metadata.Parameter('find', {'_key' : 'mem_key'})
                    mem_key = p.get('value')
                    query = f'for d in {self.get_collection()} \
                            FILTER LIKE(d.username, "{self.get("username")}", true) \
                                OR LIKE(d.{mem_key}, "{self.get("username")}", true) \
                                OR LIKE(d.email, "{self.get("username")}", true) \
                            RETURN d'
                    lfound = self.db.AQLQuery(query, rawResults=False, batchSize=1)
                    if len(lfound) <= 0:
                        self._key = None
                        self.status = False
                        return False
        found = lfound[0]
        if found.getStore().get('deleted', False) != False:
            raise ObjectNotFoundException
        for key in self.attributes:
            setattr(self, key, found[key] if key in found.getStore() else self.get(key))