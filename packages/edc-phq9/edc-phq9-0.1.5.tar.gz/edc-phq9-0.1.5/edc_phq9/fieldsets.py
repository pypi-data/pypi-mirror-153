from django.utils.html import format_html


def get_phq9_fields() -> tuple:
    return (
        "ph9interst",
        "ph9feel",
        "ph9troubl",
        "ph9tired",
        "ph9appetit",
        "ph9badabt",
        "ph9concen",
        "ph9moving",
        "ph9though",
        "ph9functio",
    )


def get_phq9_fieldsets() -> tuple:
    return (
        "PHQ-9",
        {
            "description": format_html(
                "<h3>Over the last 2 weeks, how often have you been bothered "
                "by any of the following?</h3>"
            ),
            "fields": get_phq9_fields(),
        },
    )
