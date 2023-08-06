#!/usr/bin/python3
import arequest
import asyncio
import argparse
import importlib.resources

__version__ = "1.4.2"

headers = {
    "User-Agent": "User-Agent:Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
}

async def scan(url, args, paths):
    async with arequest.Session() as session:
        while True:
            if paths:
                path = paths.pop()
            else:
                break
            r = await session.get(url + path, verify=False, headers=headers)
            if r.status_code != 404 and str(r.status_code) not in args.exclude:
                for i in args.exclude:
                    if i in r.text: return

                print(f"[{r.status_code}] {path}")

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("-e", "--exclude", action="append", help="exclude status_code or content", default=[])
    parser.add_argument("-t", "--thread", default=5, help="threads, default 5")

    args = parser.parse_args()
    url = args.url[:-1] if args.url.endswith("/") else args.url

    paths = importlib.resources.read_text("ctfscan", "default.txt").split("\n")

    tasks = []
    for _ in range(args.thread):
        tasks.append(scan(url, args, paths))

    await asyncio.gather(*tasks)

def run():
    asyncio.run(main())

if __name__ == '__main__':
    run()
