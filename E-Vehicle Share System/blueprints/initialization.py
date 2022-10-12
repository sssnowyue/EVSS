from flask_cors import CORS
import config
from app import create_app
from models import VehicleOrderModel
from utils import db
from datetime import datetime
app = create_app()

app.config.from_object(config)
app.app_context().push()
CORS(app, resources={r'/*': {'origins': '*'}})

longitude = -4.280000
latitude = 55.840000
# order = VehicleOrderModel(user_id=2, bike_id=5, state=1)
order = VehicleOrderModel().query.filter_by(id=11).update({"finish_time": datetime.now()})
# db.session.add(order)
db.session.commit()
print('success')