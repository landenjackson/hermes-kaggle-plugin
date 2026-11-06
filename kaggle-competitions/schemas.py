"""Tool schemas — what the LLM sees."""

KAGGLE_LIST_SUBMISSIONS = {
    "name": "kaggle_list_submissions",
    "description": (
        "List recent Kaggle submissions for a competition, with best score and status. "
        "Omit competition to check all tracked competitions. Use whenever the user asks "
        "about their Kaggle submissions, scores, or results."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "competition": {
                "type": "string",
                "description": "Competition slug (e.g. 'titanic'). Omit to check all tracked competitions.",
            },
        },
    },
}

KAGGLE_SCORE_HISTORY = {
    "name": "kaggle_score_history",
    "description": (
        "Full chronological score history for one Kaggle competition — every submission "
        "with date, score and description, plus the best score. Use for trend questions "
        "('how has my score moved?', 'what was my best submission?')."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "competition": {
                "type": "string",
                "description": "Competition slug. Defaults to the first tracked competition.",
            },
        },
    },
}

KAGGLE_WATCH = {
    "name": "kaggle_watch",
    "description": (
        "Poll all tracked competitions right now and report any NEW completed scores "
        "since the last check (pending submissions that finished, or first-seen results). "
        "Use for 'any new scores?', or as the polling action in a scheduled job."
    ),
    "parameters": {"type": "object", "properties": {}},
}

KAGGLE_LEADERBOARD = {
    "name": "kaggle_leaderboard",
    "description": (
        "Fetch the public leaderboard (top N) for a Kaggle competition. Use when the user "
        "asks where they stand or what the top scores look like."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "competition": {"type": "string", "description": "Competition slug."},
            "top": {"type": "integer", "description": "How many rows (default 10)."},
        },
        "required": ["competition"],
    },
}
