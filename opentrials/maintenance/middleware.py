from models import MaintenanceWindow

class MaintenanceMiddleware(object):
    def process_request(self, request):
        maintenance_window = MaintenanceWindow.active_maintenance()
        if maintenance_window:
            request.maintenance_window = maintenance_window