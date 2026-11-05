"""Streamlit entry point (client in the class diagram).

Two pages: the student page at / and the admin room at /admin (not listed in a menu).
Run from the project root:
    .venv\\Scripts\\streamlit.exe run app.py
"""

import streamlit as st

from pekael.ui import admin_page, student_page

st.set_page_config(page_title="Pekael · Informasi PKL PTIK UNJ", page_icon=":material/menu_book:", layout="centered")
navigation = st.navigation(
    [
        st.Page(student_page.main, title="Pekael", url_path="", default=True),
        st.Page(admin_page.main, title="Ruang admin · Pekael", url_path="admin"),
    ],
    position="hidden",
)
navigation.run()
