"""kaggle-competitions — registration.

Wires the four agent tools. The desktop pane (desktop/plugin.js) and dashboard API
(dashboard/plugin_api.py) are declared in plugin.yaml and loaded by their surfaces.
"""
from __future__ import annotations

import logging

from . import schemas, tools

logger = logging.getLogger(__name__)


def register(ctx):
    ctx.register_tool(name="kaggle_list_submissions", toolset="kaggle",
                      schema=schemas.KAGGLE_LIST_SUBMISSIONS, handler=tools.kaggle_list_submissions)
    ctx.register_tool(name="kaggle_score_history", toolset="kaggle",
                      schema=schemas.KAGGLE_SCORE_HISTORY, handler=tools.kaggle_score_history)
    ctx.register_tool(name="kaggle_watch", toolset="kaggle",
                      schema=schemas.KAGGLE_WATCH, handler=tools.kaggle_watch)
    ctx.register_tool(name="kaggle_leaderboard", toolset="kaggle",
                      schema=schemas.KAGGLE_LEADERBOARD, handler=tools.kaggle_leaderboard)
    logger.info("kaggle-competitions: 4 tools registered")
