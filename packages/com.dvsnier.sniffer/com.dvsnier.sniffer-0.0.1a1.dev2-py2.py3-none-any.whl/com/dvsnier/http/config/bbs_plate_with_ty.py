# -*- coding:utf-8 -*-


def get_json_with_tianya():
    'the json with tianya str data'
    json_with_str = ''' {
            "title": {
                "select": "div#post_head.atl-head > h1.atl-title > span.s_title > span"
            },
            "author_or_introduce": {
                "find": {
                    "name": "div",
                    "attrs": {
                        "class": "atl-menu clearfix js-bbs-act"
                    }
                },
                "child": {
                    "name": "div",
                    "attrs": {
                        "class": "atl-info"
                    }
                }
            },
            "meta": {
                "select": "div.atl-menu.clearfix.js-bbs-act"
            },
            "system": {
                "article": {
                    "article_link": "js_pageurl"
                }
            },
            "publisher": {
                "attrs": {
                    "attr_name": "class",
                    "author_name": "_host",
                    "author_id": "_hostid",
                    "author_time": "replytime"
                },
                "select": "div#alt_reply a.reportme.a-link",
                "child": {
                    "name": "div",
                    "attrs": {
                        "class": "bbs-content clearfix"
                    }
                }
            },
            "respondent": {
                "attrs": {
                    "author_name": "_host",
                    "author_id": "_hostid",
                    "author_time": "js_restime"
                },
                "select": "div:not(.host-item).atl-item",
                "child": {
                    "select": "div.atl-con-bd.clearfix div.bbs-content",
                    "reply_key": "replyid",
                    "sequence": "id"
                },
                "subordinate_reply_item": {
                    "select": "div.atl-con-bd.clearfix div.item-reply-view div.ir-list li",
                    "li_item": {
                        "select": "div.atl-con-bd.clearfix div.bbs-content",
                        "attrs": {
                            "comment_key_with_union_id": "id",
                            "comment_key_with_union_rid": "_rid",
                            "comment_name": "_username",
                            "comment_id": "_userid",
                            "comment_time": "_replytime",
                            "comment_content": {
                                "select": "span.ir-content"
                            }
                        },
                        "more_comment": {
                            "reply": {
                                "select": "div.atl-con-bd.clearfix div.atl-reply",
                                "attrs": {
                                    "id": "id"
                                }
                            },
                            "select": "div.atl-con-bd.clearfix div.item-reply-view div.ir-action div.ir-page",
                            "attrs": {
                                "comment_index": "_index",
                                "comment_page_count": "_pagecount",
                                "comment_key_with_union_id": "id",
                                "comment_key_with_union_rid": "_rid",
                                "comment_name": "author_name",
                                "comment_id": "author_id",
                                "comment_time": "comment_time",
                                "comment_content": "content"
                            }
                        }
                    }
                }
            },
            "present": {
                "find": {
                    "name": "div",
                    "attrs": {
                        "class": "atl-main"
                    },
                    "find_child": {
                        "name": "div",
                        "attrs": {
                            "class": "atl-item host-item"
                        }
                    }
                }
            }
        }
        '''
    return json_with_str
