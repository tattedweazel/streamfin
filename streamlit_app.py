import streamlit as st

from modules.sidenav import get_sidebar


# --- Sidenav ---
pg = get_sidebar()
pg.run()

