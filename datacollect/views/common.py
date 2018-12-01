import functools
from datetime import datetime

import pandas as pd
from datacollect.dao.excel_io import import_from_df

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,jsonify
)

from datacollect.db import get_db

bp = Blueprint('common', __name__, url_prefix='/common')

@bp.route("/import", methods=["POST"])
def import_excel():
    """"""
    excel_type = request.form["excel_type"]
    file = request.files["file"]
    df = pd.read_excel(file.stream)
    updated_date = datetime.now()
    updated_by = g.user["username"]
    result = import_from_df(df, get_db(), excel_type, updated_date, updated_by)

    return jsonify(result.to_json())
