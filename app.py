import datetime

from flask import Flask, render_template, jsonify, Response, request

app = Flask(__name__)


@app.route('/')
def index_view():
    username = request.args.get('username')
    posts = []  # allows function to return even when not on a user's timeline
    if username:
        posts = create_timeline(username)

    return render_template('index.html', username=username, posts=posts)


@app.route('/users')
def users_view():
    with open('./users.json', 'r') as f:
        users = f.read()
    return Response(users, mimetype="application/json")


@app.route('/posts')
def posts_view():
    with open('./posts.json', 'r') as f:
        posts = f.read()
    return Response(posts, mimetype="application/json")


# Fetches a user's following list given their username
def get_following(username, all_users):
    following = all_users[username]
    return following


# fetches, formats and orders posts from a given list of users
def get_posts(users, all_posts):
    posts = []

    for user in users:
        user_posts = all_posts[user]  # list of all posts by a user
        for post in user_posts:
            post['user'] = user
            posts.append(post)

    posts.sort(key=lambda item: item['time'])  # order by latest first

    # format time for readability
    for post in posts:
        time = datetime.datetime.strptime(post['time'], '%Y-%m-%dT%H:%M:%SZ')
        formatted_time = time.strftime('%a %b %d %Y %H:%M')
        post['time'] = formatted_time

    return posts


# Compiles posts to be displayed on a given user's timeline
def create_timeline(username):
    all_users = users_view().json
    all_posts = posts_view().json

    following = get_following(username, all_users)
    timeline_users = following + [username]  # include users own posts
    timeline_posts = get_posts(timeline_users, all_posts)

    return timeline_posts


if __name__ == '__main__':
    app.run(host='127.0.0.1')
