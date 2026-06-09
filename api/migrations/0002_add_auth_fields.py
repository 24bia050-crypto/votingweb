from django.db import migrations, models


def add_auth_fields(apps, schema_editor):
    # tumia Django schema editor badala ya raw SQL
    User = apps.get_model('api', 'Voter')
    table_name = User._meta.db_table

    with schema_editor.connection.cursor() as cursor:

        # check password column exists (portable way)
        columns = schema_editor.connection.introspection.get_table_description(
            cursor, table_name
        )
        column_names = [col.name for col in columns]

        if 'password' not in column_names:
            cursor.execute(
                f"ALTER TABLE {table_name} ADD COLUMN password VARCHAR(128) NULL"
            )

        if 'token' not in column_names:
            cursor.execute(
                f"ALTER TABLE {table_name} ADD COLUMN token VARCHAR(64) NULL"
            )

        # UNIQUE index safe check (Postgres/SQLite safe way)
        try:
            cursor.execute(
                f"CREATE UNIQUE INDEX ux_{table_name}_token ON {table_name}(token)"
            )
        except Exception:
            pass


def remove_auth_fields(apps, schema_editor):
    User = apps.get_model('api', 'Voter')
    table_name = User._meta.db_table

    with schema_editor.connection.cursor() as cursor:

        try:
            cursor.execute(f"DROP INDEX ux_{table_name}_token")
        except Exception:
            pass

        # SQLite/Postgres safe drop (ignore errors)
        try:
            cursor.execute(f"ALTER TABLE {table_name} DROP COLUMN token")
        except Exception:
            pass

        try:
            cursor.execute(f"ALTER TABLE {table_name} DROP COLUMN password")
        except Exception:
            pass


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_auth_fields, remove_auth_fields),
    ]