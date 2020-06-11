from odoo import models, fields, api

def doThis():
    print ('hey')

class HvacUtils(models.TransientModel):
    _name = "hvac.utils"
    _project_attribute_name = 'Project'
    _default_project_attribute_value = 'P_000'

    def test(self):
        
        product_tmpl = self.env['product.template'].search(
            [('name', '=', 'SAMPLE 6')])
        attib = self.getProjectAttribute()
        values = self.getProjectAttributeValues()
        default_value = self.getDefaultProjectAttributeValue(True)
        #product_tmpl = self.createProjectProductTemplate("SAMPLE 6")
        product = self.createProjectProductVariant(product_tmpl, "P_001")
        for value in values:
            print(value)

    def getProjectAttribute(self, auto_create=True):
        result = self.env['product.attribute'].search(
            [('name', '=', self._project_attribute_name)])
        if (not result and auto_create):
            result = self.env['product.attribute'].create(
                [{
                    'name': self._project_attribute_name,
                    #'create_variant': 'dynamic'
                }])
            #result.create_variant = 'no_variant'
        return result

    def getProjectAttributeValues(self, auto_create=True):
        attribute = self.getProjectAttribute(auto_create)
        result = attribute.value_ids
        default_attrib = result.search([('name', "=", "jj")])
        return result

    def getProjectAttributeValue(self, project_code, auto_create=True):
        attribute = self.getProjectAttribute(auto_create)
        existing = attribute.value_ids.search(
            [('name', '=', project_code), ('attribute_id', '=', attribute.id)])
        result = False
        if existing and len(existing) > 0:
            result = existing[0]
        else:
            result = self.env['product.attribute.value'].create({
                'name': project_code,
                'attribute_id': attribute.id,
                'sequence': 1, })
        return result

    def getDefaultProjectAttributeValue(self, auto_create=True):
        result = False
        project_attribute = self.getProjectAttribute(auto_create)
        if project_attribute:
            result = project_attribute.value_ids.search(
                [('name', "=", self._default_project_attribute_value)])
            if not result and auto_create:
                self.env['product.attribute.value'].create({
                    'name': self._default_project_attribute_value,
                    'attribute_id': project_attribute.id,
                    'sequence': 1, })
        return result

    """
        Make sure if the template has the 'project variant line' and also
        this variant includes all projects. So that we can create products 
        with the project variant in this template. 
    """

    def ensureProjectAttributeIsSelectedOnProductTemplate(self, product_tmpl, proj_code):
        attrib = self.getProjectAttribute()
        value_id = self.getProjectAttributeValue(proj_code)
        if product_tmpl:
            project_line = self.env['product.template.attribute.line'].search([
                ("attribute_id", "=", attrib.id), ("product_tmpl_id", "=", product_tmpl.id)])
            if not project_line:
                project_line = self.env['product.template.attribute.line'].create({
                    'product_tmpl_id': product_tmpl.id,
                    'attribute_id': attrib.id,
                    'value_ids': [(6, 0, [value_id.id])], })
            else:
                project_line.value_ids = project_line.value_ids.concat(value_id)
        print('hhhh')
        return product_tmpl
                



    def ensureProjectAttributeLineOnProjectTemplate(self, produc_tmpl):
        attrib = self.getProjectAttribute()
        default_value = self.getDefaultProjectAttributeValue()
        all_values = self.getProjectAttributeValues()
        if produc_tmpl:
            project_line = self.env['product.template.attribute.line'].search([
                ("attribute_id", "=", attrib.id), ("product_tmpl_id", "=", produc_tmpl.id)])
            if not project_line:
                project_line = self.env['product.template.attribute.line'].create({
                    'product_tmpl_id': produc_tmpl.id,
                    'attribute_id': attrib.id,
                    'value_ids': [(6, 0, all_values.ids)], })
            else:
                project_line.value_ids = [(6, 0, all_values.ids)]
            # for value in self.getProjectAttributeValues():
            #     if not self.env['product.template.attribute.value'].search([
            #             ('attribute_line_id', "=", project_line.id),
            #             ('product_attribute_value_id', "=", value.id)]):
            #         self.env['product.template.attribute.value'].create([
            #             {'attribute_line_id': project_line.id, 'product_attribute_value_id': value.id}])
        return produc_tmpl

    # def createProjectAttribute(self):
    #     result = self.getProjectAttribute()
    #     if not result:
    #         result = self.env['product.attribute'].create(
    #             [{
    #                 'name': self._project_attribute_name,
    #                 'create_variant':'always'
    #                 }])
    #         #result.create_variant = 'no_variant'
    #         #result.create_variant = 'always'
    #     return result

    """
        Creates a new project product template.
        Project products has the 'Project' variant attribute.
    """

    def createProjectProductTemplate(self, name):
        product_tmpl = self.env['product.template'].search(
            [('name', '=', name)])
        if not product_tmpl:
            product_tmpl = self.env['product.template'].create(
                [{'name': name}])
        self.ensureProjectAttributeLineOnProjectTemplate(product_tmpl)
        return product_tmpl

    def createProjectProductVariant(self, product_tmpl, project_name):
        result = False
        attrib = self.getProjectAttribute()
        _line = False
        _value = False

        for line in product_tmpl.valid_product_template_attribute_line_ids:
            if (line.attribute_id == attrib):
                _line = line
        if _line:
            for val in _line.product_template_value_ids:
                if val.name == project_name:
                    _value = val

        if _value:
            result = product_tmpl._create_product_variant(_value)
            # result = self.env['product.product'].create([{
            # 'product_tmpl_id': product_tmpl.id,
            # 'product_template_attribute_value_ids': [(6, 0, [_value.id])]
            # }])
        return result

    def projectAttributeValueExists(self, projectCode):
        self.env['product.attribute'].search()

    def getVariantProjectName(self, product):
        attributes = self.env['product.attribute.value'].search([])
        project_attribute = self.env['product.attribute'].search(
            [('name', '=', self._project_attribute_name)])

        return False
    
    def forkBom(self, bom_id, project):
        if type(project)=='str':
            project = self.getProjectAttributeValue(project)
        
