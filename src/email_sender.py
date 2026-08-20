"""Cloud Function: SMTP-отправка для workflow авто-эскалации.

YaWL умеет вызывать HTTP (httpCall), но не умеет отправлять почту напрямую —
поэтому шаг эскалации ходит сюда. Функция принимает JSON {to, subject, body}
и отправляет письмо тем же ящиком, что и поллер (тот же Lockbox-секрет с
паролем можно переиспользовать при деплое).
"""

from __future__ import annotations

import json
import os
import smtplib
import ssl
from email.message import EmailMessage
from typing import Any


def _env(name: str, default: str | None = None) -> str:
    value = os.environ.get(name, default)
    if value is None:
        raise RuntimeError(f"missing required env var: {name}")
    return value


def handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    raw_body = event.get("body") or "{}"
    if isinstance(raw_body, (bytes, bytearray)):
        raw_body = raw_body.decode("utf-8")
    try:
        payload = json.loads(raw_body) if raw_body else {}
    except json.JSONDecodeError as error:
        return {"statusCode": 400, "body": json.dumps({"error": f"invalid json: {error}"})}

    to_address = payload.get("to")
    subject = payload.get("subject") or "(без темы)"
    text = payload.get("body") or payload.get("text") or ""
    if not to_address:
        return {"statusCode": 400, "body": json.dumps({"error": "'to' is required"})}

    message = EmailMessage()
    message["From"] = _env("SMTP_USER")
    message["To"] = to_address
    message["Subject"] = subject
    message.set_content(text)

    context_ssl = ssl.create_default_context()
    with smtplib.SMTP_SSL(_env("SMTP_HOST", "smtp.yandex.ru"), int(_env("SMTP_PORT", "465")), context=context_ssl, timeout=30) as smtp:
        smtp.login(_env("SMTP_USER"), _env("SMTP_PASSWORD"))
        smtp.send_message(message)

    print(f"[email-sender] sent to={to_address!r} subject={subject!r} chars={len(text)}")
    return {"statusCode": 200, "body": json.dumps({"ok": True, "to": to_address})}
