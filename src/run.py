from src.app import app
import os

port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)

# app.run(debug=app.config['DEBUG'], port=4990)
