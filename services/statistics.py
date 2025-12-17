def count_likes(post_id: int, likes: list[dict]) -> int:
    return sum(1 for like in likes if like["post_id"] == post_id)
