from flask import render_template, redirect, url_for, request, session
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound
import logging

from app.home import blueprint
import app.service.service as service
import app.service.ontology as ontology


@blueprint.route('/')
def route_default():
    return redirect(url_for('home_blueprint.route_scotland'))


@blueprint.route('/scotland')
def route_scotland():
    print('route_scotland:')

    page_data = ontology.get_page_by_name('scotland')

    print('route_template_vis: page_data = ', page_data)

    try:
        return render_template('scotland.html', option=page_data)

    except TemplateNotFound:
        return render_template('page-404.html'), 404

    except:
        return render_template('page-500.html'), 500


@blueprint.route('/portal')
def route_portal():
    if not current_user.is_authenticated:
        return redirect(url_for('base_blueprint.route_login'))

    result = service.get_bookmarks()
    return render_template('portal.html', option=result)


@blueprint.route('/dashboards')
def route_dashboards():
    print('dashboards:')
    try:
        table = ontology.get_pages_by_type('dashboard')
        print('dashboards: data = ', table)
        return render_template('dashboards.html', table=table)

    except TemplateNotFound:
        return render_template('page-404.html'), 404

    except:
        return render_template('page-500.html'), 500


@blueprint.route('/plots')
def route_plots():
    print('plots:')

    try:
        table = ontology.get_pages_by_type('plot')
        print('plots: data = ', table)
        return render_template('plots.html', table=table)

    except TemplateNotFound:
        return render_template('page-404.html'), 404

    except:
        return render_template('page-500.html'), 500


@blueprint.route('/analytics')
def route_analytics():
    print('analytics:')

    try:
        table = ontology.get_pages_by_type('analytics')
        print('plots: data = ', table)
        return render_template('analytics.html', table=table)

    except TemplateNotFound:
        return render_template('page-404.html'), 404

    except:
        return render_template('page-500.html'), 500


@blueprint.route('/models')
def route_models():
    print('route_models:')

    try:
        table = ontology.get_pages_by_type('model')
        print('models: data = ', table)
        return render_template('plots.html', table=table)

    except TemplateNotFound:
        return render_template('page-404.html'), 404

    except:
        return render_template('page-500.html'), 500


@blueprint.route('/search', methods=['GET'])
def route_search():
    query = request.args.get('query')
    print('route_search: search: query = ', query)

    if query:
        result = service.search(query)
        return render_template('search.html', data={'query': query, 'result': result})

    return render_template('search.html', data={})


@blueprint.route('/settings', methods=['GET'])
@login_required
def route_settings():
    print('route_settings:')
    print('route_settings: token = ', session.get('token '))

    try:
        return render_template('settings.html')

    except TemplateNotFound:
        return render_template('page-404.html'), 404

    except:
        return render_template('page-500.html'), 500


@blueprint.route('/profile')
@login_required
def profile():
    if not current_user.is_authenticated:
        return redirect(url_for('base_blueprint.route_login'))

    return render_template('profile.html')


@blueprint.route('v05')
def route_v05():
    print('route_v05')
    try:
        table = ontology.get_all_pages()
        print('route_pages_v0.5: page_data = ', table)
        return render_template('pages-table-1.html', table=table)

    except TemplateNotFound:
        return render_template('page-404.html'), 404

    except:
        return render_template('page-500.html'), 500


#
# V.1+ released and test/development pages
#


@blueprint.route('/released')
@blueprint.route('/review')
@blueprint.route('/example')
def route_pages():
    url_prefix = request.url_rule.rule.replace('/', '')
    logging.debug(f'routes.py:route_pages: binding_type = {url_prefix}')
    try:
        onto_pages = service.get_onto_pages(url_prefix)
        print('route_released_pages: onto_pages = ', onto_pages)
        return render_template('pages-table-2.html', table=onto_pages, publishType=url_prefix)
    except TemplateNotFound:
        return render_template('page-404.html'), 404
    except:
        return render_template('page-500.html'), 500


@blueprint.route('/<id_or_name>')
def route_page(id_or_name):
    logging.debug(f'routes.py:route_page: id_or_name = {id_or_name}')

    if id_or_name == 'page-blank':
        return render_template('page-blank.html')

    # check if the page name exist in local ontology
    page_data = ontology.get_page_by_name(id_or_name)
    if page_data is not None:
        logging.debug(f'routes.py:route_page: local ontology page_data = {page_data}')
        try:
            return render_template('template-1.html', option=page_data)
        except TemplateNotFound:
            logging.error(f'routes.py:route_page: exception1 = TemplateNotFound')
            return render_template('page-404.html'), 404
        except Exception as e:
            logging.error(f'routes.py:route_page: exception1 = {e}')
            return render_template('page-500.html'), 500

    elif page_data is None:
        # page_data = None, i.e.,
        # check if the page id exist in ontology database
        page_data = service.get_onto_page_by_id(id_or_name)
        logging.debug(f'routes.py:route_page: page_data = {page_data}')
        try:
            return render_template('template-2.html', option=page_data)
        except TemplateNotFound:
            logging.error(f'routes.py:route_page: exception2 = TemplateNotFound')
            return render_template('page-404.html'), 404
        except Exception as e:
            logging.error(f'routes.py:route_page: exception2 = {e}')
            return render_template('page-500.html'), 500
