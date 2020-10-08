from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, DateWidget, DecimalWidget, CharWidget
from .models import Product,ProductStatus


class ProductResource(resources.ModelResource):

    pdid = fields.Field(
        column_name='PdID', # column name on file
        attribute='pdid',
        widget=CharWidget()) # attribute on table
    name = fields.Field(
        column_name='Product', # column name on file
        attribute='name',) # attribute on table
    descr1 = fields.Field(
        column_name='Descr1', # column name on file
        attribute='descr1',) # attribute on table
    descr2 = fields.Field(
        column_name='Descr2', # column name on file
        attribute='descr2',) # attribute on table
    detail = fields.Field(
        column_name='Detail', # column name on file
        attribute='detail',) # attribute on table
    remarks = fields.Field(
        column_name='Remarks', # column name on file
        attribute='remarks',) # attribute on table
    status_id = fields.Field(
        column_name='ProductStatus',
        attribute='status',
        widget=ForeignKeyWidget(ProductStatus, 'name'))
    price = fields.Field(
        column_name='Price',
        attribute='price',
        widget=DecimalWidget())
    date = fields.Field(
        column_name='TIMESTAMP',
        attribute='date',
        widget=DateWidget('%Y.%m.%d'))
    Handlager = fields.Field(
        column_name='Handlager',
        attribute='handlager',)
    lang_id = fields.Field(
        column_name='lang_id',
        attribute='lang_id',)
    weight = fields.Field(
        column_name='Weigth',
        attribute='weight',)
    ptype = fields.Field(
        column_name='PType',
        attribute='ptype',)
    HarmonizedCode = fields.Field(
        column_name='HarmonizedCode',
        attribute='harmonizedcode',)
    eccn = fields.Field(
        column_name='ECCN',
        attribute='eccn',)
    lkz = fields.Field(
        column_name='LKZ',
        attribute='lkz',)
    ag = fields.Field(
        column_name='AG',
        attribute='ag',)
    imageurl = fields.Field(
        column_name='imageURL',
        attribute='imageurl',)
        
    class Meta:
        model = Product
        fields = ('pdid', 'name', 'descr1', 'descr2', 
                'detail', 'remarks', 'status_id' ,'price', 
                'date', 'Handlager', 'lang_id', 'weight', 
                'ptype', 'HarmonizedCode', 'eccn', 'lkz', 
                'ag', 'imageurl',)
        list_display = ('name','descr1',)
        import_id_fields = ('pdid',)
        skip_unchanged = True # skip unchanged records
        report_skipped = True # whether skipped records appear in the import Result object
        exclude = ('id',)

    