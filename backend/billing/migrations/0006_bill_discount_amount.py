# Generated migration

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0005_alter_bill_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='discount_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
