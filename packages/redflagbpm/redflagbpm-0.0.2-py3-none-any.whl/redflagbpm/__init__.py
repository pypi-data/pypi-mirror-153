from redflagbpm.BPMService import BPMService
from redflagbpm.Services import Service, DocumentService


def setupServices(self:BPMService):
    self.service = Service(self)
    self.documentService = DocumentService(self)

BPMService.setupServices=setupServices