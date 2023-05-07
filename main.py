import openai
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost

# GPT-4 APIキーを設定
openai.api_key = "your_openai_api_key"

# キーワードを設定
keyword = "your_keyword_here"

# GPT-4でコンテンツを生成
prompt = f"Write a blog post about {keyword}."
response = openai.Completion.create(
    engine="gpt-4",
    prompt=prompt,
    max_tokens=1024,
    n=1,
    stop=None,
    temperature=0.7,
)

generated_content = response.choices[0].text.strip()

# WordPressの認証情報を設定
wp_url = "your_wordpress_url/xmlrpc.php"
wp_username = "your_wordpress_username"
wp_password = "your_wordpress_password"

# WordPressクライアントを初期化
wp_client = Client(wp_url, wp_username, wp_password)

# 新しい記事を作成
post = WordPressPost()
post.title = f"Blog post about {keyword}"
post.content = generated_content
post.post_status = "publish"  # 記事をすぐに公開する場合は 'publish'、下書きのままにする場合は 'draft'

# 記事をWordPressに投稿
post_id = wp_client.call(NewPost(post))
print(f"Post successfully published with ID: {post_id}")