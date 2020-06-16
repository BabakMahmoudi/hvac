

We will use the 'Bom Structure' report to show the bom structure of the
manufacturing project.
The standard report is designed to show the structure of a single 'bom' 
while in our case we have multiple products in our project and want 
to show a bom including those products. Therefore we need to override the default 
functionality. We could use 2 approaches fo this override:

1. Light Approach:
In this approach we only override the model of the report, all other assets (such as js files),
will be kept untouched:
    class ReportHvacBomExtensions(models.AbstractModel):
    _inherit = 'report.mrp.report_bom_structure'

    def get_bom(self):
        pass
    def get_html(self, bom_id=False, searchQty=1, searchVariant=False):
        return ""
here we may override those methods to provide the required functionalities.

2. Complete override:
In this approach we will override the whole reporting system including the assets and 
model. 
To do so:
    * We make a complete copy of the 'mrp' static folder to reuse the existing codes and css.
    * We copy the report folder from 'mrp' to get a copy of the existing models.
    * In the manifest file we load the report:
         'data': [
             ...
        'report/mrp_report_bom_structure.xml'
        ],
        # only loaded in demonstration mode
        'qweb': ['static/src/xml/mrp.xml'],
    * In our template file we will add the assets:
            <template id="assets_backend" name="mrp assets" inherit_id="web.assets_backend">
            <xpath expr="." position="inside">
                <!-- already loaded
                <link rel="stylesheet" type="text/scss" href="/mrp/static/src/scss/mrp_workorder_kanban.scss" />
                
                <script type="text/javascript" src="/mrp/static/src/js/mrp.js"></script>
                -->
                <script type="text/javascript" src="/hvac_mrp_project/static/src/js/mrp_bom_report.js"></script>
            </xpath>
            </template>

            <template id="assets_common" name="mrp bom common assets" inherit_id="web.assets_common">
            <xpath expr="." position="inside">
                <!-- already loaded 
                <link rel="stylesheet" type="text/scss" href="/mrp/static/src/scss/mrp_bom_report.scss" />
                <link rel="stylesheet" type="text/scss" href="/mrp/static/src/scss/mrp_fields.scss" />
                <link rel="stylesheet" type="text/scss" href="/mrp/static/src/scss/mrp_gantt.scss" />
                -->
            </xpath>
            </template>
    * Finally in view file (project_view.xml), we will refer to our action 'mrp_bom_hvac_report'
        <record id="action_report_mrp_hvac_bom" model="ir.actions.client">
        <field name="name">BoM Structure &amp; Cost</field>
        <!--
            We have two modes
        <field name="tag">mrp_bom_report</field>
        -->
        <field name="tag">mrp_bom_hvac_report</field>
        
        <field name="context" eval="{'model': 'report.mrp.hvac.report_bom_structure'}" />
        </record>
    * This client action is actually defined in the 'mrp_bom_report.js':
        
            core.action_registry.add('mrp_bom_hvac_report', MrpBomReport);
            return MrpBomReport;

            });
    * We will also change the above js file to use our own model
        return this._rpc({
                    // Change our model 
                    //model: 'report.mrp.report_bom_structure',
                    model: 'report.mrp.hvac.report_bom_structure', 
                    method: 'get_html',
                    args: args,
                    context: this.given_context,
                })
                .then(function (result) {
                    self.data = result;
                });


We will try to use the 'Light' version as far as it works in our case. We may later switch 
to complete version, it there be required features that can not be supported by the 'Light' 
approach. To switch we should only edit the tag in 'hvac_mrp_project_views'
      <!-- 
        We may switch modes by using the appopriate tag
        field.
        Light mode : <field name="tag">mrp_bom_report</field>
        Compelet mode:<field name="tag">mrp_bom_hvac_report</field>
      -->
      <field name="tag">mrp_bom_report</field>
