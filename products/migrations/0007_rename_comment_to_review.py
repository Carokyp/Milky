import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0006_alter_product_options_product_background_image_and_more"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Comment",
            new_name="Review",
        ),
        migrations.AlterField(
            model_name="review",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="reviews",
                to="products.product",
            ),
        ),
    ]
