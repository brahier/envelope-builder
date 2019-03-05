import datetime
import json
import pathlib
import re
from io import BytesIO

import jinja2
import weasyprint


@jinja2.evalcontextfilter
def nl2br(eval_ctx, value):
    result = u'\n\n'.join(u'<p>%s</p>' % p.replace('\n', jinja2.Markup('<br>\n'))
                          for p in Envelopes._paragraph_re.split(jinja2.escape(value)))
    if eval_ctx.autoescape:
        result = jinja2.Markup(result)
    return result


class Envelopes:

    _paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')

    def __init__(self, year=datetime.datetime.now().year):
        self.year = year
        self.classes = list()

    def addClass(self, clas):
        self.classes.append(clas)

    def makePdf(self, dstFile):
        base = pathlib.Path(__file__).parent.absolute()
        env = jinja2.Environment(
            loader=jinja2.PackageLoader(__name__, 'templates'),
            autoescape=jinja2.select_autoescape(['html', 'xml'])
        )
        env.filters['nl2br'] = nl2br
        template = env.get_template('env.html')

        envelopes = list()
        for c in self.classes:
            for i in range(c.number):
                envelopes.append(
                    {
                        'name': c.name,
                        'class': c.clas,
                        'table': c.table,
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
            target=dstFile,
            stylesheets=[weasyprint.CSS(base.joinpath("assets", "env.css"))],
        )
