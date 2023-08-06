from redflagbpm.BPMService import BPMService
from redflagbpm.Services import Service, DocumentService, Context


def setupServices(self: BPMService):
    self.service = Service(self)
    self.documentService = DocumentService(self)
    self.context = Context(self)


BPMService.setupServices = setupServices
