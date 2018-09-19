from src.app import app
import os

# app.run(debug=app.config['DEBUG'], port=4990)

# Bind to PORT if defined, otherwise default to 5000.
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
