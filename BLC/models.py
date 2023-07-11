from django.db import models
from django_db_views.db_view import DBView

class Items(models.Model):
    item_id = models.IntegerField(primary_key=True)
    item_name = models.CharField(unique=True, max_length=20)
    price = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'items'


class Sales(models.Model):
    sale_id = models.AutoField(primary_key=True)
    store = models.ForeignKey('Store', models.DO_NOTHING)
    sale_date = models.DateField(blank=True, null=True)
    total_price = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sales'
    
class DetailSale(models.Model):
    detail_sale_id = models.AutoField(primary_key=True)
    sale = models.ForeignKey('Sales', models.DO_NOTHING)
    item = models.ForeignKey('Items', models.DO_NOTHING)
    quantity = models.IntegerField(blank=True, null=True)
    unit_price = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'detail_sale'


class Stock(models.Model):
    stock_id = models.AutoField(primary_key=True)
    store = models.ForeignKey('Store', models.DO_NOTHING)
    item = models.ForeignKey(Items, models.DO_NOTHING)
    quantity = models.PositiveIntegerField()
    shelf_no = models.CharField(max_length=2, blank=True, null=True)
    shelf_floor = models.IntegerField(blank=True, null=True)
    item_order = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stock'


class Store(models.Model):
    store_id = models.AutoField(primary_key=True)
    store_name = models.CharField(unique=True, max_length=45)
    located = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'store'


class Daily_Sales(DBView):
    view_definition = """
    CREATE VIEW `DAILY_SALES` AS
    select store_id, sale_date, sum(total_price) as total_amount
    from sales
    group by store_id, sale_date
    order by 1, 2
    """

    class Meta:
        managed = False
        db_table = "Daily_Sales"

class Monthly_Sales(DBView):
    view_definition = """
    CREATE VIEW `DAILY_SALES` AS
    select store_id, sale_date, sum(total_price) as total_amount
    from sales
    group by store_id, sale_date
    order by 1, 2
    """

    class Meta:
        managed = False
        db_table = "Monthly_Sales"