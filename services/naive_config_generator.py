from sqlmodel import Session
from string import Template
from pathlib import Path

from models.caddyfile_model import CaddyfileParameter
from models.site_header_model import Header
from models.user_model import User

from sqlmodel import select
import secrets
from encrypt_manager import decrypt

import logging
logger = logging.getLogger("uvicorn")


def get_naive_config(session: Session) -> str:
    template = Template(Path("templates/caddyfile.template").read_text())

    global_p = session.scalars(
        select(CaddyfileParameter).where(
            CaddyfileParameter.block == "global_parameter"
        )
    ).all()
    site_h = session.scalars(select(Header)).all()
    site_p = session.scalars(
        select(CaddyfileParameter).where(CaddyfileParameter.block == "site_parameter")
    ).all()
    users = session.scalars(select(User)).all()
    forward_proxy_p = session.scalars(
        select(CaddyfileParameter).where(
            CaddyfileParameter.block == "forward_proxy_parameter"
        )
    ).all()
    reverse_proxy_h = session.scalars(
        select(CaddyfileParameter).where(
            CaddyfileParameter.block == "reverse_proxy_header"
        )
    ).all()
    reverse_proxy_p = session.scalars(
        select(CaddyfileParameter).where(
            CaddyfileParameter.block == "reverse_proxy_parameter"
        )
    ).all()

    if not reverse_proxy_h:
        logger.warning("reverse proxy header not found in config")
        return
    picked_reverse_proxy_h = secrets.choice(reverse_proxy_h)

    result = template.safe_substitute(
        gobal_parameters="\n  ".join(f"{p.parameter} {p.value}" for p in global_p),
        site_headers=", ".join(f"{h.domain}:{h.port}" for h in site_h),
        site_parameters="\n  ".join(f"{p.parameter} {p.value}".strip() for p in site_p),
        users="\n        ".join(f"basic_auth {u.login} {decrypt(u.password)}" for u in users),
        forward_proxy_parameters="\n        ".join(
            f"{p.parameter} {p.value}" for p in forward_proxy_p
        ),
        reverse_proxy_header=picked_reverse_proxy_h.value,
        reverse_proxy_parameters="\n      ".join(
            f"{p.parameter} {p.value}" for p in reverse_proxy_p
        ),
    )

    return result
