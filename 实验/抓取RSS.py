import feedparser

# feedparser文档：https://feedparser.readthedocs.io/en/latest/index.html


def odaily():
    """
    通过RSS接口获取Odaily上的最新文章。

    官方文档：
    https://github.com/ODAILY/RSS

    RSS 接口返回包含以下元素的 XML 文档：
    <channel>：RSS 频道信息。
        <title>：频道标题。
        <link>: 频道网址。
        <description>：频道说明。
        <language>：当前语言。
        <item>：包含有关文章的信息。 A <channel>可以包含多个 < items >.
            <title>： 标题。
            <description>： 描述 。
            <author>： 作者
            <link>：网址。
            <source>： 来源
            <pubDate>：文章的发表日期。
            <content>： 内容。
            <guid>: 指导。
            <media>: 图片链接
    """
    d = feedparser.parse('https://www.odaily.news/v1/openapi/odailyrss')

    print(d.feed)
    print(d.entries)
    print(len(d.entries))

odaily()