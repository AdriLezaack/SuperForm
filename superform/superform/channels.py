import ast

from flask import Blueprint, current_app, url_for, request, redirect, render_template

from superform.models import db, Channel
from superform.plugins.pdf import pdf_plugin
from superform.utils import login_required, get_instance_from_module_path, \
    get_modules_names, get_module_full_name

channels_page = Blueprint('channels', __name__)


@channels_page.route("/channels", methods=['GET', 'POST'])
@login_required(admin_required = True)
def channel_list():
    if request.method == "POST":
        action = request.form.get('@action', '')
        if action == "new":
            name = request.form.get('name')
            module = request.form.get('module')
            if module in get_modules_names(
                    current_app.config["PLUGINS"].keys()):
                channel = Channel(name=name, module=get_module_full_name(module), config="{}")
                db.session.add(channel)
                db.session.commit()
        elif action == "delete":
            channel_id = request.form.get("id")
            channel = Channel.query.get(channel_id)
            if channel:
                db.session.delete(channel)
                db.session.commit()
        elif action == "edit":
            channel_id = request.form.get("id")
            channel = Channel.query.get(channel_id)
            name = request.form.get('name')
            channel.name = name
            db.session.commit()

    channels = Channel.query.all()
    return render_template("channels.html", channels = channels,
                           modules = get_modules_names(
                               current_app.config["PLUGINS"].keys()))


@channels_page.route("/configure/<int:id>", methods=['GET', 'POST'])
@login_required(admin_required=True)
def configure_channel(id):
    c = Channel.query.get(id)
    m = c.module
    clas = get_instance_from_module_path(m)
    config_fields = clas.CONFIG_FIELDS
    if request.method == 'GET':
        if c.config is not "":
            d = ast.literal_eval(c.config)
            setattr(c, "config_dict", d)
            # TEAM06: addition for pdf feature
            if str(m) == 'superform.plugins.pdf':
                return pdf_plugin(id, c, config_fields)
            # TEAM06: end addition

        return render_template("channel_configure.html", channel=c, config_fields=config_fields)
    str_conf = "{"
    cfield = 0
    for field in config_fields:
        if cfield > 0:
            str_conf += ","

        # TEAM06: changes for the pdf feature
        if str(m) == "superform.plugins.pdf":
            if field == "Format":
                str_conf += "\"" + field + "\" : \"" + request.form['format'] + "\""
            else:
                str_conf += "\"" + field + "\" : \"" + request.form[
                    'logo'] + "\""
            print('field=%s\nstr_conf=%s' %(field,str_conf))
        else:
            str_conf += "\"" + field + "\" : \"" + request.form.get(field) + "\""
        # TEAM06: end changes
        cfield += 1
    str_conf += "}"
    c.config = str_conf
    db.session.commit()
    return redirect(url_for('channels.channel_list'))
