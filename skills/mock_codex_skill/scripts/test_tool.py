import openai

def my_tool(arg1):
    return f'Hello {arg1}'
if __name__ == '__main__':
    import argparse
    import json
    import sys
    parser = argparse.ArgumentParser()
    parser.add_argument('--args', type=str, help='JSON string of arguments')
    args = parser.parse_args()
    try:
        kwargs = json.loads(args.args) if args.args else {}
        result = my_tool(**kwargs)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f'Error executing my_tool: {e}', file=sys.stderr)
        sys.exit(1)