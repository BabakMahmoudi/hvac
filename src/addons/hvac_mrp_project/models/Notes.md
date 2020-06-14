
About product variants:

There are 4 models for variants:
    "product.attribute"         : Product attributes 
    "product.attribute.value"   : Product attribute values
    "product.template.attribute.line"
    "product.template.attribute.value"
    "product.template.attribute.exclusion"

Following sample from D:\source\github\odoo-13.0\addons\product\tests\test_product_attribute_value_config.py
shows how to create product variants 
class TestProductAttributeValueSetup(TransactionCase):
    def setUp(self):
        super(TestProductAttributeValueSetup, self).setUp()

        self.computer = self.env['product.template'].create({
            'name': 'Super Computer',
            'price': 2000,
        })

        self._add_ssd_attribute()
        self._add_ram_attribute()
        self._add_hdd_attribute()

        self.computer_case = self.env['product.template'].create({
            'name': 'Super Computer Case'
        })

        self._add_size_attribute()

    def _add_ssd_attribute(self):
        self.ssd_attribute = self.env['product.attribute'].create({'name': 'Memory', 'sequence': 1})
        self.ssd_256 = self.env['product.attribute.value'].create({
            'name': '256 GB',
            'attribute_id': self.ssd_attribute.id,
            'sequence': 1,
        })
        self.ssd_512 = self.env['product.attribute.value'].create({
            'name': '512 GB',
            'attribute_id': self.ssd_attribute.id,
            'sequence': 2,
        })

        self._add_ssd_attribute_line()

    def _add_ssd_attribute_line(self):
        self.computer_ssd_attribute_lines = self.env['product.template.attribute.line'].create({
            'product_tmpl_id': self.computer.id,
            'attribute_id': self.ssd_attribute.id,
            'value_ids': [(6, 0, [self.ssd_256.id, self.ssd_512.id])],
        })
        self.computer_ssd_attribute_lines.product_template_value_ids[0].price_extra = 200
        self.computer_ssd_attribute_lines.product_template_value_ids[1].price_extra = 400

    def _add_ram_attribute(self):
        self.ram_attribute = self.env['product.attribute'].create({'name': 'RAM', 'sequence': 2})
        self.ram_8 = self.env['product.attribute.value'].create({
            'name': '8 GB',
            'attribute_id': self.ram_attribute.id,
            'sequence': 1,
        })
        self.ram_16 = self.env['product.attribute.value'].create({
            'name': '16 GB',
            'attribute_id': self.ram_attribute.id,
            'sequence': 2,
        })
        self.ram_32 = self.env['product.attribute.value'].create({
            'name': '32 GB',
            'attribute_id': self.ram_attribute.id,
            'sequence': 3,
        })
        self.computer_ram_attribute_lines = self.env['product.template.attribute.line'].create({
            'product_tmpl_id': self.computer.id,
            'attribute_id': self.ram_attribute.id,
            'value_ids': [(6, 0, [self.ram_8.id, self.ram_16.id, self.ram_32.id])],
        })
        self.computer_ram_attribute_lines.product_template_value_ids[0].price_extra = 20
        self.computer_ram_attribute_lines.product_template_value_ids[1].price_extra = 40
        self.computer_ram_attribute_lines.product_template_value_ids[2].price_extra = 80

    def _add_hdd_attribute(self):
        self.hdd_attribute = self.env['product.attribute'].create({'name': 'HDD', 'sequence': 3})
        self.hdd_1 = self.env['product.attribute.value'].create({
            'name': '1 To',
            'attribute_id': self.hdd_attribute.id,
            'sequence': 1,
        })
        self.hdd_2 = self.env['product.attribute.value'].create({
            'name': '2 To',
            'attribute_id': self.hdd_attribute.id,
            'sequence': 2,
        })
        self.hdd_4 = self.env['product.attribute.value'].create({
            'name': '4 To',
            'attribute_id': self.hdd_attribute.id,
            'sequence': 3,
        })

        self._add_hdd_attribute_line()

    def _add_hdd_attribute_line(self):
        self.computer_hdd_attribute_lines = self.env['product.template.attribute.line'].create({
            'product_tmpl_id': self.computer.id,
            'attribute_id': self.hdd_attribute.id,
            'value_ids': [(6, 0, [self.hdd_1.id, self.hdd_2.id, self.hdd_4.id])],
        })
        self.computer_hdd_attribute_lines.product_template_value_ids[0].price_extra = 2
        self.computer_hdd_attribute_lines.product_template_value_ids[1].price_extra = 4
        self.computer_hdd_attribute_lines.product_template_value_ids[2].price_extra = 8

    def _add_ram_exclude_for(self):
        self._get_product_value_id(self.computer_ram_attribute_lines, self.ram_16).update({
            'exclude_for': [(0, 0, {
                'product_tmpl_id': self.computer.id,
                'value_ids': [(6, 0, [self._get_product_value_id(self.computer_hdd_attribute_lines, self.hdd_1).id])]
            })]
        })

    def _add_size_attribute(self):
        self.size_attribute = self.env['product.attribute'].create({'name': 'Size', 'sequence': 4})
        self.size_m = self.env['product.attribute.value'].create({
            'name': 'M',
            'attribute_id': self.size_attribute.id,
            'sequence': 1,
        })
        self.size_l = self.env['product.attribute.value'].create({
            'name': 'L',
            'attribute_id': self.size_attribute.id,
            'sequence': 2,
        })
        self.size_xl = self.env['product.attribute.value'].create({
            'name': 'XL',
            'attribute_id': self.size_attribute.id,
            'sequence': 3,
        })
        self.computer_case_size_attribute_lines = self.env['product.template.attribute.line'].create({
            'product_tmpl_id': self.computer_case.id,
            'attribute_id': self.size_attribute.id,
            'value_ids': [(6, 0, [self.size_m.id, self.size_l.id, self.size_xl.id])],
        })

    def _get_product_value_id(self, product_template_attribute_lines, product_attribute_value):
        return product_template_attribute_lines.product_template_value_ids.filtered(
            lambda product_value_id: product_value_id.product_attribute_value_id == product_attribute_value)[0]

    def _get_product_template_attribute_value(self, product_attribute_value, model=False):
        """
            Return the `product.template.attribute.value` matching
                `product_attribute_value` for self.

            :param: recordset of one product.attribute.value
            :return: recordset of one product.template.attribute.value if found
                else empty
        """
        if not model:
            model = self.computer
        return model.valid_product_template_attribute_line_ids.filtered(
            lambda l: l.attribute_id == product_attribute_value.attribute_id
        ).product_template_value_ids.filtered(
            lambda v: v.product_attribute_value_id == product_attribute_value
        )

    def _add_exclude(self, m1, m2, product_template=False):
        m1.update({
            'exclude_for': [(0, 0, {
                'product_tmpl_id': (product_template or self.computer).id,
                'value_ids': [(6, 0, [m2.id])]
            })]
        })

