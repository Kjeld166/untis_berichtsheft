#!/usr/bin/env python3
import argparse
import base64
import json
import os
import socket
import time
from typing import Iterable, List, Tuple

import requests


def prompt_or_env(name: str, default: str = "") -> str:
    value = os.getenv(name)
    if value is not None and value != "":
        return value
    if default != "":
        return default
    return input(f"{name}: ").strip()


def try_dns(host: str):
    try:
        info = socket.gethostbyname_ex(host)
        print(f"DNS OK: {host} -> {info[2]}")
        return True
    except Exception as exc:
        print(f"DNS FAIL: {host} -> {exc}")
        return False


def try_http_get(url: str, timeout: int = 15) -> Tuple[bool, str, int]:
    try:
        start = time.time()
        r = requests.get(url, timeout=timeout)
        elapsed = time.time() - start
        print(f"GET {url} -> {r.status_code} in {elapsed:.2f}s")
        return True, r.text[:300], r.status_code
    except requests.exceptions.Timeout:
        print(f"GET TIMEOUT {url}")
        return False, "timeout", 0
    except Exception as exc:
        print(f"GET ERROR {url} -> {type(exc).__name__}: {exc}")
        return False, str(exc), 0


def try_auth(url: str, school_short: str, username: str, password: str, timeout: int = 20) -> Tuple[bool, str, dict]:
    payload = {
        "id": "auth",
        "method": "authenticate",
        "jsonrpc": "2.0",
        "params": {"user": username, "password": password, "client": "diagnose"},
    }
    try:
        start = time.time()
        r = requests.post(
            f"{url}/WebUntis/jsonrpc.do?school={school_short}",
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=timeout,
        )
        elapsed = time.time() - start
        print(f"POST jsonrpc.do -> {r.status_code} in {elapsed:.2f}s")
        print(r.text[:500])
        return r.ok, r.text[:500], r.json() if r.content else {}
    except requests.exceptions.Timeout:
        print(f"AUTH TIMEOUT: {url}/WebUntis/jsonrpc.do?school={school_short}")
        return False, "timeout", {}
    except Exception as exc:
        print(f"AUTH ERROR: {type(exc).__name__}: {exc}")
        return False, str(exc), {}


def try_token(session_id: str, url: str, school_short: str, timeout: int = 20) -> Tuple[bool, str]:
    try:
        cookie_value = f'JSESSIONID={session_id};schoolname="{base64.b64encode(("#" + school_short).encode()).decode().rstrip("=")}"'
        r = requests.get(
            f"{url}/WebUntis/api/token/new",
            headers={"Accept": "application/json", "Cookie": cookie_value},
            timeout=timeout,
        )
        print(f"TOKEN GET -> {r.status_code}: {r.text[:200]}")
        return r.ok, r.text[:200]
    except requests.exceptions.Timeout:
        print(f"TOKEN TIMEOUT: {url}/WebUntis/api/token/new")
        return False, "timeout"
    except Exception as exc:
        print(f"TOKEN ERROR: {type(exc).__name__}: {exc}")
        return False, str(exc)


def parse_year_ids(raw: str) -> List[str]:
    if not raw:
        return ["29", "30", "31", "32"]
    out: List[str] = []
    for item in raw.split(","):
        value = item.strip()
        if value:
            out.append(value)
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Diagnose WebUntis connectivity and auth behavior")
    parser.add_argument("--url", default="https://bszet.webuntis.com")
    parser.add_argument("--school", default="bszet")
    parser.add_argument("--user", default="")
    parser.add_argument("--password", default="")
    parser.add_argument("--year-ids", default="29,30,31,32")
    args = parser.parse_args()

    url = args.url or prompt_or_env("WEBUNTIS_URL", "https://bszet.webuntis.com")
    school = args.school or prompt_or_env("WEBUNTIS_SCHOOL", "bszet")
    user = args.user or prompt_or_env("WEBUNTIS_USER", "")
    password = args.password or prompt_or_env("WEBUNTIS_PASSWORD", "")
    year_ids = parse_year_ids(args.year_ids)

    print("=== DNS ===")
    host = url.replace("https://", "").replace("http://", "").split("/", 1)[0]
    try_dns(host)

    print("\n=== BASE URL CHECK ===")
    try_http_get(url, timeout=15)

    print("\n=== AUTH CHECK ===")
    ok, text, data = try_auth(url, school, user, password, timeout=20)
    if ok and isinstance(data, dict):
        result = data.get("result") or {}
        session_id = result.get("sessionId")
        if session_id:
            print(f"Received sessionId: {session_id}")
            print("\n=== TOKEN CHECK ===")
            try_token(session_id, url, school, timeout=20)
        else:
            print("No sessionId returned; auth probably failed.")

    print("\n=== YEAR ID CANDIDATES ===")
    for year_id in year_ids:
        print(f"Candidate year id: {year_id}")
        try:
            r = requests.get(
                f"{url}/WebUntis/api/rest/view/v2/years",
                headers={"Accept": "application/json", "X-Webuntis-Api-School-Year-Id": year_id},
                timeout=15,
            )
            print(f"Status: {r.status_code} :: {r.text[:200]}")
        except requests.exceptions.Timeout:
            print("TIMEOUT for year id candidate")
        except Exception as exc:
            print(f"ERROR for year id {year_id}: {type(exc).__name__}: {exc}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
