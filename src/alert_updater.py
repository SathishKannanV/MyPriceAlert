from src.common.database import Database
from src.models.alerts.alert import Alert

Database.initialize()

alerts_needing_update = Alert.find_needing_updates()

for alerts in alerts_needing_update:
    alerts.load_item_price()
    alerts.send_email_if_price_reached()