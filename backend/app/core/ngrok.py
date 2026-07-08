import os
import re
import logging
from pyngrok import ngrok

logger = logging.getLogger("uvicorn.error")

def start_ngrok_tunnel(port: int = 8000):
    # Check if a tunnel is already running to avoid duplicate tunnels
    try:
        tunnels = ngrok.get_tunnels()
        if tunnels:
            for t in tunnels:
                logger.info(f"Existing ngrok tunnel already active: {t.public_url}")
            return
    except Exception:
        pass

    # Read credentials from venv/.env
    venv_env = os.path.join(os.path.dirname(__file__), "..", "..", "..", "venv", ".env")
    ngrok_url = None
    ngrok_token = None

    if os.path.exists(venv_env):
        try:
            with open(venv_env, "r") as f:
                content = f.read()
                url_match = re.search(r'["\'](https?://[^"\']+)["\']', content)
                if url_match:
                    ngrok_url = url_match.group(1)
                all_tokens = re.findall(r'["\']([a-zA-Z0-9_-]{15,})["\']', content)
                if all_tokens:
                    ngrok_token = all_tokens[-1]
        except Exception as e:
            logger.warning(f"Failed to read config from venv/.env: {e}")

    # Fallback to system environment variables
    if not ngrok_token:
        ngrok_token = os.environ.get("NGROK_AUTH_TOKEN")
    if not ngrok_url:
        ngrok_url = os.environ.get("NGROK_URL")

    if not ngrok_token:
        logger.warning("NGROK_AUTH_TOKEN not found in venv/.env or environment. Skipping ngrok tunnel startup.")
        return

    try:
        # Set authentication token
        ngrok.set_auth_token(ngrok_token)
        
        tunnel = None
        if ngrok_url:
            domain_name = ngrok_url.replace("https://", "").replace("http://", "")
            subdomain_name = domain_name.split(".")[0]
            
            # Try to connect with custom domain
            try:
                tunnel = ngrok.connect(port, domain=domain_name)
                logger.info(f"NGROK: Public tunnel established at: {tunnel.public_url}")
            except Exception as e_domain:
                logger.warning(f"NGROK: Could not connect using custom domain '{domain_name}': {e_domain}")
                
                # Try to connect with custom subdomain
                try:
                    tunnel = ngrok.connect(port, subdomain=subdomain_name)
                    logger.info(f"NGROK: Public tunnel established at: {tunnel.public_url}")
                except Exception as e_sub:
                    logger.warning(f"NGROK: Could not connect using custom subdomain '{subdomain_name}': {e_sub}")
        
        # Fallback to random ngrok URL if custom domain failed or wasn't provided
        if not tunnel:
            tunnel = ngrok.connect(port)
            logger.info(f"NGROK: Free-tier random public tunnel established at: {tunnel.public_url}")
            
    except Exception as e:
        logger.error(f"NGROK: Failed to start ngrok tunnel: {e}")
