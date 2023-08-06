# -*- coding: UTF-8 -*-
# Copyright 2014-2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

ATELIER_INFO = dict(
    nickname="cosi",
    verbose_name="Lino Così",
    # srcref_url='https://gitlab.com/lino-framework/cosi/blob/master/%s',
    intersphinx_urls = dict(
        docs="https://cosi.lino-framework.org",
        dedocs="https://cosi.lino-framework.org/de/"))

SETUP_INFO = dict(
    name='lino-cosi',
    version='22.6.0',
    install_requires=['lino-xl', 'django-iban', 'lxml'],
    # tests_require=['beautifulsoup4'],  # satisfied by lino deps
    test_suite='tests',
    description="A Lino Django application for basic sales and accounting.",
    author='Rumma & Ko Ltd',
    author_email='info@lino-framework.org',
    url="https://gitlab.com/lino-framework/cosi",
    license_files=['COPYING'],
    classifiers="""\
Programming Language :: Python
Programming Language :: Python :: 3
Development Status :: 5 - Production/Stable
Environment :: Web Environment
Framework :: Django
Intended Audience :: Developers
Intended Audience :: System Administrators
License :: OSI Approved :: GNU Affero General Public License v3
Operating System :: OS Independent
Topic :: Office/Business :: Financial :: Accounting
""".splitlines())

SETUP_INFO.update(long_description="""

- More about {verbose_name}:
  https://{nickname}.lino-framework.org

- Source code:
  https://gitlab.com/lino-framework/{nickname}

- Demo sites:
  https://www.lino-framework.org/demos.html

- Developer specs:
  https://www.lino-framework.org/specs/{nickname}

- {verbose_name} is an integral part of the Lino framework, which is documented
  at https://www.lino-framework.org

- {verbose_name} is a sustainably free open-source project. Your contributions are
  welcome.  See https://community.lino-framework.org for details.

- Professional hosting, support and maintenance:
  https://www.saffre-rumma.net

""".format(**ATELIER_INFO))


SETUP_INFO.update(packages=[
    'lino_cosi',
    'lino_cosi.lib',
    'lino_cosi.lib.cosi',
    'lino_cosi.lib.contacts',
    'lino_cosi.lib.contacts.fixtures',
    'lino_cosi.lib.contacts.management',
    'lino_cosi.lib.contacts.management.commands',
    'lino_cosi.lib.products',
    'lino_cosi.lib.products.fixtures',
    'lino_cosi.lib.sales',
    'lino_cosi.lib.sales.fixtures',
    'lino_cosi.lib.orders',
])

SETUP_INFO.update(message_extractors={
    'lino_cosi': [
        ('**/cache/**', 'ignore', None),
        ('**.py', 'python', None),
        ('**.js', 'javascript', None),
        ('**/templates_jinja/**.html', 'jinja2', None),
    ],
})

SETUP_INFO.update(
    # package_data=dict(),
    zip_safe=False,
    include_package_data=True)


# def add_package_data(package, *patterns):
#     l = SETUP_INFO['package_data'].setdefault(package, [])
#     l.extend(patterns)
#     return l


# ~ add_package_data('lino_cosi',
# ~ 'config/patrols/Patrol/*.odt',
# ~ 'config/patrols/Overview/*.odt')

# l = add_package_data('lino_cosi.lib.cosi')
# for lng in 'de fr'.split():
#     l.append('lino_cosi/lib/cosi/locale/%s/LC_MESSAGES/*.mo' % lng)

# l = add_package_data('lino_xl.lib.sepa',
#                      'lino_xl.lib/sepa/config/iban/*')
                     # 'config/iban/*')
# print 20160820, SETUP_INFO['package_data']
# raw_input()
