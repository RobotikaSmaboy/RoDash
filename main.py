from roboys_dash import create_app
from roboys_dash import config

from werkzeug.middleware.proxy_fix import ProxyFix

app = create_app()

# Apply proxy fix if necessary
# Ref: https://flask.palletsprojects.com/en/2.3.x/deploying/proxy_fix/
if(int(config.get("BEHIND_PROXY")) == 1):
    app.wsgi_app = ProxyFix(
        app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
    )

if __name__ == "__main__":
    app.run(port=34455, debug=True)
