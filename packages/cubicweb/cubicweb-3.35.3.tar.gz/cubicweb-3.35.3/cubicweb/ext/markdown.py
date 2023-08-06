import logging

import markdown

log = logging.getLogger(__name__)


def markdown_publish(context, data):
    """publish a string formatted as MarkDown Text to HTML

    :type context: a cubicweb application object

    :type data: str
    :param data: some MarkDown text

    :rtype: unicode
    :return:
      the data formatted as HTML or the original data if an error occurred
    """
    md = markdown.Markdown(extensions=["mdx_urlize:UrlizeExtension"])
    try:
        return md.convert(data)
    except Exception:
        import traceback

        traceback.print_exc()
        log.exception("Error while converting Markdown to HTML")
        return data
