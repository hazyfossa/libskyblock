from readable_number import ReadableNumber

human_readable_form = ReadableNumber(precision=1, use_shortform=True)


def humanize(i: float | int) -> str:
    return human_readable_form.of(i)
