"""Check the admin login in THIS terminal, the same way the website does (Sprint 4).

Shows where the admin account is read from (.env or environment variables) and which
part does not match. Never prints the password. Usage from the project root:
    .venv\\Scripts\\python.exe scripts\\check_admin_login.py
"""

import getpass
import os
import sys
from pathlib import Path

from dotenv import dotenv_values

from pekael.config.app_configurator import DEFAULT_ENV_FILE, AppConfigurator
from pekael.services.admin_auth import AdminAuthenticator


def main() -> int:
    env_file = DEFAULT_ENV_FILE.resolve()
    print(f"Folder kerja  : {Path.cwd()}")
    print(f"File .env     : {env_file} ({'ada' if env_file.is_file() else 'TIDAK ADA'})")
    file_values = dotenv_values(env_file) if env_file.is_file() else {}
    for name in ("ADMIN_USERNAME", "ADMIN_PASSWORD"):
        if name in os.environ:
            same = os.environ[name] == (file_values.get(name) or "")
            print(f"{name:15}: dari VARIABEL LINGKUNGAN terminal ({'sama dengan' if same else 'BERBEDA dari'} .env)")
        else:
            print(f"{name:15}: dari .env ({'terisi' if file_values.get(name) else 'kosong'})")

    config = AppConfigurator.read_config()
    if not config.admin_enabled:
        print("\nLogin admin NONAKTIF: nama pengguna atau kata sandi belum diatur.")
        return 1
    username = input("\nNama pengguna : ")
    password = getpass.getpass("Kata sandi    : ")
    auth = AdminAuthenticator(config.admin_username, config.admin_password)
    expected_user = (config.admin_username or "").strip().casefold()
    print(f"Nama pengguna cocok : {'ya' if username.strip().casefold() == expected_user else 'TIDAK'}")
    print(f"Kata sandi cocok    : {'ya' if auth.verify(config.admin_username, password) else 'TIDAK'}"
          f" (panjang yang diketik {len(password.strip())}, yang diatur {len(config.admin_password.get_secret_value().strip())})")
    ok = auth.verify(username, password)
    print("\nHASIL:", "BERHASIL, login di website seharusnya diterima." if ok else "DITOLAK.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
