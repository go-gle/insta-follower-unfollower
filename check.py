from followers_checker import FollowerChecker
from argparse import ArgumentParser


def get_args():
    parser = ArgumentParser(
        prog='Unfollowers checker',
        description='Check the diff between following and followers',
    )
    parser.add_argument('--user', required=True)
    parser.add_argument('--password', required=True)
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    unfollowers = FollowerChecker(args.user, args.password).get_followers_unfollowers()
    print('\n'.join(unfollowers))
