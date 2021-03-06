from superform.models import Channel, Post, Publishing
from superform.plugins import rss
from superform.plugins.rss import post_pre_validation


def test_pre_validate_post_title():
    chan = Channel
    chan.module = "superform.plugins.rss"
    pre_validate_post_title(chan, 40000)


def test_pre_validate_post_description():
    chan = Channel
    chan.module = "superform.plugins.rss"
    pre_validate_post_description(chan, 40000)


def test_prevalidate_post_link_url():
    chan = Channel
    chan.module = "superform.plugins.rss"
    pre_validate_post_Link_url(chan)


def test_prevalidate_post_img_url():
    chan = Channel
    chan.module = "superform.plugins.rss"
    pre_validate_post_img_url(chan)


def test_postpre_rss():
    ret_code = rss.post_pre_validation(
        Post(title="rss test", description="desc rss test", link_url="www.test.com", image_url="www.test.com"))
    assert ret_code == 1


def pre_validate_post_title(channel, maxLengthTitle):
    post = Post
    post.title = "x" * maxLengthTitle
    post.description = "x"
    post.link_url = "https://www.test.com"
    post.image_url = "https://www.test.com"
    assert post_pre_validation(post) == 1
    post.title += "x"
    assert post_pre_validation(post) == 0
    post.title = ""
    assert post_pre_validation(post) == 0


def pre_validate_post_description(channel, maxLengthDescription):
    post = Post
    post.title = "x"
    post.description = "x" * maxLengthDescription
    post.link_url = "https://www.test.com"
    post.image_url = "https://www.test.com"
    assert post_pre_validation(post) == 1
    post.description += "x"
    assert post_pre_validation(post) == 0
    post.description = ""
    assert post_pre_validation(post) == 0


def pre_validate_post_Link_url(channel):
    post = Post
    post.title = "x"
    post.description = "x"
    post.link_url = "https://www.test.com"
    post.image_url = "https://www.test.com"
    assert post_pre_validation(post) == 1
    post.link_url = "test error link"
    assert post_pre_validation(post) == 0
    post.link_url = ""
    assert post_pre_validation(post) == 1


def pre_validate_post_img_url(channel):
    post = Post
    post.title = "x"
    post.description = "x"
    post.link_url = "https://www.test.com"
    post.image_url = "https://www.test.com"
    assert post_pre_validation(post) == 1
    post.image_url = "test error link"
    assert post_pre_validation(post) == 0
    post.image_url = ""
    assert post_pre_validation(post) == 1
