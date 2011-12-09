from models import MaintenanceWindow

class MaintenanceMiddleware(object):
    def process_request(self, request):
        request.under_maintenance = MaintenanceWindow.under_maintenance()