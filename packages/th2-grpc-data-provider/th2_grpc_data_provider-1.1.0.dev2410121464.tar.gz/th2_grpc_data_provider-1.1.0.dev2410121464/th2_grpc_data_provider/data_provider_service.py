from . import data_provider_pb2_grpc as importStub

class DataProviderService(object):

    def __init__(self, router):
        self.connector = router.get_connection(DataProviderService, importStub.DataProviderStub)

    def getEvent(self, request, timeout=None):
        return self.connector.create_request('getEvent', request, timeout)

    def getEvents(self, request, timeout=None):
        return self.connector.create_request('getEvents', request, timeout)

    def getMessage(self, request, timeout=None):
        return self.connector.create_request('getMessage', request, timeout)

    def getMessageStreams(self, request, timeout=None):
        return self.connector.create_request('getMessageStreams', request, timeout)

    def searchMessages(self, request, timeout=None):
        return self.connector.create_request('searchMessages', request, timeout)

    def searchEvents(self, request, timeout=None):
        return self.connector.create_request('searchEvents', request, timeout)

    def searchMessageGroups(self, request, timeout=None):
        return self.connector.create_request('searchMessageGroups', request, timeout)

    def getMessagesFilters(self, request, timeout=None):
        return self.connector.create_request('getMessagesFilters', request, timeout)

    def getEventsFilters(self, request, timeout=None):
        return self.connector.create_request('getEventsFilters', request, timeout)

    def getEventFilterInfo(self, request, timeout=None):
        return self.connector.create_request('getEventFilterInfo', request, timeout)

    def getMessageFilterInfo(self, request, timeout=None):
        return self.connector.create_request('getMessageFilterInfo', request, timeout)

    def matchEvent(self, request, timeout=None):
        return self.connector.create_request('matchEvent', request, timeout)

    def matchMessage(self, request, timeout=None):
        return self.connector.create_request('matchMessage', request, timeout)