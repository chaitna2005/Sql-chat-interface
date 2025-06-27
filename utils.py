def to_markdown_table(data):
    if not data:
        return "No results found."
    headers = list(data[0].keys())
    header_row = "| " + " | ".join(headers) + " |"
    separator_row = "| " + " | ".join(["---"] * len(headers)) + " |"
    rows = []
    for row in data:
        rows.append("| " + " | ".join(str(row[h]) for h in headers) + " |")
    return "\n".join([header_row, separator_row] + rows)


