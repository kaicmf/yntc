---
layout: default
---

<div class="container">
    <h1 style="font-size: 2.5em; margin-bottom: 10px; color: #667eea;">{{ site.title }}</h1>
    <p style="font-size: 1.2em; color: #666; margin-bottom: 40px;">{{ site.tagline }}</p>

    {% if site.posts.size > 0 %}
    <div class="posts-list">
        {% for post in site.posts limit: 10 %}
        <div class="post-item">
            <h2><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h2>
            <p class="post-meta">
                <time datetime="{{ post.date | date_to_xmlschema }}">
                    {{ post.date | date: "%Y年%m月%d日" }}
                </time>
                {% if post.categories %}
                | 分类：{{ post.categories | join: ', ' }}
                {% endif %}
            </p>
            <p class="post-excerpt">{{ post.excerpt | strip_html | truncatewords: 50 }}</p>
            <a href="{{ post.url | relative_url }}" style="color: #667eea;">阅读更多 →</a>
        </div>
        {% endfor %}
    </div>

    <!-- Pagination -->
    {% if paginator.total_pages > 1 %}
    <div style="text-align: center; margin-top: 40px;">
        {% if paginator.previous_page %}
        <a href="{{ paginator.previous_page_path | relative_url }}">← 上一页</a>
        {% endif %}
        
        <span>第 {{ paginator.page }} 页，共 {{ paginator.total_pages }} 页</span>
        
        {% if paginator.next_page %}
        <a href="{{ paginator.next_page_path | relative_url }}">下一页 →</a>
        {% endif %}
    </div>
    {% endif %}
    {% else %}
    <p style="text-align: center; color: #666; font-size: 1.1em; margin-top: 60px;">
        暂时还没有文章，敬请期待...
    </p>
    {% endif %}
</div>
