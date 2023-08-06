from filum.helpers import html_to_md, current_timestamp


def parse_reddit(obj):
    content = obj.r
    response_parent = content[0]['data']['children'][0]['data']
    response_comments = content[1]['data']['children']

    comments = {}

    def get_comments(comments_dict, path=[], depth_tracker=[]):
        for comment in comments_dict:
            id = comment['data']['name']
            # print('replies: ', comment['data']['replies'])
            replies = comment['data']['replies']
            parent_id = comment['data']['parent_id']
            is_submitter = 1 if comment['data']['is_submitter'] else 0
            depth = comment['data']['depth']
            depth_tracker.append(depth)
            if len(depth_tracker) >= 2 and depth_tracker[-1] == depth_tracker[-2]:
                path[-1] = id
            elif len(depth_tracker) >= 2 and depth_tracker[-1] < depth_tracker[-2]:
                path = path[:depth+1]
            else:
                path.append(id)

            comment_body = comment['data']['body_html']
            comment_body = html_to_md(comment_body)
            comments.update({
                id: {
                    'author': comment['data']['author'],
                    'text': comment_body,
                    'timestamp': comment['data']['created_utc'],
                    'permalink': comment['data']['permalink'],
                    'upvotes': comment['data']['ups'],
                    'downvotes': comment['data']['downs'],
                    'score': comment['data']['score'],
                    'parent_id': parent_id,
                    'ancestor_id': response_parent['name'],
                    'is_submitter': is_submitter,
                    'depth': comment['data']['depth'],
                    'path': '/'.join(path)
                    }
                })
            print(html_to_md(comment['data']['body_html']))
            if 'author_fullname' in comment['data'].keys():
                comments[id]['author_id'] = comment['data']['author_fullname']
            else:
                comments[id]['author_id'] = None

            if len(replies) == 0:
                continue
            else:
                get_comments(replies['data']['children'], path, depth_tracker)

    get_comments(response_comments)
    body = html_to_md(response_parent['selftext_html']) if response_parent['selftext_html'] else None
    parent_metadata = {
        'title': response_parent['title'],
        'body': body,
        'permalink': response_parent['permalink'],
        'num_comments': response_parent['num_comments'],
        'author': response_parent['author'],
        'score': response_parent['score'],
        'id': response_parent['name'],
        'source': obj.site,
        'posted_timestamp': response_parent['created_utc'],
        'saved_timestamp': current_timestamp()
    }

    thread = {
        'parent_data': parent_metadata,
        'comment_data': comments
    }
    return thread
