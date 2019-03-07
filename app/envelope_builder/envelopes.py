# Copyright 2019 Jacques Supcik
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This module generates the envelopes"""


import datetime
import pathlib
import re

import jinja2
import weasyprint


@jinja2.evalcontextfilter
def nl2br(eval_ctx, value):
    """nl2br converts line breaks to <br> tags"""
    result = u'\n\n'.join(u'<p>%s</p>' % p.replace('\n', jinja2.Markup('<br>\n'))
                          for p in Envelopes.paragraph_re.split(jinja2.escape(value)))
    if eval_ctx.autoescape:
        result = jinja2.Markup(result)
    return result


class Envelopes:
    """Envelopes is the class for envelopes"""

    paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')

    def __init__(self, year=datetime.datetime.now().year):
        self.year = year
        self.classes = list()

    def add_class(self, clas):
        """add_class adds a class to classes list"""
        self.classes.append(clas)

    def make_pdf(self, dst_file):
        """make_pdf generates the PDF"""
        base = pathlib.Path(__file__).parent.absolute()
        env = jinja2.Environment(
            loader=jinja2.PackageLoader(__name__, 'templates'),
            autoescape=jinja2.select_autoescape(['html', 'xml'])
        )
        env.filters['nl2br'] = nl2br
        template = env.get_template('env.html')

        envelopes = list()
        for clas in self.classes:
            for i in range(clas.number):
                envelopes.append(
                    {
                        'name': clas.name,
                        'class': clas.clas,
                        'table': clas.table,
                        'rank': i + 1,
                    }
                )

        html = template.render(
            year=self.year,
            envelopes=envelopes,
        )
        weasyprint.HTML(
            string=html,
            base_url=str(base),
        ).write_pdf(
            target=dst_file,
            stylesheets=[weasyprint.CSS(base.joinpath("assets", "env.css"))],
        )
