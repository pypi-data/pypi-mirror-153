from .Element import Element
import re
import datetime

class File(Element):
    db_name = 'core'
    
    @classmethod
    def get_collection(cls):
        return 'Files'

    def get_class(self):
        return 'File'
    
    def isEdge(self):
        return False

    def update(self):
        try:
            self.date_updated = datetime.datetime.utcnow()
            self.version = self.get('version', 0)
            if self.version == None:
                self.version = 0
            self.version += 1
            to_update = self.to_dict()
            try:
                to_update.pop('date_created')
            except:
                pass
            try:
                to_update.pop('user_created')
            except:
                pass
            for key in self.attributes:
                if key in to_update and (to_update[key] == None or re.search(r'^(obj_){1}\w+$', key) != None or re.search(r'^(alias_){1}\w+$', key) != None):
                    to_update.pop(key)
            update_obj = self.db[self.get_collection()].fetchDocument(self._key)
            before = update_obj['_rev']
            update_obj.set(to_update)
            update_obj.patch()
            after = update_obj['_rev']
            if self.cascade == True and before != after:
                try:
                    self.cascade_update()
                except:
                    pass
        except:
            return False
        return before != after
