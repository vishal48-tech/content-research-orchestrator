from src.utils.scoring import score_source

def test_edu_domain():
    assert score_source("https://arxiv.org/abs/123", 500) == 0.9

def test_gov_domain():
    assert score_source("https://www.nih.gov/page", 500) == 0.9

def test_github_domain():
    assert score_source("https://github.com/user/repo", 500) == 0.7

def test_unknown_domain():
    assert score_source("https://random-blog.com/post", 500) == 0.5

def test_length_bonus_2000():
    assert score_source("https://example.com", 2500) == 0.6

def test_length_bonus_1000():
    assert score_source("https://example.com", 1500) == 0.55

def test_max_cap():
    assert score_source("https://arxiv.org", 3000) == 1.0

def test_no_length_bonus():
    assert score_source("https://example.com", 500) == 0.5