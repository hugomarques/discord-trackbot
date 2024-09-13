def paginate_messages(messages, max_chars=2000):
    pages = []
    current_page = ""

    for message in messages:
        if len(current_page) + len(message) + 1 > max_chars:
            pages.append(current_page.strip())
            current_page = message + "\n"
        else:
            current_page += message + "\n"

    if current_page:
        pages.append(current_page.strip())

    return pages
