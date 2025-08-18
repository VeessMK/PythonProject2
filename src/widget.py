def get_date(full_date: str) -> str:
    """
    Принимает формат "2024-03-11T02:26:18.671407"
    и возвращает строку с датой в формате
    "ДД.ММ.ГГГГ"
    """

    return f'{full_date[8:10]}.{full_date[5:7]}.{full_date[:4]}'