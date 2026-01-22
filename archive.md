---
layout: page
title: 文章存档
permalink: /archive.html
---

# 文章存档

## 按年份分类

{% for post in site.posts %}
  {% capture current_year %}{{ post.date | date: "%Y" }}{% endcapture %}
  {% if current_year != previous_year %}
    {% if previous_year %}
    </ul>
    {% endif %}
    <h2>{{ current_year }}</h2>
    <ul>
    {% capture previous_year %}{{ current_year }}{% endcapture %}
  {% endif %}
  <li>
    <span>{{ post.date | date: "%m月%d日" }}</span>
    <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
    {% if post.categories %}
    <span class="category">({{ post.categories | join: ", " }})</span>
    {% endif %}
  </li>
{% endfor %}
</ul>

<style>
.archive {
  margin-top: 30px;
}

.archive h2 {
  margin-top: 30px;
  color: #667eea;
  border-bottom: 2px solid #667eea;
  padding-bottom: 10px;
}

.archive ul {
  list-style: none;
  padding: 0;
}

.archive li {
  padding: 8px 0;
  border-bottom: 1px solid #eee;
}

.archive li:last-child {
  border-bottom: none;
}

.archive li span {
  color: #999;
  font-size: 0.9em;
  margin-right: 15px;
}

.archive li a {
  color: #667eea;
  text-decoration: none;
}

.archive li a:hover {
  text-decoration: underline;
}

.archive .category {
  color: #999;
  font-size: 0.85em;
  margin-left: 10px;
}
</style>
