from ftw.referencewidget import _
from ftw.referencewidget.widget import ReferenceWidgetFactory
from plone.z3cform.layout import FormWrapper
from z3c.form.button import buttonAndHandler
from z3c.form.field import Fields
from z3c.form.form import Form
from z3c.relationfield.schema import RelationList
from zope.interface import Interface


class IFormSchema(Interface):

    relation = RelationList(
        title=_(u'Relation'),
        required=False)


class TestForm(Form):
    label = u'Testform'
    ignoreContext = True
    fields = Fields(IFormSchema)

    def __init__(self, *args, **kwargs):
        super(TestForm, self).__init__(*args, **kwargs)
        self.result_data = None

    def update(self):
        self.fields['relation'].widgetFactory = ReferenceWidgetFactory
        return super(TestForm, self).update()

    @buttonAndHandler(u'Submit')
    def handle_submit(self, action):
        data, errors = self.extractData()
        if len(errors) > 0:
            return

        self.result_data = {}
        for key, value in data.items():
            if not value:
                continue

            self.result_data[key] = value


class TestView(FormWrapper):
    form = TestForm

    def render(self):
        return super(TestView, self).render()
