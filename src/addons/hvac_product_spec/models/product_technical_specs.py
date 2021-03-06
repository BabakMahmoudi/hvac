# -*- coding: utf-8 -*-

from odoo import models, fields, api

from typing import TYPE_CHECKING
if TYPE_CHECKING :
    from odoo.addons.product.models.product_template import ProductTemplate
else:
    ProductTemplate = models.Model


class technical_specs(ProductTemplate):
    _inherit = 'product.template'

    hvac_spec_computed_des = fields.Text(compute="compute_description")
    hvac_spec_manual_des = fields.Text()
    hvac_spec_type = fields.Selection([('value1', 'MAU'), ('value2', 'ENC'), (
        'value3', 'Door'), ('value4', 'Exhaust Fan'), ('value5', 'Control Panel')])
    
    # ENC Fields

    hvac_spec_enc_dimension_length = fields.Integer()
    hvac_spec_enc_dimension_width = fields.Integer()
    hvac_spec_enc_dimension_height = fields.Integer()
    hvac_spec_enc_dimension_internal_height = fields.Integer()
    hvac_spec_enc_dimension_internal_width = fields.Integer()
    hvac_spec_enc_dimension_internal_length = fields.Integer()
    hvac_spec_enc_electrical_supply_voltage = fields.Boolean()
    havc_spec_enc_number_of_ligths = fields.Integer()
    hvac_spec_enc_light_type = fields.Selection(
        [('value1', 'value 1'), ('value2', 'value 2')])

    # Control Panel Fields

    havc_spec_cp_model_number = fields.Selection(
        [('value1', 'value 1'), ('value2', 'value 2')])
    hvac_spec_cp_electrical_supply_voltage = fields.Selection(
        [('value1', 'value 1'), ('value2', 'value 2')])
    hvac_spec_cp_number_of_exhaust_fan = fields.Integer()
    hvac_spec_cp_number_of_mau = fields.Integer()
    hvac_spec_cp_c1c2_interlocks = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')])
    hvac_spec_cp_intrinsically_safe = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')])
    hvac_spec_cp_number_of_feeds = fields.Integer()
    hvac_spec_cp_pneumatic_doors = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')])
    hvac_spec_cp_remote_access_device = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')])

    # Door Fields

    hvac_spec_door_type = fields.Selection([('value1', 'French'), ('value2', 'Bi-Fold'), ('value3',
                                                                                          'Double Bi-Fold'), ('value4', 'Tri-Fold'), ('value5', 'Sliding'), ('value6', 'Overhead')])
    hvac_spec_door_model = fields.Selection(
        [('value1', 'value 1'), ('value2', 'value 2')])
    hvac_spec_door_opening_width = fields.Integer()
    hvac_spec_door_opening_height = fields.Integer()
    hvac_spec_door_overall_height = fields.Integer()
    hvac_spec_door_oveall_width = fields.Integer()
    hvac_spec_door_insulated = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')])
    hvac_spec_door_number_of_view_windows = fields.Integer()
    hvac_spec_door_number_of_skins = fields.Selection(
        [('value1', '1'), ('value2', '2')])
    hvac_spec_door_hinge_type = fields.Selection(
        [('value1', 'Standard'), ('value2', 'Bullet')])

    # MAU Fields

    hvac_spec_mau_type = fields.Selection(
        [('value1', 'Single Stage'), ('value2', 'Dual'), ('value3', 'Dual Recirc'), ('value4', 'Custom')])
    hvac_spec_mau_fuel_type = fields.Selection(
        [('value1', 'Nat Gas'), ('value2', 'Propane')])
    hvac_spec_mau_model_number = fields.Selection(
        [('value1', 'SNP'), ('value2', 'SPP'), ('value2', 'DNP')])
    hvac_spec_mau_electrical_supply_voltage = fields.Selection(
        [('value1', 'value 1'), ('value2', 'value 2')])
    hvac_spec_mau_cfm = fields.Integer()
    hvac_spec_mau_esp = fields.Integer()
    hvac_spec_mau_serial_number = fields.Integer()

    # Exhaust Fan Fields

    hvac_spec_exfan_model_number = fields.Selection(
        [('value1', 'SNP'), ('value2', 'SPP'), ('value2', 'DNP')])
    hvac_spec_exfan_electrical_supply_voltage = fields.Selection(
        [('value1', 'value 1'), ('value2', 'value 2')])
    hvac_spec_exfan_diameter = fields.Integer()
    hvac_spec_exfan_esp = fields.Integer()
    hvac_spec_exfan_blade_type = fields.Selection(
        [('value1', 'value 1'), ('value2', 'value 2')])
    hvac_spec_exfan_cfm = fields.Char()
    hvac_spec_exfan_hub_size = fields.Char()
    hvac_spec_exfan_hub_serial_number = fields.Char()
    hvac_spec_exfan_number_of_blades = fields.Integer()

    def get_enc_des(self):
        des = ''
        try:
            des = 'outside dimentions : {}" W x {}" L x {}" H'.format(self.hvac_spec_enc_dimension_width,self.hvac_spec_enc_dimension_length ,self.hvac_spec_enc_dimension_height) 
            des = des + '\ninside dimention : {}" W x {}" L x {}" H'.format(self.hvac_spec_enc_dimension_internal_width , self.hvac_spec_enc_dimension_internal_length,self.hvac_spec_enc_dimension_internal_height)
            
        except:
            pass
        return des 
    def get_door_des(self):
        des = ''
        try:
            des = 'dimentions : {}" W x {}" H'.format(self.hvac_spec_door_oveall_width , self.hvac_spec_door_overall_height )
        except :
            pass
        return des
    def get_mau_des(self):
        des = ''
        try:
            mau_type_dic = {'value1': 'Single Stage', 'value2': 'Dual', 'value3': 'Dual Recirc', 'value4': 'Custom'}
            mau_fuel_dic = {'value1': 'Nat Gas', 'value2': 'Propane'}
            des = "mau type : {}".format(mau_type_dic.get(self.hvac_spec_mau_type))
            des = des + "\nfuel type : {}".format(mau_fuel_dic.get(self.hvac_spec_mau_fuel_type))
        except:
            pass
        return des
    def get_bom_des(self):
        des = ''
        try:
            if self.bom_ids :
                for line in self.bom_ids.bom_line_ids:
                    des =des + '{} {}  \n {}'.format(line.product_qty ,line.product_id.name,line.product_tmpl_id.get_description())
        except:
            pass
        return des
    

    def get_description(self):
        res = ''   
        if self.hvac_spec_type and self.hvac_spec_type == "value2":
            res = self.get_enc_des()           
        if self.hvac_spec_type and self.hvac_spec_type == "value3":
            res = self.get_door_des()
        if self.hvac_spec_type and self.hvac_spec_type == "value1":
            res = self.get_mau_des()
        if self.hvac_spec_manual_des :
            res = res + "\n" + self.hvac_spec_manual_des
        res = res + "\n" + self.get_bom_des()
        self.hvac_spec_computed_des = res
        return res

    @api.depends("hvac_spec_enc_dimension_length",
        "hvac_spec_enc_dimension_width",
        "hvac_spec_enc_dimension_height",
        "hvac_spec_enc_dimension_internal_height",
        "hvac_spec_enc_dimension_internal_width",
        "hvac_spec_enc_dimension_internal_length",
        "hvac_spec_door_overall_height",
        "hvac_spec_door_oveall_width",
        "hvac_spec_mau_type")
    def compute_description(self):
        self.hvac_spec_computed_des = self.get_description() 
        
