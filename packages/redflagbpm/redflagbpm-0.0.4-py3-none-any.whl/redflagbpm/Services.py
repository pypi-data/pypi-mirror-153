from typing import List, Any

from redflagbpm.BPMService import BPMService


class Service:
    bpm: BPMService

    def __init__(self, bpm: BPMService):
        self.bpm = bpm

    def sendMail(self, msg: dict):
        return self.bpm.call("EBHBPMService.sendMail", msg)

    def execute(self, script: str, context: dict):
        return self.bpm.call("EBHBPMService.execute", body={
            "script": script,
            "context": context
        })

    def notifyUser(self, user: str, title: str, description: str, target: str = None, sound: bool = False):
        return self.bpm.call("EBHBPMService.notifyUser", body={
            "user": user,
            "title": title,
            "description": description,
            "target": target,
            "sound": sound})

    def notifyGroup(self, group: str, title: str, description: str, target: str = None, sound: bool = False):
        return self.bpm.call("EBHBPMService.notifyGroup", body={
            "group": group,
            "title": title,
            "description": description,
            "target": target,
            "sound": sound})

    def now(self):
        return self.bpm.call("EBHBPMService.now", body={})

    def today(self):
        return self.bpm.call("EBHBPMService.today", body={})

    def getProperty(self, code: str, the_property: str):
        return self.bpm.call("EBHBPMService.getProperty", body={
            "code": code,
            "property": the_property})

    def text(self, name: str):
        return self.bpm.call("EBHBPMService.text", body={
            "name": name})

    def code(self, name: str):
        return self.bpm.call("EBHBPMService.code", body={
            "name": name})

    def list(self, name: str, the_filter: dict = None):
        return self.bpm.call("EBHBPMService.list", body={
            "name": name,
            "filter": the_filter})


class Context:
    bpm: BPMService

    def __init__(self, bpm: BPMService):
        self.bpm = bpm

    def setValue(self, variable: str, value: Any, address=None):
        self.bpm.exec(script="_____context_____.setAttribute('" + variable + "',_____variable_____,100)",
                      context={"_____variable_____": value},
                      address=address)

    def setJsonValue(self, variable: str, key: str, value: Any, address=None):
        self.bpm.exec(script=variable + ('.put("%s",_____variable_____)' % key),
                      context={"_____variable_____": value},
                      address=address)

    def setDictValue(self, variable: str, key: str, value: Any, address=None):
        self.bpm.exec(script=variable + ('["%s"]=_____variable_____' % key),
                      context={"_____variable_____": value},
                      address=address)

    def setInputValue(self, key: str, value: Any, address=None):
        self.setJsonValue("input", key, value, address)

    def getValue(self, variable: str, address=None):
        return self.bpm.exec(script=variable, address=address)

    def getJsonValue(self, variable: str, key: str, address=None):
        return self.bpm.exec(script=variable + ('.getValue("%s")' % key),
                             address=address)

    def getDictValue(self, variable: str, key: str, address=None):
        return self.bpm.exec(script=variable + ('["%s"]' % key),
                             address=address)

    def getInputValue(self, key: str, address=None):
        return self.getJsonValue("input", key, address)


class DocumentService:
    bpm: BPMService

    def __init__(self, bpm: BPMService):
        self.bpm = bpm

    def registerCollection(self, schema: dict):
        return self.bpm.call("EBHBPMDocumentService.registerCollection", body={"schema": schema})

    def unregisterCollection(self, collection: str) -> bool:
        return self.bpm.call("EBHBPMDocumentService.unregisterCollection", body={"collection": collection})

    def listCollections(self) -> List[str]:
        return self.bpm.call("EBHBPMDocumentService.listCollections", body={})

    def getSchema(self, collection: str) -> dict:
        return self.bpm.call("EBHBPMDocumentService.getSchema", body={"collection": collection})

    def create(self, collection: str, theObject: dict) -> str:
        return self.bpm.call("EBHBPMDocumentService.create", body={"collection": collection, "object": theObject})

    def createList(self, collection: str, theObject: List[dict]):
        return self.bpm.call("EBHBPMDocumentService.createList", body={"collection": collection, "object": theObject})

    def readByOid(self, oid: str) -> dict:
        return self.bpm.call("EBHBPMDocumentService.readByOid", body={"oid": oid})

    def readById(self, collection: str, theId: str) -> dict:
        return self.bpm.call("EBHBPMDocumentService.readById", body={"collection": collection, "id": theId})

    def readList(self, collection: str, criteria: str = None, parameters: dict = None, sorting: str = None) -> \
            List[dict]:
        return self.bpm.call("EBHBPMDocumentService.readList",
                             body={"collection": collection, "criteria": criteria, "parameters": parameters,
                                   "sorting": sorting})

    def upsert(self, collection: str, theObject: dict) -> str:
        return self.bpm.call("EBHBPMDocumentService.upsert", body={"collection": collection, "object": theObject})

    def updateByCriteria(self, collection: str, toSet: dict, criteria: str = None, parameters: dict = None) -> int:
        return self.bpm.call("EBHBPMDocumentService.updateByCriteria",
                             body={"collection": collection, "criteria": criteria,
                                   "set": toSet,
                                   "parameters": parameters})

    def updateById(self, collection: str, theId: str, toSet: dict) -> bool:
        return self.bpm.call("EBHBPMDocumentService.updateById", body={"collection": collection,
                                                                       "id": theId,
                                                                       "set": toSet})

    def updateByOid(self, collection: str, oid: str, toSet: dict) -> bool:
        return self.bpm.call("EBHBPMDocumentService.updateByOid", body={"collection": collection,
                                                                        "oid": oid,
                                                                        "set": toSet})

    def deleteByOid(self, oid: str) -> bool:
        return self.bpm.call("EBHBPMDocumentService.deleteByOid", body={"oid": oid})

    def deleteById(self, collection: str, theId: str) -> dict:
        return self.bpm.call("EBHBPMDocumentService.deleteById", body={"collection": collection, "id": theId})

    def deleteByCriteria(self, collection: str, criteria: str = None, parameters: dict = None) -> int:
        return self.bpm.call("EBHBPMDocumentService.updateByCriteria",
                             body={"collection": collection, "criteria": criteria, "parameters": parameters})
