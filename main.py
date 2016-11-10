#!/usr/bin/env python
import os
import jinja2
import webapp2
import random


template_dir = os.path.join(os.path.dirname(__file__), "templates") # "templates" je pot do .html datoteke
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("index.html")

class LotoHandler(BaseHandler):
    def get(self):
        combination = list()
        lottoNumbers = range(1, 40)
        for i in range(7):
            number = random.choice(lottoNumbers)
            combination.append(number)
            lottoNumbers.remove(number)
        combination = sorted(combination)
        params = {"comb": combination}
        return self.render_template("loto.html", params = params)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler), # webapp2.Route(pot, handler) -> pot = neki.com/blog -> vpisemo /blog
    webapp2.Route('/loto', LotoHandler)
], debug=True) # vsaka podstran ima svoj handler, ali pa z if stavki dolocimo vse v enem MainHandler-ju
